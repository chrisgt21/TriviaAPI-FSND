
# Trivia API
Trivia api is a web application that allows people to hold trivia on a regular basis using a webpage to manage the trivia app and play the game.

The app allows one to: 

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended.

#### PIP Dependencies

navigate to the `/backend` directory and run:

```bash
pip install -r requirements.txt
```

This will install all of the required packages in the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Getting Started

* Backend URL: `http://127.0.0.1:5000/`

### Error Handling

Here is a list of the error codes returned:

* 400 – Bad request
* 404 – Resource not found
* 422 – Unprocessable
* 500 – Internal server error

Example of error message:

```json
      {
        "success": "False",
        "error": 404,
        "message": "Resource not found",
      }
```


### Endpoints

#### GET /categories
##### Returns all categories

- Example:  `curl http://127.0.0.1:5000/categories`

```json
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "success": true
    }
```

#### GET /questions
##### Returns all paginated questions

- Example: `curl http://127.0.0.1:5000/questions`

```json
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "questions": [
            {
                "answer": "Maya Angelou", 
                "category": 4, 
                "difficulty": 2, 
                "id": 5, 
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            }, 
            {
                "answer": "Muhammad Ali", 
                "category": 4, 
                "difficulty": 1, 
                "id": 9, 
                "question": "What boxer's original name is Cassius Clay?"
            }, 
            {
                "answer": "Apollo 13", 
                "category": 5, 
                "difficulty": 4, 
                "id": 2, 
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            }, 
            {
                "answer": "Tom Cruise", 
                "category": 5, 
                "difficulty": 4, 
                "id": 4, 
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }, 
            {
                "answer": "Edward Scissorhands", 
                "category": 5, 
                "difficulty": 3, 
                "id": 6, 
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }, 
            {
                "answer": "Brazil", 
                "category": 6, 
                "difficulty": 3, 
                "id": 10, 
                "question": "Which is the only team to play in every soccer World Cup tournament?"
            }, 
            {
                "answer": "Uruguay", 
                "category": 6, 
                "difficulty": 4, 
                "id": 11, 
                "question": "Which country won the first ever soccer World Cup in 1930?"
            }, 
            {
                "answer": "George Washington Carver", 
                "category": 4, 
                "difficulty": 2, 
                "id": 12, 
                "question": "Who invented Peanut Butter?"
            }, 
            {
                "answer": "Lake Victoria", 
                "category": 3, 
                "difficulty": 2, 
                "id": 13, 
                "question": "What is the largest lake in Africa?"
            }, 
            {
                "answer": "The Palace of Versailles", 
                "category": 3, 
                "difficulty": 3, 
                "id": 14, 
                "question": "In which royal palace would you find the Hall of Mirrors?"
            }
        ], 
        "success": true, 
        "total_questions": 19
    }
```

#### DELETE /questions/<int:id\>
##### Deletes a question by specifying the id

- Example: `curl http://127.0.0.1:5000/questions/26 -X DELETE`

```json
{
    "success": true,
    "deleted": 26
}
```

#### POST /quizzes
##### Play quiz game by choosing category

- Example: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [],"quiz_category": {"type": "History", "id": "6"}}`

```json
{
  "question": {
    "answer": "Uruguay", 
    "category": 6, 
    "difficulty": 4, 
    "id": 11, 
    "question": "Which country won the first ever soccer World Cup in 1930?"
  }, 
  "success": true
}
```

#### POST /questions
##### Creates a new question by passing a json object

- Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            "question": "Duke hit its highest scoring mark with a score of 136 vs. Virginia in which year?",
            "answer": "1965",
            "difficulty": 4,
            "category": "6"
        }'`

```json
{
    "created": 27,
    "success": true
}
```

#### POST /questions
##### Search for keywords in questions

- Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Duke"}'`

```json
{
  "questions": [
    {
      "answer": "1965", 
      "category": 6, 
      "difficulty": 4, 
      "id": 27, 
      "question": "Duke hit its highest scoring mark with a score of 136 vs. Virginia in which year?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}
```

#### GET /categories/<int:id\>/questions
##### Gets questions by category using by passing the id of the category
- Example: `curl http://127.0.0.1:5000/categories/1/questions`

```json
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}

```


