import logging
from xml.dom import minidom

from django.conf import settings

from .marshall import EventXml
from .models import Event, EventTypes
from oauth import Consumer, Client


log = logging.getLogger(__name__)

consumer_key = settings.TC_CONSUMER_KEY
consumer_secret = settings.TC_CONSUMER_SECRET

message_template = """
<result>
   <success>%s</success>
   <errorCode>%s</errorCode>
   <message>%s</message>
</result>
"""

subscription_order_message_template = """
<result>
   <success>%s</success>
   <message>%s</message>
   <accountIdentifier>%s</accountIdentifier>
</result>
"""

simple_success_message = """
<result>
   <success>true</success>
</result>
"""


def fetch_event(url):
    consumer = Consumer(consumer_key, consumer_secret)
    client = Client(consumer)
    resp, content = client.request(url)
    event = Event()
    event.status = int(resp['status'])

    if event.status == 200:
        xml_document = minidom.parseString(content)
        event_xml = EventXml(xml_document)
        event.raw = event_xml.pretty_print

        try:
            event.type = int(EventTypes(event_xml.eventType))
        except ValueError:
            event.type = int(EventTypes.UNKNOWN)

        event.save()
        return handle_event(event_xml)
    else:
        message = "HTTP response %d" % event.status
        log.error(message)
        event.save()
        return message_template % ('false', "UNKNOWN_ERROR", message)


def handle_event(event_xml):
    log.info("Recevied event type %s" % event_xml.eventType)
    if event_xml.eventType == "SUBSCRIPTION_ORDER":
        return create_order(event_xml)
    elif event_xml.eventType == "SUBSCRIPTION_CHANGE":
        return change_order(event_xml)
    elif event_xml.eventType == "SUBSCRIPTION_CANCEL":
        return cancel_order(event_xml)
    elif event_xml.eventType == "SUBSCRIPTION_NOTICE":
        return notice_order(event_xml)
    elif event_xml.eventType == "USER_ASSIGNMENT":
        return assign_user(event_xml)
    elif event_xml.eventType == "USER_UNASSIGNMENT":
        return unassign_user(event_xml)
    else:
        message = "Event type %s is not configured" % event_xml.eventType
        return message_template % ('false', 'CONFIGURATION_ERROR', message)


def create_order(event_xml):
    log.info("Read %s %s %s" % (
        event_xml.payload.company.name,
        event_xml.payload.company.website,
        event_xml.payload.order.edition))

    org = event_xml.payload.create_organization()
    owner = event_xml.creator.create_user_model(org, admin=True)
    subscription = event_xml.payload.create_subscription(owner)
    event_xml.payload.create_user_licenses(subscription)

    if subscription:
        # subscription owner uses already one license
        subscription.attach_or_use_license(owner, 'permission')

        return subscription_order_message_template % (
            'true', 'Account creation successful', subscription.uuid)
    else:
        return message_template % (
            'false', 'ACCOUNT_NOT_FOUND',
            'The account could not be found')


def change_order(event_xml):
    account_id = event_xml.payload.account.account_identifier
    subscription = event_xml.payload.get_subscription(account_id)

    if subscription is None:
        message = "Account %s not found" % account_id
        log.error(message)
        return message_template % ('false', "ACCOUNT_NOT_FOUND", message)

    # Update the number of licenses
    event_xml.payload.update_user_licenses(subscription)

    return message_template % ('true', '', 'Subscription changed')


def cancel_order(event_xml):
    account_id = event_xml.payload.account.account_identifier
    subscription = event_xml.payload.get_subscription(account_id)

    if subscription is None:
        message = "Account %s not found" % account_id
        log.error(message)
        return message_template % ('false', "ACCOUNT_NOT_FOUND", message)

    # Delete users associated with this subscription and
    # release the license
    event_xml.payload.delete_associated_users(subscription)

    # delete organization
    event_xml.payload.delete_organization(subscription)

    # delete subscription owner
    event_xml.payload.delete_subscription_owner(subscription)

    # and finally remove the subscription
    event_xml.payload.delete_subscription(subscription)

    return message_template % ('true', '', 'Subscription cancelled succesfully')


def notice_order(event_xml):
    account_id = event_xml.payload.account.account_identifier
    subscription = event_xml.payload.get_subscription(account_id)

    if subscription is None:
        message = "Account %s not found" % account_id
        log.error(message)
        return message_template % ('false', "ACCOUNT_NOT_FOUND", message)

    # do something with the info we get from the MP
    event_xml.payload.notice(subscription)

    log.debug(message_template)
    return message_template % ('true', '', 'Subscription cancelled succesfully')


def assign_user(event_xml):
    account_id = event_xml.payload.account.account_identifier
    subscription = event_xml.payload.get_subscription(account_id)

    if subscription is None:
        message = "Account %s not found" % account_id
        log.error(message)
        return message_template % ('false', "ACCOUNT_NOT_FOUND", message)

    if subscription.licenses_available <= 0:
        return message_template % ('false', 'MAX_USERS_REACHED',
                                   'we have reached the limit of paid licenses')

    organization = event_xml.payload.get_organization(subscription)
    user = event_xml.payload.user.create_user_model(organization)
    event_xml.payload.attach_user_license(subscription, user)

    log.info("Assigning user %s to account %s" % (str(user), account_id))
    return simple_success_message


def unassign_user(event_xml):
    account_id = event_xml.payload.account.account_identifier
    subscription = event_xml.payload.get_subscription(account_id)

    if subscription is None:
        message = "Account %s not found" % account_id
        log.error(message)
        return message_template % ('false', "ACCOUNT_NOT_FOUND", message)

    openid = event_xml.payload.user.openid
    user = event_xml.payload.user.get_user(openid)

    if not user:
        log.error("User not found: %s" % openid)
        return message_template % ('false', "USER_NOT_FOUND", message)

    # remove the user
    event_xml.payload.user.remove_user(user)

    # release the license
    event_xml.payload.release_user_license(subscription, user)

    log.info("Unassigning user %s from account %s" % (user.username, account_id))
    return simple_success_message
