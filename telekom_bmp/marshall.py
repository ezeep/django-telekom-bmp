from social.utils import module_member
from xml.dom.minidom import Document

from django.conf import settings

UserMixin = module_member(
    getattr(settings, 'TC_USER_INTEGRATION', 'telekom_bmp.mixins.UserMixin'))
PayloadMixin = module_member(
    getattr(settings, 'TC_PAYLOAD_INTEGRATION', 'telekom_bmp.mixins.PayloadMixin'))


class EventXml(Document):
    eventXml = None
    eventType = None
    creator = None
    payload = None
    pretty_print = ""

    def __init__(self, xmlDocument):
        self.eventXml = xmlDocument

        # type is not a unique tag so we need to do this to get the event type
        types = self.eventXml.getElementsByTagName('event')[0].getElementsByTagName('type')
        for t in types:
            if t.parentNode.tagName == 'event':
                self.eventType = t.childNodes[0].data
                break

        self.creator = UserXml(self.eventXml, field="creator")
        self.payload = PayloadXml(self.eventXml)
        self.pretty_print = xmlDocument.toxml()

    def __str__(self):
        return self.pretty_print


class UserXml(UserMixin, Document):
    userXml = None
    openid = None
    email = None
    firstName = None
    lastName = None

    def __init__(self, xmlDocument, field="user"):
        elements = xmlDocument.getElementsByTagName(field)
        if len(elements) == 0:
            return
        self.userXml = elements[0]
        self.openid = self.userXml.getElementsByTagName("openId")[0].childNodes[0].data
        self.email = self.userXml.getElementsByTagName("email")[0].childNodes[0].data
        self.firstName = self.userXml.getElementsByTagName("firstName")[0].childNodes[0].data
        self.lastName = self.userXml.getElementsByTagName("lastName")[0].childNodes[0].data

    def __str__(self):
        return self.email


class OrderXml(Document):
    orderXml = None
    edition = None
    number_of_licenses = 0

    def __init__(self, xmlDocument):
        elements = xmlDocument.getElementsByTagName('order')
        if len(elements) == 0:
            return
        self.orderXml = elements[0]
        self.edition = self.orderXml.getElementsByTagName("editionCode")[0]\
            .childNodes[0].data

        for item in self.orderXml.getElementsByTagName('item'):
            if item.getElementsByTagName('unit')[0].childNodes[0].data == 'USER':
                self.number_of_licenses = int(
                    item.getElementsByTagName('quantity')[0].childNodes[0].data)
                break

    def __str__(self):
        return self.edition


class PayloadXml(PayloadMixin, Document):
    payloadXml = None
    account = None
    user = None
    order = None
    company = None

    def __init__(self, xmlDocument):
        elements = xmlDocument.getElementsByTagName('payload')
        if len(elements) == 0:
            return
        self.payloadXml = elements[0]
        self.account = AccountXml(self.payloadXml)
        self.user = UserXml(self.payloadXml)
        self.order = OrderXml(self.payloadXml)
        self.company = CompanyXml(self.payloadXml)


class CompanyXml(Document):
    companyXml = None
    name = None
    website = None

    def __init__(self, xmlDocument):
        elements = xmlDocument.getElementsByTagName('company')
        if len(elements) == 0:
            return
        self.companyXml = elements[0]
        self.name = self.companyXml.getElementsByTagName('name')[0].childNodes[0].data
        self.website = self.companyXml.getElementsByTagName('website')[0].childNodes[0].data

    def __str__(self):
        return self.name


class AccountXml(Document):
    account_xml = None
    account_identifier = None

    def __init__(self, xmlDocument):
        elements = xmlDocument.getElementsByTagName('account')
        if len(elements) == 0:
            return
        self.account_xml = elements[0]
        self.account_identifier = (
            self.account_xml.getElementsByTagName('accountIdentifier')[0].
            childNodes[0].data
        )

    def __str__(self):
        return self.account_identifier
