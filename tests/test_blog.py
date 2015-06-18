import unittest
from flask_app import app
from coverage import coverage

cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()


class BasicTestCase(unittest.TestCase):
    """Tests to be carried out for the following api calls
        0: '/api/v1/users'
        1: '/api/v1/sessions'
        2: '/api/v1/posts'
        3: '/api/v1/posts/<int:id>'
    """


    def test_index(self):
        """initial test. ensure flask was set up correctly"""
        tester = app.test_client(self)
        response = tester.get('/api/v1/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "{msg:'Hello, World!'}")
    
    def test_database(self):
        """initial test. ensure that the database exists"""
        tester = os.path.exists("flaskr.db")
        self.assertEqual(tester, True)

class PostTestCase(unittest.TestCase):
    
    def test_post(self):
        tester = app.test_client(self)
        response = tester.get('/hello_world', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "{msg:'Hello, World!', comments:[{id:1,text:'one',author:'John Doe',date:'12-11-10'}]'}")

    def setUp(self):
        """Set up a blank temp database before each test"""
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def login(self, username, password):
        """Login helper function"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/logout', follow_redirects=True)

    # assert functions

    def test_empty_db(self):
        """Ensure database is blank"""
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_login_logout(self):
        """Test login and logout using helper functions"""
        rv = self.login(app.app.config['USERNAME'],app.app.config['PASSWORD'])
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login(app.app.config['USERNAME'] + 'x',app.app.config['PASSWORD'])
        assert b'Invalid username' in rv.data
        rv = self.login(app.app.config['USERNAME'],app.app.config['PASSWORD'] + 'x')
        assert b'Invalid password' in rv.data

    def test_messages(self):
        """Ensure that user can post messages"""
        self.login(app.app.config['USERNAME'],app.app.config['PASSWORD'])
        rv = self.app.post('/post/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
            ))
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data

        """Ensure that user can delete messages"""
        rv = self.app.delete('/post/1/delete')



if __name__ == '__main__':
    unittest.main()