import logging
log = logging.getLogger(__name__)


class UserMixin(object):
    """Creates a datastore model"""
    def create_user_model(self, organization, admin=False):
        """
        Creates a user.
        Available data:
            self.email
            self.openid
            self.firstName, self.lastName

        if admin is true, we are creating a superuser, the
        subscription owner.

        returns a user object (django or custom model)
        """
        pass

    def get_user(self, openid):
        """
        returns a user object (django or custom model)
        based on the openid gotten from the auth
        """
        pass

    def remove_user(self, user):
        """
        removes a user
        """
        pass


class PayloadMixin(object):

    def get_subscription(self, account_id):
        """
        based on the account_id returns a subscription object
        """
        pass

    def get_subscription_owner(self, subscription):
        """
        returns the user who owns the subscription
        """
        pass

    def create_subscription(self, owner):
        """
        creates a subscription objects and returns it
        """
        pass

    def delete_subscription_owner(self, subscription):
        pass

    def delete_subscription(self, subscription):
        pass

    def get_users(self, subscription):
        """
            returns the list of users in a subscripton except
            the owner
        """
        pass

    def create_user_licenses(self, subscription):
        """
        provision user licenses.
        The number of licenses bought is self.order.number_of_licenses
        """
        pass

    def update_user_licenses(self, subscription):
        """
        This function is called when there is a change on the number
        self.order.number_of_licenses
        """
        pass

    def attach_user_license(self, subscription, user):
        pass

    def release_user_license(self, subscription, user):
        pass

    def get_available_licenses(self, subscription):
        pass

    def delete_associated_users(self, subscription):
        pass

    def create_organization(self):
        """
        returns a new created organization
        """
        pass

    def get_organization(self, subscription):
        pass

    def delete_organization(self, subscription):
        pass

    def notice(self, subscription):
        pass
