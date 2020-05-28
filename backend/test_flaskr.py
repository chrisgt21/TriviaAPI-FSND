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
        self._objbase_name = "trivia_test"
        self._objbase_path = "postgres://{}/{}".format(
            'localhost:5432', self._objbase_name)
        setup_db(self.app, self._objbase_path)


        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Tests pagination successfully
    def test_get_paginated_questions(self):

        response = self.client().get('/questions')
        _obj = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(_obj['success'], True)
        self.assertTrue(_obj['total_questions'])
        self.assertTrue(len(_obj['questions']))

    # Test pagination failure - 404 exptected
    def test_pagination_failure_404(self):
        response = self.client().get('/questions?page=100')
        _obj = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(_obj['success'], False)
        self.assertEqual(_obj['message'], 'Resource not found')

    # Test for deleting a question
    def test_delete_question(self):
        new_question = {
            'question': 'In the 2005-06 season, who wore the number 4 on the Duke Basketball team?',
            'answer': 'J.J. Redick',
            'difficulty': 4,
            'category': '6'
        }
        question = Question(question=new_question['question'], answer=new_question['answer'],
                            category=new_question['category'], difficulty=new_question['difficulty'])
        question.insert()
        ques_id = question.id
        prev_ques = Question.query.all()
        response = self.client().delete('/questions/{}'.format(ques_id))

        _obj = json.loads(response.data)
        curr_ques = Question.query.all()
        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(_obj['success'], True)

        self.assertEqual(_obj['deleted'], ques_id)

        self.assertTrue(len(prev_ques) - len(curr_ques) == 1)

        self.assertEqual(question, None)

    def test_create_new_question(self):
        """Tests question creation success"""

        new_question = {
            'question': 'In the 2005-06 season, who wore the number 4 on the Duke Basketball team?',
            'answer': 'J.J. Redick',
            'difficulty': 4,
            'category': '6'
        }

        prev_ques = Question.query.all()

        response = self.client().post('/questions', json=new_question)
        _obj = json.loads(response.data)

        curr_ques = Question.query.all()

        question = Question.query.filter_by(id=_obj['created']).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(_obj['success'], True)
        self.assertTrue(len(curr_ques) - len(prev_ques) == 1)

        self.assertIsNotNone(question)

    # Tests question creation - fail 422
    def test_create_fail_422(self):

        prev_ques = Question.query.all()

        response = self.client().post('/questions', json={})
        _obj = json.loads(response.data)

        curr_ques = Question.query.all()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(_obj['success'], False)

        self.assertTrue(len(curr_ques) == len(prev_ques))

    # Test search questions - succeed 200
    def test_search_questions(self):

        response = self.client().post('/questions',
                                      json={'searchTerm': 'bird'})

        _obj = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(_obj['success'], True)

        self.assertEqual(len(_obj['questions']), 1)

        self.assertEqual(_obj['questions'][0]['id'], 5)

    # Test search questions - fail 404
    def test_search_question_fail_404(self):

        response = self.client().post('/questions', json={'searchTerm': 'ghjkfyuyuit7y'})

        _obj = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(_obj['success'], False)
        self.assertEqual(_obj['message'], 'Resource not found')

    # Test get questions by category - succeed 200
    def test_get_questions_by_category(self):

        response = self.client().get('/categories/1/questions')
        _obj = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(_obj['success'], True)
        self.assertTrue(len(_obj['questions']))
        self.assertTrue(_obj['total_questions'])
        self.assertTrue(_obj['current_category'])

    # Test play quiz - succeed 200
    def test_play_quiz_game(self):


        response = self.client().post('/quizzes',json={'previous_questions': [13, 14],'quiz_category': {'type': 'Geography', 'id': '3'}})

        _obj = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(_obj['success'], True)

        self.assertTrue(_obj['question'])

        self.assertEqual(_obj['question']['category'], 3)

        self.assertNotEqual(_obj['question']['id'], 13)
        self.assertNotEqual(_obj['question']['id'], 14)

    # Test play quiz - fail 404
    def test_play_quiz_fail_404(self):

        response = self.client().post('/quizzes', json={})

        _obj = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(_obj['success'], False)
        self.assertEqual(_obj['message'], 'Resource not found')


if __name__ == "__main__":
    unittest.main()