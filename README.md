
# To Do Tasks

### Introduction
To do tasks is normal to do lists with extra feature of tasks getting refreshed everyday i.e even after you tick off a task it gets unticked next day. The main advantage is it helps you keep track of the daily mandatory tasks and keep you aware of what is completed each day. This comes under daily tasks section. There is one more section called general tasks section which is similar to normal to do checklist.

---

#### Features
- Application is a role based application. Admins can manage the users and grant admin access. Admins can see the feedback given by the users as well.
- Two sections are present in To Do tasks
    - Daily Tasks (gets refreshed everyday)
    - General Tasks
- Tasks can be checked/ticked and unchecked/unticked.
- We can delete the tasks from ticked and unticked as well.
    - Note: Tasks under daily tasks should be deleted if you don't want a task to be refreshed again next day.

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
    - As said, application is role based application. It takes care of admin's and user's details and issues tokens.
    - Passwords safeguarding - 
        - Passwords are not stored in plain text. Password obtained during account creation is encrypted using hashing and the result is saved in DB.
        - When user logins, the entered password is hashed and verified using the hashed password from DB.
    - JWT Tokens 
        - Once the user logins, server sets two httponly cookies. One is for refresh token (lasts for 90 days) and access token (lasts for 10 minutes)
        - Using the refresh token we get the access token for accessing the tasks.
        - we blacklist tokens if there is any error or expiration of refresh token and makes sure no one used that refresh token to get access token.
    - CRUD operations are available for users and admins.
    - DB (Postgres DB only for the authentication server)
        - To store user creds
        - refresh tokens
        - blacklisted tokens
        - User details are stored with roles. 
        - Admins can make users admins.
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


---

#### Repo Links
- Lists of Tasks (todo-lists)
    - > https://github.com/sngrmvj/todo-lists
- User Interface (todo-ui)
    - > https://github.com/sngrmvj/todo-ui


