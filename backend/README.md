# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### get categories

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

* Testing with curl
```bash
curl http://127.0.0.1:5000/categories
```

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```
### get questions
`GET '/questions'`
* Request arguements: None.
* Returns: An objects.
* curl test:
  ```bash
  curl http://127.0.0.1:5000/questions
  ```

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
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, ],
  "success": true,
}
```
### delete question
`DELETE 'question/${id}'`
* Request arguement: question id
* Removes object from database
* curl test:
```bash
curl -X DELETE http://127.0.01:5000/questions/21
```
```json
{
  "deleted": 21,
  "questions": [{
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
},],
  "success": true
}
```

### create question
`POST '/questions'`
* Request arguments: answer, category, difficulty and question
* Creates a new question,
* curl test:
```bash
curl -X POST -d '{"answer": "Nairobi", "difficulty": "1", "category": "2", "question": "What is the capital of Kenya?"}' -H "Content-Type: application/json" http://127.0.0.1:5000/questions
```

```json
{
  "created": 24,
  "success": true,
}
```
### Search question using term
`POST '/search'`

* Request arguments: search,
* Returns questions containing search term,
* curl test:
```bash
curl -X POST -d '{"search": "graphic"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/search 
```

```json
{
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

### Get questions in a category
`POST '/categories/${id}/questions'`
* Request arguments: category id,
* returns questions in a category,
* curl test:
```bash
curl http://127.0.0.1:5000/categories/1/questions
```

```json
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
  ], 
  "success": true, 
  "total_questions": 2
}
```
### Get quizzes
`POST '/quizzes'`
* Request argumnets: question category, previous questions,
* curl test:
```bash
curl -X POST -d '{"previous_questions":[], "quiz_category":{"id":"2", "type":"History"}}' -H 'Content-Type: application/json' http://127.0.0.1:5000/quizzes
```

```json
{
  "question": {
    "answer": "Escher", 
    "category": 2, 
    "difficulty": 1, 
    "id": 16, 
    "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
  }, 
  "success": true
}
```

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```