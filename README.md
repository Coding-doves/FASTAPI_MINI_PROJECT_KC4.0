# FASTAPI MINI-PROJECT
___
 
### OBJECTIVE:
To assess your understanding of fundamental FastAPI concepts and your ability to build a basic API application.

### TASK DESCRIPTION:
___
You are required to build a simple CRUD (Create, Read, Update, Delete) API for managing a collection of books. The API should allow users to perform the following operations:

- Create a new book: Users should be able to add a new book to the collection by providing details such as title, author, publication year, and genre.
- Retrieve a list of all books: Users should be able to retrieve a list of all books in the collection.
- Retrieve details of a specific book: Users should be able to retrieve details of a specific book by providing its unique identifier (ID).
- Update details of a book: Users should be able to update details of a specific book by providing its unique identifier (ID) and the updated information.
- Delete a book: Users should be able to delete a specific book from the collection by providing its unique identifier (ID).
 
## REQUIREMENTS:
Use FastAPI framework to build the API.
Persist data in-memory (e.g., using lists or dictionaries)

### USAGE
- clone repo
`git clone https://github.com/Coding-doves/FASTAPI_MINI_PROJECT_KC4.0.git`
- Navigate into directory
`cd FASTAPI_MINI_PROJECT_KC4.0`
- Activate environment
`venv\Script\activate`
- Point to FastAPI Python Interpreter (using VScode)
    - `Ctrl + Shift + p`
    - Type `interperter`
    - Select `python interpreter`
    - Select `Enter interpreter path`
    - Select `venv` folder
    - Select `Script` folder
    - Select `Python` interpreter
- Run
`uvicorn app:app --reload`
