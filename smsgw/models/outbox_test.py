# -*- coding: utf-8 -*-
# http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

import datetime

from smsgw.tests import SmsgwIntegrationTestCase
from smsgw.core import db
from smsgw.models import Outbox, Contact
from smsgw.models.datasets import outbox as outbox_datasets, \
    contacts as contacts_datasets


class OutboxModelTest(SmsgwIntegrationTestCase):

    def test_send(self):
        """ Testing outbox sending message """

        contact = Contact(**contacts_datasets.BASIC_CONTACT)
        db.session.add(contact)

        # no message passed
        with self.assertRaises(AssertionError):
            Outbox.send(message=None, destination_number="number")

        # message passed but is not string
        with self.assertRaises(AssertionError):
            Outbox.send(message=1, destination_number="number")

        # no destination number passed
        with self.assertRaises(AssertionError):
            Outbox.send(message="", destination_number=None)

        # destination passed but is not string
        with self.assertRaises(AssertionError):
            Outbox.send(message="", destination_number=22)

        ##
        # Default no compression coding
        ##

        #
        # Single message
        #

        # basic message
        outbox = Outbox.send(user=self.user, **outbox_datasets.SEND_BASIC)
        self.assertIsNotNone(outbox)
        self.assertIsNotNone(outbox.id)
        self.assertEqual(outbox.userId, self.user.id)
        self.assertIsNone(outbox.applicationId)
        self.assertEqual(outbox.destinationNumber,
                         outbox_datasets.SEND_BASIC['destination_number'])
        self.assertEqual(outbox.text,
                         outbox_datasets.SEND_BASIC['message'] \
                            .replace('{firstName}', '') \
                            .replace('{lastName}', ''))
        self.assertEqual(outbox.coding, outbox_datasets.SEND_BASIC['coding'])
        self.assertEqual(outbox.multipart, 'false')
        self.assertEqual(outbox.klass, 1)
        self.assertIsNotNone(outbox.sent)
        self.assertIsNotNone(outbox.sendTimeout)
        self.assertEqual(outbox.sendBefore, datetime.time(23, 59, 59))
        self.assertEqual(outbox.sendAfter, datetime.time(00, 00, 00))

        # basic message with contact
        outbox = Outbox.send(user=self.user, contact=contact,
                             **outbox_datasets.SEND_BASIC)
        self.assertIsNotNone(outbox)
        self.assertIsNotNone(outbox.id)
        self.assertEqual(outbox.userId, self.user.id)
        self.assertIsNone(outbox.applicationId)
        self.assertEqual(outbox.destinationNumber,
                         outbox_datasets.SEND_BASIC['destination_number'])
        self.assertEqual(outbox.text,
                         outbox_datasets.SEND_BASIC['message'] \
                            .replace('{firstName}', contact.firstName) \
                            .replace('{lastName}', contact.lastName))
        self.assertEqual(outbox.coding, outbox_datasets.SEND_BASIC['coding'])
        self.assertEqual(outbox.multipart, 'false')
        self.assertEqual(outbox.klass, 1)
        self.assertIsNotNone(outbox.sent)
        self.assertIsNotNone(outbox.sendTimeout)
        self.assertEqual(outbox.sendBefore, datetime.time(23, 59, 59))
        self.assertEqual(outbox.sendAfter, datetime.time(00, 00, 00))

        # flash message
        outbox = Outbox.send(user=self.user, **outbox_datasets.SEND_FLASH)
        self.assertIsNotNone(outbox)
        self.assertIsNotNone(outbox.id)
        self.assertEqual(outbox.userId, self.user.id)
        self.assertIsNone(outbox.applicationId)
        self.assertEqual(outbox.destinationNumber,
                         outbox_datasets.SEND_FLASH['destination_number'])
        self.assertEqual(outbox.text, outbox_datasets.SEND_FLASH['message'])
        self.assertEqual(outbox.coding, outbox_datasets.SEND_FLASH['coding'])
        self.assertEqual(outbox.multipart, 'false')
        self.assertEqual(outbox.klass, 0)
        self.assertIsNotNone(outbox.sent)
        self.assertIsNotNone(outbox.sendTimeout)
        self.assertEqual(outbox.sendBefore, datetime.time(23, 59, 59))
        self.assertEqual(outbox.sendAfter, datetime.time(00, 00, 00))

        #
        # Multipart messages
        #

        # basic multipart message
        dataset = outbox_datasets.MULTIPART_MESSAGES[0]
        outbox = Outbox.send(user=self.user, **dataset)
        multiparts = outbox.multiparts
        message = "{0}{1}{2}".format(
            outbox.text, multiparts[0].text, multiparts[1].text
        )
        self.assertIsNotNone(outbox)
        self.assertIsNotNone(outbox.id)
        self.assertEqual(outbox.userId, self.user.id)
        self.assertIsNone(outbox.applicationId)
        self.assertEqual(outbox.destinationNumber, dataset['destination_number'])
        self.assertEqual(outbox.coding, dataset['coding'])
        self.assertEqual(outbox.multipart, 'true')
        self.assertEqual(outbox.klass, 1)
        self.assertIsNotNone(outbox.sent)
        self.assertIsNotNone(outbox.sendTimeout)
        self.assertEqual(outbox.sendBefore, datetime.time(23, 59, 59))
        self.assertEqual(outbox.sendAfter, datetime.time(00, 00, 00))
        self.assertEqual(len(multiparts), 2)
        self.assertEqual(message, dataset['message'])
        for index, multipart in enumerate(multiparts):
            self.assertEqual(multipart.sequencePosition, index + 2)

        # flash multipart message
        dataset = outbox_datasets.MULTIPART_MESSAGES[1]
        outbox = Outbox.send(user=self.user, **dataset)
        multiparts = outbox.multiparts
        print multiparts
        message = "{0}{1}{2}{3}".format(
            outbox.text,
            multiparts[0].text,
            multiparts[1].text,
            multiparts[2].text
        )
        self.assertIsNotNone(outbox)
        self.assertIsNotNone(outbox.id)
        self.assertEqual(outbox.userId, self.user.id)
        self.assertIsNone(outbox.applicationId)
        self.assertEqual(outbox.destinationNumber, dataset['destination_number'])
        self.assertEqual(outbox.coding, dataset['coding'])
        self.assertEqual(outbox.multipart, 'true')
        self.assertEqual(outbox.klass, 0)
        self.assertIsNotNone(outbox.sent)
        self.assertIsNotNone(outbox.sendTimeout)
        self.assertEqual(outbox.sendBefore, datetime.time(23, 59, 59))
        self.assertEqual(outbox.sendAfter, datetime.time(00, 00, 00))
        self.assertEqual(len(multiparts), 3)
        self.assertEqual(message, dataset['message'])
        for index, multipart in enumerate(multiparts):
            self.assertEqual(multipart.sequencePosition, index + 2)

        # TODO(vojta) test UDH generation

        ##
        # Unicode
        ##

        # TODO(vojta)


    def test_get_message_multipart(self):
        """ Testing outbox splitting message to multiparts """

        #
        # Default no compression coding
        #

        msg = outbox_datasets.MULTIPART_MESSAGES[0]["message"]
        multiparts = Outbox.get_message_multipart(
            msg, 160,
            Outbox.DEFAULT_NO_COMPRESSION
        )
        self.assertEqual(len(multiparts), 3)
        self.assertEqual(multiparts[0], msg[:160])
        self.assertEqual(multiparts[1], msg[160:320])
        self.assertEqual(multiparts[2], msg[320:])

        msg = outbox_datasets.MULTIPART_MESSAGES[1]["message"]
        multiparts = Outbox.get_message_multipart(
            msg, 160,
            Outbox.DEFAULT_NO_COMPRESSION
        )
        self.assertEqual(len(multiparts), 4)
        self.assertEqual(multiparts[0], msg[:157])
        self.assertEqual(multiparts[1], msg[157:314])
        self.assertEqual(multiparts[2], msg[314:473])
        self.assertEqual(multiparts[3], msg[473:])


        #
        # Unicode
        #

        # TODO(vojta)


    def test_get_message_length(self):
        """ Testing outbox message length class method """

        #
        # Default no compression coding
        #

        for msg, length in outbox_datasets.MESSAGE_LENGTH:
            self.assertEqual(
                Outbox.get_message_length(msg, Outbox.DEFAULT_NO_COMPRESSION),
                length
            )

        #
        # Unicode
        #

        # TODO(vojta)
