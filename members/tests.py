# members.tests
# Testing for the members app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 22 09:25:12 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: tests.py [] benjamin@bengfort.com $

"""
Testing for the members app.
"""

##########################################################################
## Imports
##########################################################################

import hashlib
import unittest

from rest_framework import status
from members.models import Profile

from django.test import TestCase, Client
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

##########################################################################
## User Fixture
##########################################################################

fixtures = {
    'user': {
        'username': 'jdoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'jdoe@example.com',
        'password': 'supersecret',
    },
    'api_user': {
        'username': 'starbucks',
        'first_name': 'Jane',
        'last_name': 'Windemere',
        'profile': {
            'biography': 'Originally from Seattle, now lives in Portland',
            'organization': 'SETI'
        }
    }
}

##########################################################################
## Model Tests
##########################################################################


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(**fixtures['user'])

    def test_profile_on_create(self):
        """
        Test the User post_save signal to create a profile
        """

        self.assertEqual(Profile.objects.count(), 1, "begin profile count mismatch (user mock has no profile?)")
        u = User.objects.create_user(username="test", email="test@example.com", password="password")
        self.assertEqual(Profile.objects.count(), 2, "additional profile object doesn't exist")
        self.assertIsNotNone(u.profile)

    def test_profile_email_hash_md5(self):
        """
        Ensure that the email_hash on a user is an MD5 digest
        """

        email   = "Jane.Doe@gmail.com"
        udigest = hashlib.md5(email).hexdigest()
        ldigest = hashlib.md5(email.lower()).hexdigest()

        u = User.objects.create_user(username="test", email=email, password="password")
        self.assertIsNotNone(u.profile, "user has no profile?")
        self.assertIsNotNone(u.profile.email_hash, "user has no email hash?")

        self.assertNotEqual(udigest, u.profile.email_hash, "email was not lower case before digest")
        self.assertEqual(ldigest, u.profile.email_hash, "email not hashed correctly")

    def test_profile_email_hash_create(self):
        """
        Email should be hashed on user create
        """

        digest = hashlib.md5(fixtures['user']['email']).hexdigest()

        self.assertIsNotNone(self.user.profile, "user has no profile?")
        self.assertIsNotNone(self.user.profile.email_hash, "user has no email hash?")
        self.assertEqual(digest, self.user.profile.email_hash, "email hash does not match expected")

    def test_profile_email_hash_update(self):
        """
        Email should be hashed on user update
        """

        newemail = "john.doe@gmail.com"
        digest   = hashlib.md5(newemail).hexdigest()

        self.user.email = newemail
        self.user.save()

        self.assertEqual(digest, self.user.profile.email_hash, "email hash does not match expected")


##########################################################################
## View Tests
##########################################################################


class UserViewsTest(TestCase):

    def setUp(self):
        self.user   = User.objects.create_user(**fixtures['user'])
        self.client = Client()

    def login(self):
        credentials = {
            'username': fixtures['user']['username'],
            'password': fixtures['user']['password'],
        }

        return self.client.login(**credentials)

    def logout(self):
        return self.client.logout()

    @unittest.skip('not implemented yet')
    def test_profile_view_auth(self):
        """
        Assert that profile can only be viewed if logged in.
        """
        endpoint = reverse('profile')
        loginurl = reverse('social:begin', args=('google-oauth2',))
        params   = "next=%s" % endpoint
        expected = "%s?%s" % (loginurl, params)
        response = self.client.get(endpoint)

        self.assertRedirects(response, expected, fetch_redirect_response=False)

    @unittest.skip('not implemented yet')
    def test_profile_object(self):
        """
        Assert the profile gets the current user
        """

        endpoint = reverse('profile')

        self.login()
        response = self.client.get(endpoint)

        self.assertEqual(self.user, response.context['user'])

    @unittest.skip('not implemented yet')
    def test_profile_template(self):
        """
        Check that the right template is being used
        """
        endpoint = reverse('profile')

        self.login()
        response = self.client.get(endpoint)

        self.assertTemplateUsed(response, 'registration/profile.html')


class UserAPITest(APITestCase):

    def setUp(self):
        self.user   = User.objects.create_user(**fixtures['user'])
        self.client.force_authenticate(user=self.user)

    @unittest.skip('not implemented yet')
    def test_user_create(self):
        """
        Check that a user can be created using the POST method
        Required to test because the serializer overrides create.
        NOTE: MUST POST IN JSON TO UPDATE/CREATE PROFILE
        """
        endpoint = reverse("api:user-list")
        response = self.client.post(endpoint, data=fixtures['api_user'],
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that a profile and user exist in database
        user = User.objects.filter(username=fixtures['api_user']['username'])
        profile = Profile.objects.filter(user=user)

        self.assertEquals(len(user), 1)
        self.assertEquals(len(profile), 1)

        self.assertEqual(profile[0].organization, 'SETI')

    @unittest.skip('not implemented yet')
    def test_user_update(self):
        """
        Check that a user can be updated using a PUT method
        Required to test because the serializer overrides update.
        NOTE: MUST POST IN JSON TO UPDATE/CREATE PROFILE
        """

        endpoint = reverse("api:user-detail", kwargs={"pk": self.user.pk})

        # Check that the user profile exists
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update the profile
        content  = {
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "profile": {
                "biography": "This is a test bio.",
                "organization": "NASA"
            }
        }

        response = self.client.put(endpoint, content, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Fetch the profile again
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.profile.organization, "NASA")
