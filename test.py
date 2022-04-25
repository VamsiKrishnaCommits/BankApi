import json
from businesslayer import app
from databaselayer import db
import unittest
import contextlib
from sqlalchemy import MetaData

class FlaskTest(unittest.TestCase):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vamsi@localhost/testing'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = 'vamsi'
    db.init_app(app)




    def test_index(self):
        tester = app.test_client(self)
        response = tester.post('/create_user', json={'name':'vamsi','address':'hyd','phone':'123456*78*90'})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()