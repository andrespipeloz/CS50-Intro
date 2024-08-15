# TASK Management
#### Video Demo:  <URL https://www.youtube.com/watch?v=cm1u0Re98WE>
#### Description:
##### Introduction:
This project is  web-based task management dashboard that allows users to create and edite tasks with this fields: name, ID, progress, created date, progress, completed, priority and department. It provides visual representations of task progress and priority using bar charts and it also allow to filter the tasks by this items. The application requires users to log in, ensuring that each user can manage their own tasks securely. It provides also the possibility to change password.

##### Features:
- User authentication (registration, login, logout)
- Filter tasks by various criteria including task ID, task name, deadline, estimated time, progress, completion status, department, and priority.
- Add new tasks.
- Change task progress, priority, and department.
- Mark tasks as completed.
- View a list of tasks with details such as ID, name, creation date, deadline, estimated completion time, progress, completion status, department, and priority.
- Visualize task progress and priority using bar charts.
- Charts display tooltips with task names for each category (e.g., Not Started, In Progress, Completed).

##### Languages / Frameworks used:
+ Flask
+ CS50 Library for SQL
+ SQLite
+ Chart.jss
+ HTML/CSS
+ Bootstrap

##### File structure:

project/
â”œâ”€â”€ static/
â”‚   â”œâ”€â”€ styles.css
â”œâ”€â”€ templates/
â”‚   â”œâ”€â”€ apology.html
â”‚   â”œâ”€â”€ completed.html
â”‚   â”œâ”€â”€ department.html
â”‚   â”œâ”€â”€ index.html
â”‚   â”œâ”€â”€ layout.html
â”‚   â”œâ”€â”€ login.html
â”‚   â”œâ”€â”€ logout.html
â”‚   â”œâ”€â”€ priority.html
â”‚   â”œâ”€â”€ progress.html
â”‚   â”œâ”€â”€ register.html
â”œâ”€â”€ app.py
â”œâ”€â”€ helpers.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ README.md
â””â”€â”€ tasks.db
##### File structure:
###### styles.css
Here you can find all the css and styling of the website

###### app.py
In app.py it was imported all the libraries needed for the application, as well as the tasks.db file, which was the database used to store the users and the tasks.

Beginning with the @app.route("/") where index is defined, the idea is to show the user a list of their tasks with a filter option and then display the task progress and priority using bar charts. To do this the function request.args.get was used to retrieve the value of each parameter, then to apply the filter we query the database with the "SELECT * FROM tasks WHERE leader_id = ? " to then complete the statement with the conditionals displayed afterwards if a filter was used, followed by the "params" to concatenate the respective parameters in the "?" when required.
Finally we execute the query with parameters

In the @app.route("/login"...) we just check that all inputs are filled out and that the username and the hash password matches in order to allow the user to log in

In the @app.route("/logout") the session is just cleared and redirects to the log in page.

In the @app.route("/register", methods=["GET", "POST"]), the user is asked for a username (not being used yet) and a password with a confirmation of it. If all validations are passed, then the new user is created in the tasks.db database and the user is automatically logged in in their session.

In the @app.route("/change", methods=["GET", "POST"]), the user has the possibility to change their password when needed. It happends just by providing the existing password and a new password with its confirmation. if all validations are passed, then the password is successfully changed.

In the @app.route("/add", methods=["GET", "POST"]), the user can add new tasks to their dashboard. It has to add the task name, deadline, estimated time to completed (days), progress, priority, department and if it is aldeary done. Them the user is redirected to the route("/")

In the @app.route("/progress", methods=["GET", "POST"]), the user can change the stage or progress of their tasks. To do this, a loop through all their tasks is done to see where the changes has been made and thus apply this changes in the database.

In the @app.route("/completed", methods=["GET", "POST"]), the user can mark a task as completed. To do this, a loop is done through all the tasks to change the ones where the completed status has changed to update it in the database.

In the @app.route("/priority", methods=["GET", "POST"]), the user can change the priority of its tasks. If follows the same logic as explained in ("/progress").

In the @app.route("/department", methods=["GET", "POST"]), the user can change which department is in charge of whichs tasks. To do this, a loop is done through all the tasks where the department has change in order to update them in the database.

###### Templates

In apology.html is a template that is used (same as in the Finance problem), where every time a mistake is made or a validation is not completed, this template is shown

In completed.html is the templated where @app.route("/completed") is rendered, as well as department.html with In the @app.route("/department"), login.html with @app.route("/login"), logout.html with @app.route("/logout"), priority.html with @app.route("/priority"),progress.html with @app.route("/progress"), register.html with @app.route("/register"), task.html with @app.route("/add"), change.html with @app.route("/change")

The layout.html is where all the standard formatting is done. Finally, Index.html is where the standard @app.route("/") is display. here is where all tasks are displayed, as well as the tool that allow us to filter all of them. Finally, there is a script code that allows us to take the information of each tasks process and priority and to display them in a bar chart.

###### helpers.py

Here it was used the same helpers functions "def log_ing" and "def apology" that were used in the pset Finance.

###### tasks.db

Is is the database used to store all the information from the application. It has the following schema:
CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
username TEXT NOT NULL,
hash TEXT NOT NULL,
role TEXT NOT NULL CHECK (role IN ('leader', 'support')),
task_id INTEGER,
FOREIGN KEY (task_id) REFERENCES tasks(id)
);

CREATE TABLE tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name TEXT NOT NULL,
time DATETIME DEFAULT CURRENT_TIMESTAMP,
leader_id INTEGER NOT NULL,
support_id INTEGER,
deadline DATETIME NOT NULL,
estimated_time INTEGER NOT NULL,
progress INTEGER NOT NULL CHECK (progress >= 0 AND progress <= 2),
completed INTEGER NOT NULL CHECK(completed IN (0, 1)),
department TEXT NOT NULL CHECK (department IN ('marketing', 'sales', 'accounting', 'HR', 'production', 'development', 'service')),
priority NUMERIC NOT NULL CHECK (priority >= 0 AND priority <= 2),
FOREIGN KEY (leader_id) REFERENCES users(id),
FOREIGN KEY (support_id) REFERENCES users(id)
);

The support_id and the role were not finally used in the web application
