import os
import unittest
from flask_app import app, db, basedir, User
#from coverage import coverage



class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_user_email(self):
        ''' checks if user signed up with a valid email '''
        u = User(email='johndoe@gmail.com', password='admin')
        extension = u.email.split('@')[1]
        assert extension == 'gmail.com'
    
    def test_user_password_length(self):
        ''' checks if password is hashed '''
        u = User(email='johndoe@gmail.com', password='admin')
        password = u.password
        assert len(password) > 10

    def test_can_create_user(self):
        ''' tests if a user can be created '''
        u = User(email='john@example.com', password='password')
        db.session.add(u)
        db.session.commit()
        assert u.name == 'john'
    
    
    
    
    

if __name__ == '__main__':
    unittest.main()



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
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print "\n\nCoverage Report:\n"
    cov.report()
    print "HTML version: " + os.path.join(basedir, "tmp/coverage/index.html")
    cov.html_report(directory='tmp/coverage')
    cov.erase()