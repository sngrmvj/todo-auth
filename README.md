
# To Do Tasks

### Introduction
A To-Do checklist application, mainly for daily tasks which gets refreshed every day. You can tick off a task that gets unticked the next morning. This is useful when you have to do mandatory tasks or work that repeats every day which keeps you on track. The application also has another section called the general tasks section which is a normal checklist (won’t get refreshed).

---

#### Features
- Application is role-based application admins and users.
    - Admins have privilege access to managing the users and grant admin access.
    - Admins can see the feedback given by the users.
- Two sections are present in To-Do tasks
    - Daily Tasks (gets refreshed everyday)
    - General Tasks
- Tasks can be ticked off and unticked.
- Tasks can be deleted irrespective of ticked or unticked.
    - Note: Tasks under the daily tasks section should be deleted if you don't want a task to be refreshed again the next day.

---

#### Technical Features
- Application is divided into three microservices
    - todo-lists 
        - Maintains the tasks of the users and admins
    - todo-auth (current one)
        - Authentication server (More info check the repo)
    - todo-ui
        - User Interface (More info check the repo)
- Authentication server (current service)
    - Application is built using the Django framework of Python and DB is Postgres.
    - It takes care of admin's and user's details and issues tokens.
    - Passwords safeguarding - 
        - Passwords are not stored in plain text. Password obtained during account creation is encrypted using hashing and the result is saved in DB.
        - When user logins, the entered password is hashed and verified using the hashed password from DB.
    - JWT Tokens 
        - Once the user logins, the server sets two httponly cookies in the browser using the HTTP response of the Login API.
            - One is for refresh token (lasts for 90 days) and access token (lasts for 10 minutes)
        - Using the refresh token we get the access token (if it expires) for accessing the tasks rather than asking the user to log in again (Token refreshing).
        - We blacklist tokens if there is any error or expiration of refresh token and makes sure no one use that refreshes token to get access token.
    - CRUD operations are available for users and admins.
    - DB (Postgres DB only for the authentication server)
        - To store user credentials.
            - User details are stored with roles.
            - Admins can make users admins.
        - To store refresh tokens
        - To store blacklisted tokens
    - Secrets are provided as environmental variables.
    - Note 
        - For very first admin, we need to make them admin manually in DB
        - From next, we can make others admin by logging into the admins acount -> My Profile -> (List of users) -> (Select user) -> Click on make admin.
- Environment Variables to be provided before you run the application. (Either in dockerfile or docker-compose.yml)
    - SECRET_KEY
    - DATABASE_NAME
    - DATABASE_USER
    - DATABASE_PASSWORD
    - DATABASE_HOST
    - DATABASE_PORT
- Local setup 
  - Install python.
  - `pip install -r requirements.txt`.
  - `python manage.py runserver`.
        - If you want it run on different port, please specify at the end of the command `0.0.0.0:(port)`.
        - Add that in the User Interface.


---

#### Repo Links
- Lists of Tasks (todo-lists)
    - > https://github.com/sngrmvj/todo-lists
- User Interface (todo-ui)
    - > https://github.com/sngrmvj/todo-ui


