from django.test import TestCase
from portal.models import Organization


class UtilsTest(TestCase):
    def test_get_email_domain(self):
        """
            get email domain from web
        """
        example = u'http://www.example.com'
        expected_email_domain = 'example.com'

        org = Organization(website=example)

        self.assertEqual(org.get_email_domain(), expected_email_domain)

    def test_get_email_domain_empty(self):
        expected_email_domain = ''

        org = Organization(website='')

        self.assertEqual(org.get_email_domain(), expected_email_domain)
