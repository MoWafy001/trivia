import os
from flask import Flask, request, abort, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category, db
from random import randint

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # allows users from any origin to any route
    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # GET all the categories  #1
    @app.route("/categories")
    def get_categories():
        try:
            res = {
                "success": True,
                "categories": [cat.format() for cat in Category.query.all()]
            }
            return jsonify(res)
        except:
            abort(500)

    # GET 10 questions based on the page number  #2
    @app.route("/questions")
    def get_questions():
        page = request.args.get("page", 1, type=int)
        if page < 1:  # incase somehow the input is negative or a zero
            page = 1
        start = (page-1)*10
        end = start + 10
        questions = Question.query.all()[start:end]

        if len(questions) == 0:
            abort(404)

        questions = [q.format() for q in questions]

        data = {
            "success": True,
            "questions": questions,
            "length": len(Question.query.all())
            # shows how many questions are there in the db
        }
        return jsonify(data)

    # DELETE question  #3
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            db.session.delete(Question.query.get(question_id))
            db.session.commit()
            res = {
                "success": True,
                "length": len(Question.query.all()),  # how many questions left
                "removed_id": question_id
            }
            return jsonify(res)
        except:
            db.session.rollback()
            abort(404)

    # POST question  #4
    @app.route("/questions", methods=["POST"])
    def add_question():
        data = request.json
        try:
            # making sure no property is missing
            if (
                data["answer"] is None or
                data["category"] is None or
                data["difficulty"] is None or
                data["question"] is None
               ):
                abort(422)

            q = Question(
                question=data["question"],
                answer=data["answer"],
                category=data["category"],
                difficulty=data["difficulty"]
            )
            db.session.add(q)
            db.session.commit()
            return jsonify({
                "success": True,
                "length": len(Question.query.all()),
                "question_added": q.format()
                # showing what question had been added
            })
        except:
            db.session.rollback()
            abort(422)

    # POST search for questions  #5
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        try:
            # If there isn't a search phrase this will output all the questions
            searchTerm = request.json.get("searchTerm", "")
            questions = Question.query.filter(
              Question.question.ilike(f"%{searchTerm}%") |
              Question.answer.ilike(f"%{searchTerm}%")).all()
            questions = [q.format() for q in questions]
        except:
            abort(500)

        data = {
            "success": True,
            "questions": questions,
            "searchTerm": searchTerm,
            "length": len(questions)
        }

        return jsonify(data)

    # GET questions under a category  #6
    @app.route("/categories/<int:category>/questions")
    def get_questions_by_category(category):
        try:
            questions = Question.query.filter_by(category=category)
            questions = [q.format() for q in questions]
        except:
            abort(404)

        data = {
            "success": True,
            "questions": questions,
            "category": category,
            "length": len(questions)
        }

        return jsonify(data)

    # Returns question for the QUIZ feature according to the API request.  #7
    @app.route("/quizzes", methods=["POST"])
    def send_quiz_question():
        try:
            previous_questions = request.json.get("previous_questions", [])
            quiz_category = request.json.get("quiz_category")["id"]
        except:
            abort(422)
        if quiz_category != 0:
            question = list(filter(lambda x: x.id not in previous_questions,
                                   Question.query.filter_by(
                                     category=quiz_category
                                     )))
        else:
            question = list(filter(lambda x: x.id not in previous_questions,
                                   Question.query.all()))
        if len(question) != 0:
            question = question[randint(0, len(question)-1)]
        else:
            question = None

        data = {
            "success": True,
            "question": question.format() if question is not None else None
        }

        return jsonify(data)

    # error handlers
    @app.errorhandler(404)
    def not_found_error(e):
        res = {
            "success": False,
            "error": "NOT FOUND"
        }
        return jsonify(res), 404

    @app.errorhandler(422)
    def bad_entry_error(e):
        res = {
            "success": False,
            "error": "BAD ENTRY"
        }
        return jsonify(res), 422

    @app.errorhandler(500)
    def internal_server_error(e):
        res = {
            "success": False,
            "error": "INTERNAL SERVER ERROR"
        }
        return jsonify(res), 500

    return app
