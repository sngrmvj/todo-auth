
# To Do Planner

- Authentication Server

### To Do planner
- Implemented two types of To-Do lists.
- One is normal to do list
- The other is to-do list that refreshes daily (unchecks the checked items in a particular day).
    - Basically daily routine items or things to be done are unchecked automatically at the start of the day.
    - So, user can check the items what he has completed in a particular day and automatically unchecks when the new day starts.
    - Mostly daily routines like Exercises, drink water etc.

#### Main Moto
- The main moto is to save the items of the person inside the database and retrieve them when ever it is necessary
- Authentication server
- For storing of the tasks another microservice is used developed in Java and uses Kafka.

#### Features
- Authentication server, a microservice to create user and login user and provide permissions.
- Password gets hashed before inserting into database. Can't be decrypted. 
    - When a user logins, the password is hashed and compared with the hashed password in the database.
- JWT Tokens 
    - Refresh Tokens which expires in 30 days
    - Access Tokens which expires in 5 minutes
    - Refresh tokens are used to fetch access tokens instead of user logging in again and again.
    - Tokens are stored in cookie and httpOnly set to True. Check Login API. 
        - In UI, the http call should contain options - {withCredentials: true, observe:"response"}
        - This sets the cookie directly in the browser without any set-cookie, get-cookie in UI.
- CRUD Operations for the user details.
- Password reset using the OTP.
- DB (Postgres DB only for the authentication server)
    - To store user creds
    - refresh tokens
    - blacklisted tokens
- Need to implement
    - Automate the django migrations
    - Sending Email
    - API gateway
    - Terraform Script
    - ELK stack (who, when, what for)



