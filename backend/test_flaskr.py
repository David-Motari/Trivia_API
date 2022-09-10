import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('david','2834Obegi','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {"answer":"Nairobi","category":"2","difficulty":"1","question":"What is the capital of Kenya?"}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    """Test for pagination"""


    """Tests for get_questions success"""
    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    """Test for get questions failure"""
    def test_get_questions_failure(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    """Test for delete_question success"""
    def test_delete_success(self):
        """Test _____________ """
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)
    
    """Test for delete question failure"""
    def test_delete_failure(self):
        """Test _____________ """
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')    

    """Test for create question success"""
    def test_create_success(self):
        """Test _____________ """
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
    
    """test for create question failure."""
    def test_create_failure(self):
        """Test _____________ """
        res = self.client().post('/questions/50', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    """ Test search_question success"""
    def test_search_success(self):
        """test ______________ """
        res = self.client().post('/search', json={'search': 'graphic'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    """test for search question failure"""
    def test_search_noResult(self):
        res = self.client().post('/search', json={'search': '100'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """Test get category questions success"""
    def test_get_category_questions_success(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['total_questions'])

    """Test for get category questions failure"""
    def test_get_category_questions_failure(self):
        res = self.client().get('/categories/1080p/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """Test Trivia Quizzes success"""
    def test_trivia_quiz_success(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [], 'quiz_category': {'type': "Geography", 'id': '3'}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """Test Trivia Quizzes failure"""
    def test_trivia_quiz_success(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()