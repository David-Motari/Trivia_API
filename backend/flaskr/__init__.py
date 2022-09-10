import json
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginated_questions(request, selection):
	page = request.args.get('page', 1, type=int)
	start = (page - 1) * QUESTIONS_PER_PAGE
	end = start + QUESTIONS_PER_PAGE
    	
	books = [book.format() for book in selection]
	current_books = books[start:end]
    	
	return current_books

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    CORS. Allow '*' for origins.
    """
    CORS(app)
    # cors = CORS(app, resources={r"*/api/*": {"origins": "*"}})
    """
    after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,PATCH,DELETE,OPTIONS"
        )
        return response

    @app.route('/categories')
    def getAllCategories():
        """
        This endpoint handles GET requests for categories
        """
        cats = Category.query.all()
        if cats is None:
            abort(404)
        else:
            dict_cats = {}
            for category in cats:
                dict_cats[category.id] = category.type
            return jsonify({
                'success': True,
                'categories': dict_cats,
            })

    @app.route('/questions')
    def getAllQuestions():

        """
        This end point handles GET requests for questions.
        Pagination (10 questions per page) and
        Return:
            - list of questions
            - Number of total questions,
            - Current category,
            - and categories        
        """
        try:
            cats = Category.query.all()
            dict_cats = {}
            for category in cats:
                dict_cats[category.id] = category.type

            quests = Question.query.order_by(Question.id).all()
            current_quests = paginated_questions(request, quests)

            if len(current_quests) == 0:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'questions': current_quests,
                    'total_questions': len(Question.query.all()),
                    'categories': dict_cats,
                    'total_categories': len(cats)
                })
        except:
            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def deleteQuestion(question_id):
        """
        This endpoint handles DELETE request on questions.
        Args:
            - question id.
        """
        try:
            quest = Question.query.filter(Question.id == question_id).one_or_none()
            if quest is None:
                abort(404)
            quest.delete()

            quests = Question.query.order_by(Question.id).all()
            current_quests = paginated_questions(request, quests)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_quests,
                'total_questions': len(Question.query.all()),
            })

        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def createQuestion():
        """
        This endpoint handles POST requests and creates new question
        """
        body = request.get_json()

        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        new_question = body.get('question', None)

        try:
            question = Question(
                answer=new_answer, category=new_category,
                difficulty=new_difficulty, question=new_question
                )
            question.insert()

            quests = Question.query.order_by(Question.id).all()
            current_quests = paginated_questions(request, quests)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_quests,
                'total_questions': len(Question.query.all()),
            })
        except:
            abort(422)

    @app.route('/search', methods=['POST'])
    def questionSearch():
        """
        This endpoint handles POST requests for search using a term.
        Return: 
            - Question(s) with search term as substring 
        """
        body = request.get_json()
        term2_search = body.get('search', None)
        srched_quests = Question.query.filter(Question.question.ilike(f'%{term2_search}%')).all()
        paged_quests = paginated_questions(request, srched_quests)
        
        if paged_quests != None:
            return jsonify({
                'success': True,
                'total_questions': len(srched_quests),
                'questions': paged_quests,
            })
        else:
            abort(404) 

    @app.route('/categories/<int:category_id>/questions')
    def questionsPerCategory(category_id):
        """
        This endpoint handles GET requests for questions in a category.
        Arg:
            - category id.
        Returns:
            - questions in a category.
        """
        try:
            cat_quests = Question.query.filter(category_id == Question.category).all()
            paged_quests = paginated_questions(request, cat_quests)
            cat = Category.query.filter(category_id==Category.id).one_or_none()
            if cat:
                return jsonify({
                    'success': True,
                    'questions': paged_quests,
                    'total_questions': len(cat_quests),
                    'current_category': cat.type,
                })
        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def triviaQuiz():
        """
        This endpoint handles POST request to play a quiz.
        params:
            - categories,
            - Previous questions.
        return:
            - random questions within a category
        """
        try:    
            body = request.get_json()
            quiz_cat = body.get('quiz_category', None)
            prev_quests = body.get('previous_questions', None)
            cat_id = quiz_cat.get('id')

            if cat_id == 0:
                quests = Question.query.filter(Question.id.notin_(prev_quests)).all()
            else:
                quests = Question.query.filter(Question.category == cat_id).filter(Question.id.notin_(prev_quests)).all()
            if quests:
                quest = random.choice(quests)
            return jsonify({
                'success': True,
                'question': quest.format(),
            })
        except:
            abort(422)
    """
    Handling errors
    """
    @app.errorhandler(404)
    def not_found(error):
        """
        Handles resource not found error
        """
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found',
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        """
        Handles unprocessable error
        """
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable',
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        """
        Handles method not allowed error
        """
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed',
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        """
        Handles bad request error
        """
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request',
        }), 400

    return app
