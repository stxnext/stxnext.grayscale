
# -*- coding: utf-8 -*-
"""Base module for unittesting."""

import unittest

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import applyProfile


class GrayscaleLayer(PloneSandboxLayer):
    """Testing layer for stxnext.grayscale addon"""

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import stxnext.grayscale

        self.loadZCML(package=stxnext.grayscale)

        from OFS.Application import install_package
        install_package(app, stxnext.grayscale, stxnext.grayscale.initialize)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # import default profile
        applyProfile(portal, 'stxnext.grayscale:default')
        # Create test content
        # 1. Login as user with Manager privilages
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        # 2. Create and publish homepage object
        """
        portal.invokeFactory(id='homepage', type_name='GDACHomePage')
        homepage = portal.homepage
        homepage.setTitle('Homepage title')
        homepage.reindexObject()
        """

        import transaction
        transaction.commit()


    def tearDownZope(self, app):
        """Tear down Zope."""
        pass

FIXTURE = GrayscaleLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="GrayscaleLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="GrayscaleLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING

class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING

