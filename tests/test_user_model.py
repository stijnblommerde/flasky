import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):

    def test_password_setter(self):
        stijn = User(password='Kobus1hs')
        self.assertTrue(stijn.password_hash is not None)

    def test_no_password_getter(self):
        stijn = User(password='Kobus1hs')
        with self.assertRaises(AttributeError):
            stijn.password

        # more verbose version
        # try:
        #     stijn.password
        # except AttributeError:
        #     self.assertRaises(AttributeError)

    def test_password_verification(self):
        stijn = User(password='Kobus1hs')
        self.assertTrue(stijn.verify_password('Kobus1hs'))
        self.assertFalse(stijn.verify_password('x'))

    def test_salts_are_random(self):
        stijn = User(password='Kobus1hs')
        casper = User(password='Kobus1hs')
        self.assertTrue(stijn.password_hash != casper.password_hash)