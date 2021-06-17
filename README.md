
# To Do Planner (APIs)

### To Do planner
- It has two types of to-do list.
- One is normal to do list
- The other is to-do list that refreshes daily (unchecks the checked items in a particular day).
    - Basically daily routine items or things to be done are unchecked automatically at the start of the day.
    - So, user can check the items what he has completed in a particular day and automatically unchecks when the new day starts.
    - Mostly daily routines like Exercises, drink water etc.

#### Main Moto
- The main moto is to save the items of the person inside the database and retrieve them when ever it is necessary

#### Features
- Token and token refreshing 
- MongoDb to store the items and postres to store the details of the person.
- Rest api framework for HTTP requests or try to implement messaging service.
- Implement Terraform script to deploy the app to the AWS or Azure etc.
