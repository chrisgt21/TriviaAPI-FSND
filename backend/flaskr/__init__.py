import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # Enable CORS for all origins
  CORS(app, resources={'/': {'origins': '*'}})

  # Set after request decorator
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  # Endpoint to handle GET requests for all available categories
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    _categories = {}
    for category in categories:
      _categories[category.id] = category.type

    if(len(_categories) == 0):
      abort(404)
    
    return jsonify({
      'success': True, 
      'categories': _categories
    })


  # Handles GET requests for /questions
  # Endpoint returns a list of questions, number of total questions, current category, categories
  @app.route('/questions')
  def get_questions():
    selection = Question.query.all()
    total_ques = len(selection)
    curr_ques = paginate_questions(request, selection)

    categories = Category.query.all()
    _categories = {}
    for category in categories:
      _categories[category.id] = category.type
    
    if (len(curr_ques) == 0):
        abort(404)

    return jsonify({
        'success': True,
        'questions': curr_ques,
        'total_questions': total_ques,
        'categories': _categories
    })


  # Removes the question from the database by specifying the id of the question in the request and method as delete
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
      try:
          question = Question.query.filter_by(id=id).one_or_none()
          if question is None:
              abort(404)
          question.delete()

          return jsonify({
              'success': True,
              'deleted': id
          })

      except:
          abort(422)


  # Endpoint to handle posting a new question 
  @app.route('/questions', methods=['POST'])
  def post_question():
    _obj = request.get_json()

    if('searchTerm' in _obj):
      searchTerm = _obj['searchTerm']
      print(_obj)
      selection = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()

      if(len(selection) == 0):
        abort(404)

      paginated = paginate_questions(request, selection)
      
      return jsonify({
          'success': True,
          'questions': paginated,
          'total_questions': len(Question.query.all())
      })

    else:
      print(_obj)
      if not ('question' in _obj or 'answer' in _obj or 'difficulty' in _obj or 'category' in _obj):
        abort(422)
      ques = _obj['question']
      answer = _obj['answer']
      diff = _obj['difficulty']
      category = _obj['category']

      if (ques == '' or answer == '' or diff == '' or category == ''):
        abort(422)

      try:
        question = Question(question=ques, answer=answer, difficulty=diff, category=category)
        question.insert()
        return jsonify({
          'success': True,
          'created': question.id
        })
      except:
        abort(422)

  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def questions_by_category(id):
    category = Category.query.filter_by(id=id).one_or_none()
    if(category is None):
      abort(404)

    try:
      questions = Question.query.filter(Question.category == str(id)).all()
      paginated = paginate_questions(request, questions)

      return jsonify({
        'success': True,
        'questions': paginated,
        'total_questions': len(questions),
        'current_category': id
      })
    except:
      abort(404)


  @app.route('/quizzes', methods=['POST'])
  def quiz():

    def get_question():
      new_ques = questions[random.randrange(0, total, 1)].format()
      #print(new_ques)
      return new_ques

    def check_ques(prev_ques, ques):
      used = False
      for z in prev_ques:
        if(z == ques['id']):
          used = True
      return used
    try:
      _obj = request.get_json()
      if ('quiz_category' in _obj):
        category = _obj['quiz_category']
        _id = category['id']
        prev_questions = _obj['previous_questions']

        if(_id == 0):
          questions = Question.query.all()
        else:
          questions = Question.query.filter_by(category=_id).all()

        total = len(questions)
        
        if total > 0:
          new_ques = get_question()
          while(check_ques(prev_questions, new_ques)):
            print("getting new question...")
            new_ques = get_question()

            if(len(prev_questions) == total):
              return jsonify({
                'success': True,
                'question': None
              })
        else:
          new_ques = None

        return jsonify({
          'success': True, 
          'question': new_ques
        })
      else:
        abort(400)
    except:
      abort(404)

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Not able to process"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad request"
      }), 400
  
  return app

    