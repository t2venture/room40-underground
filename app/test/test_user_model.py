import unittest
import datetime
import uuid
from app.main import db
from app.main.model.user import User
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            first_name='Test',
            last_name='McTestFace',
            username='testusername',
            email='example@gmail.com',
            public_id=str(uuid.uuid4()),
            password='test123',
            registered_on=datetime.datetime.utcnow(),
            created_by=1,
            modified_by=1,
            created_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime.utcnow(),
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))

    def test_decode_auth_token(self):
        user = User(
            first_name='Test',
            last_name='McTestFace',
            username='testusername',
            email='example@gmail.com',
            public_id=str(uuid.uuid4()),
            password='test123',
            registered_on=datetime.datetime.utcnow(),
            created_by=1,
            modified_by=1,
            created_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime.utcnow(),
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))
        self.assertTrue(User.decode_auth_token(auth_token) == user.id)


if __name__ == '__main__':
    unittest.main()