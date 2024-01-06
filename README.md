# Secure and Scalable RESTful API for Notes Management

## Project Overview

You have been tasked with building a secure and scalable RESTful API to manage notes. This API enables users to perform CRUD operations on notes, share them with others, and search based on keywords. The project is implemented using Django Rest Framework, incorporating features such as secure authentication, rate limiting, and search functionality.

## Technical Details

### Framework: Django Rest Framework

Django Rest Framework (DRF) is chosen for its robust and flexible toolkit to build Web APIs. It provides serialization, authentication, permissions, and other essential components out of the box, making it an excellent choice for rapid development.

### Database: PostgreSQL

PostgreSQL is selected as the database to store notes data. It offers ACID compliance, extensibility, and support for complex queries, making it suitable for the requirements of this project.

### Rate Limiting: django-ratelimiting

To handle high traffic and prevent abuse, the django-ratelimiting package is employed. This tool allows for easy implementation of rate limiting and request throttling, ensuring the API remains responsive and secure.

### Authentication: Session-Based JWT

For security, the project utilizes a session-based JWT (JSON Web Token) authentication mechanism. This approach combines the benefits of JWTs for stateless authentication with session-based management for added security.

### Search Functionality: Text Indexing

To enhance search performance, text indexing is implemented. This feature enables users to search for notes based on keywords efficiently.

## API Endpoints

### Authentication Endpoints

- POST /api/auth/signup: Create a new user account.
- POST /api/auth/login: Log in to an existing user account and receive an access token.

### Note Endpoints

## Authentication endpoints:
- POST /api/auth/signup: create a new user account.
- POST /api/auth/login :g in to an existing user account and receive an access token
## Notes Endpoints
- GET /api/notes/: Get a list of all notes for the authenticated user.
- GET /api/notes/create/ : Create a new note for the authenticated user.
- POST /api/notes/<int:pk>/: Get a note by ID for the authenticated user.
- PUT /api/notes/<int:pk>/update/ : Update an existing note by ID for the authenticated user.
- DELETE /api/notes/<int:pk>/delete/ : Delete a note by ID for the authenticated user.
- POST /api/notes/<int:pk>/share: Share a note with another user for the authenticated user using user id.
- GET /api/search?q=:query: Search for notes based on keywords for the authenticated user.

## additional endpoints for user profile
api/profile/
api/profile/update/

## How to Run the Code and Tests

1. Clone the repository: git clone https://github.com/chiragbiradar/speer.io_backend_assesment.git
2. Install dependencies: pip install -r requirements.txt
3. Apply migrations: python manage.py migrate
4. Run the development server: python manage.py runserver
5. Execute tests: cd NotesApp python manage.py test
