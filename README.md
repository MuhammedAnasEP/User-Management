# User Management API

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MuhammedAnasEP/User-Management.git
   cd User-Management
   
2. Create a virtual environment and activate it:

   ```bash
     python -m venv venv Or virtualenv venv
     source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

3. Install dependencies:

   ```bash
     pip install -r requirements.txt

4. Connect Database:
   
     I used PostgresSQL for database,
     if your using same you can change username, name, password from settings DATABASES section.
     Or you want to connect with other engines like sqlite, MySQL etc. You want to change the engine section also.
     The sqlite connection code is commented in my setting file.

5. Run migrations:
 
   ```bash
    python manage.py makemigrations
    python manage.py migrate

6. Populate the database with sample data:
   ```bash
    python manage.py populate_users

7. Resync Sequances:

     Note:You need to change 'pg_get_serial_sequence' code in resync_sequences.py file if your not using PostgresSQL
         After the populate_users the id not auto incremented that why i created this command to resync the squance.

   ```bash
     python manage.py resync_sequences

8. Test Project (Optional):

   ```bash
    python manage.py test
  
9. Run the server:
    
   ```bash
    python manage.py runserver

## API Endpoints

  None: I used JWT Authentication in all users end point for secruty. And The token is stored in the HTTPOnly Cookie.Use Postman for the checking the api it will or other
        platforms. And send Token with every request.

  ### For users
    GET /api/users: List users with optional query parameters (page, limit, name, sort)
    POST /api/users: Create a new user
    GET /api/users/{id}: Get details of a user by ID
    PUT /api/users/{id}: Update details of a user by ID
    DELETE /api/users/{id}: Delete a user by ID

  ### For Authentication
    POST /api/auth/register: Register user for authentication
    POST /api/auth/login: Login user get token and store token to the cookies
    POST /api/auth/logout: Logout user and remove token from the cookies
    POST /api/auth/refresh-token: Create new token
    GET /api/auth/user: for fetch the data of current logined user
  

- Example Request:
  
   GET /api/users?page=1&limit=10&name=James&sort=-age

- Response:
   ```
   {
       "count": 1,
       "next": null,
       "previous": null,
       "results": [
           {
               "id": 507,
               "first_name": "James",
               "last_name": "Butt",
               "company_name": "Benton, John B Jr",
               "age": 70,
               "city": "New Orleans",
               "state": "LA",
               "zip": 70116,
               "email": "jbutt@gmail.com",
               "web": "http://www.bentonjohnbjr.com"
           }
       ]
   }
