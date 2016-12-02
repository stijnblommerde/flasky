import unittest

from app import create_app, db
from app.models import User, Role, AnonymousUser, Permission


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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

    def test_roles_and_permissions(self):
        u = User(email='name@domain.com', password='password')
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.ADMINISTER))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
