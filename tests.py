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
    
    def test_index(self):
        """initial test. ensure flask was set up correctly"""
        tester = app.test_client(self)
        response = tester.get('/api/v1/posts', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data),type('qwerty'))
    
    def test_database(self):
        """initial test. ensure that the database exists"""
        tester = os.path.exists("blog.sqlite")
        self.assertEqual(tester, True)

if __name__ == '__main__':
    unittest.main()