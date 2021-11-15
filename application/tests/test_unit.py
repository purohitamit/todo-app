from flask_testing import TestCase
from application import app, db
from flask import url_for
from application.models import Tasks


class TestBase(TestCase):

    def create_app(self):
        # Defines the flask object's configuration for the unit tests
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///',
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self):
        # Will be called before every test
        # Create table schema
        db.create_all()
        db.session.add(Tasks(description="Run unit test"))
        db.session.commit()


    def tearDown(self):
        # Will be called after every test
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    # To test whether we got successful result form our route
    def test_home_get(self):
        response = self.client.get(url_for("home"))
        self.assert200(response)

    def test_create_task_get(self):
        response = self.client.get(url_for("create_task"))
        self.assert200(response)
    
    def test_read_task_get(self):
        response = self.client.get(url_for("read_tasks"))
        self.assert200(response)
    
    def test_update_task_get(self):
        response = self.client.get(url_for("update_task", id=1))
        self.assert200(response)
    
    
class TestRead(TestBase):
    def test_read_home_task(self):
        response = self.client.get(url_for("home"))
        self.assertIn(b"Run unit test", response.data)

    def test_read_task_dictionary(self):
        response = self.client.get(url_for("read_tasks"))
        self.assertIn(b"Run unit test", response.data)

class TestCreate(TestBase):
    def test_create_task(self):
        response = self.client.post(
            url_for("create_task"),
            data ={"description": "Testing create functionality"},
            follow_redirects=True
        )
        self.assertIn(b"Testing create functionality", response.data)

class TestUpdate(TestBase):
    def test_update_task(self):
        response = self.client.post(
            url_for("update_task", id=1),
            data ={"description": "Testing update functionality"},
            follow_redirects=True
        )
        self.assertIn(b"Testing update functionality", response.data)

class TestDelete(TestBase):
    def test_delete_task(self):
        response = self.client.get(url_for("delete_task", id=1), follow_redirects=True)
        self.assertNotIn(b"Run unit test", response.data)
