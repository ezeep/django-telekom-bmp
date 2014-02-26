from social.backends.open_id import OpenIdAuth

class TelekomBMPOpenIDBackend(OpenIdAuth):
    URL = 'https://apps.telekomcloud.com/openid/id'
