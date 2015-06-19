import os
import unittest
import tempfile
from flask_app import app, db, basedir
from flask_app import User


class TestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_user_email(self):
        ''' checks if user signed up with a valid email '''
        u = User(email='johndoe@gmail.com', password='admin')
        assert '@' in u.email
    
    def test_user_password_is_hashed(self):
        ''' checks if password is hashed '''
        u = User(email='johndoe@gmail.com', password='admin')
        password = u.password
        assert len(password) > 50
    

if __name__ == '__main__':
    unittest.main()