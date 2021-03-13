import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format("mohamed_wafy", "1252002", 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # 1.1
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["categories"])

    # 2
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(True if data["questions"] == [] else data["questions"])  # empty list is allowed

    # 2.F
    def test_get_questions_fail(self):
        res = self.client().get('/questions?page=1000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"],False)

    # 3
    def test_delete_question(self):
        q = Question(question="test",answer="test",category=1,difficulty=1)
        db.session.add(q)
        db.session.commit()
        res = self.client().delete(f'/questions/{q.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["removed_id"])
        self.assertEqual(data["length"], len(Question.query.all()))

    # 3.F
    def test_delete_question_fail(self):
        res = self.client().delete('/questions/-1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"],False)

    # 4
    def test_add_question(self):
        res = self.client().post("questions", json={"answer":"test", "category":1, "difficulty":1, "question":"test"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["question_added"])
        self.assertTrue(data["length"])

    # 4.F
    def test_add_question_fail(self):
        res = self.client().post("questions", json={"category":1, "difficulty":1, "question":"test"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"],False)

    # 5
    def test_search_questions(self):
        res = self.client().post("/questions/search", json={ "searchTerm":"what" })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(True if data["questions"] == [] else data["questions"] ) #empty list is allowed
        self.assertTrue(True if data["questions"] == [] and data["length"] == 0 else data["length"])
        self.assertTrue(data["searchTerm"])

    # 6
    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(True if data["questions"] == [] else data["questions"] ) #empty list is allowed
        self.assertTrue(True if data["questions"] == [] and data["length"] == 0 else data["length"])
        self.assertTrue(data["category"])

    # 6.F
    def test_get_questions_by_category_fail(self):
        res = self.client().get("/categories/-1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"],False)

    # 7
    def test_send_quiz_question(self):
        res = self.client().post("/quizzes", json={"quiz_category": Category.query.get(1).format()})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"]) #empty list is allowed

    # 7.F
    def test_send_quiz_question_fail(self):
        res = self.client().post("/quizzes", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()