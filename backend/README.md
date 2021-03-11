# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

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

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# Routes
All the routes recieve and respond JSON.

## ` /categories [GET] `
### Returns all the categories in the db.
*categories -> a list of all the categories in the database\
success -> it's either true or false to show whether the the process was successful or not*

example:
```
curl -X GET 127.0.0.1:5000/categories
```
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "success": true
}

```

## ` /categories/<int:category>/questions [GET] `
### Returns all the questions under this category.
*The route takes the id(int) of the category as a parameter and returns a list of all the questions under this category.*

example:
```
curl -X GET 127.0.0.1:5000/categories/1/questions
```
```
{
  "category": 1, 
  "length": 3, 
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
  "success": true
}

```

## ``` /questions?page=<integer> [GET] ```
### Returns 10 questions depending of the page number.
*The route takes `page` as an argument (it is set to 1 by a defualt if it is not supplied) and returns 10 questions based on the page number.*\
the response has:\
**length** -> the number of questions in the database.\
**questions** -> the 10 questions that have been sent.\
**success** -> either `true` or `false`.

example:
```
curl -X GET 127.0.0.1:5000/questions?page=2
```
```
{
  "length": 21, 
  "questions": [
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
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
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "this is an asnwer", 
      "category": 2, 
      "difficulty": 3, 
      "id": 24, 
      "question": "this is a question"
    }, 
    {
      "answer": "this is an asnwer", 
      "category": 2, 
      "difficulty": 3, 
      "id": 25, 
      "question": "this is a question"
    }, 
    {
      "answer": "this is an asnwer", 
      "category": 2, 
      "difficulty": 3, 
      "id": 26, 
      "question": "this is a question"
    }, 
    {
      "answer": "You", 
      "category": 4, 
      "difficulty": 1, 
      "id": 28, 
      "question": "Who is the most awesome perosn ever "
    }, 
    {
      "answer": "test answer", 
      "category": 2, 
      "difficulty": 5, 
      "id": 29, 
      "question": "test question"
    }
  ], 
  "success": true
}
```

## ``` /questions [POST] ```
### Adds a question to the databases
*To add a question you need to send a an onject on containing these: `question`[string], `answer`[string], `difficulty`[int], and `category`[int].*\
```
{
    'question': 'this is a question',
    'answer': 'this is an answer',
    'difficulty': 1,
    'category': 1
}
```
the response has:\
**length** -> the number of questions in the database.\
**question_added** -> Returns the question that the user submitted.\
**success** -> either `true` or `false`.

example:
```
curl -X POST -d '{"question":"this is a question","answer":"this is an asnwer","difficulty":3,"category":2}' -H 'Content-Type: application/json' 127.0.0.1:5000/questions

```
```
{
  "length": 23, 
  "question_added": {
    "answer": "this is an asnwer", 
    "category": 2, 
    "difficulty": 3, 
    "id": 32, 
    "question": "this is a question"
  }, 
  "success": true
}
```

## ``` /questions/<int:question_id> [DELETE] ```
### Deletes a question providing an id.
*It takes the id of the question ( `question_id` ) as a parameter and deletes that question.*\
the response has:\
**length** -> the number of questions in the database.\
**removed_id** -> The id of the removed question.\
**success** -> either `true` or `false`.

example:
```
curl -X DELETE 127.0.0.1:5000/questions/32
```
```
{
  "length": 23, 
  "removed_id": 32, 
  "success": true
}
```

## ``` /questions/search [POST] ```
### Searches for questions containing the search term you supply.
*send `searchTerm` as JSON and it will look for questions that contain that search term and return them.
```
{'searchTerm': 'boxer'}
```
response:\
**questions** -> the output of the search\
**length** -> the number of questions found for the search.\
**searchTerm** -> The search term sent.\
**success** -> either `true` or `false`.

example:
```
curl -X POST -d '{"searchTerm":"boxer"}' -H 'Content-Type: application/json' 127.0.0.1:5000/questions/search
```
```
{
  "length": 1, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ], 
  "searchTerm": "boxer", 
  "success": true
}
```

## ``` /quizzes [POST] ```
### returns questions for playing quizzes.
*It takes the quiz category id ( 0 means all categories ) and the previous questions that have been sent, and returns a new question under this category/categories that haven't been send before.
```
{
    'previous_questions': [],
    'quiz_category': {'type': 'click', 'id': 0} //this means all
}
```
response:\
**question** -> a question that hasn't beed asked previously \
**success** -> either `true` or `false`.

example:
```
curl -X POST -d '{"previous_questions":[],"quiz_category":{"type":"click","id":0}}' -H 'Content-Type: application/json' 127.0.0.1:5000/quizzes
```
```
{
  "question": {
    "answer": "this is an asnwer", 
    "category": 2, 
    "difficulty": 3, 
    "id": 24, 
    "question": "this is a question"
  }, 
  "success": true
}
```