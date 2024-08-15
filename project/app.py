import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tasks.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show list of users tasks with filter option"""
    # Get filter parameters from from
    task_id = request.args.get("task_id")
    task_name = request.args.get("task_name")
    deadline = request.args.get("deadline")
    estimated_time = request.args.get("estimated_time")
    progress = request.args.get("progress")
    completed = request.args.get("completed")
    department = request.args.get("department")
    priority = request.args.get("priority")

    #base query
    query = "SELECT * FROM tasks WHERE leader_id = ? "
    params = [session["user_id"]]

    #Add filters to query if provided
    if task_id:
        query += " AND id = ?"
        params.append(task_id)
    if task_name:
        query += " AND name LIKE ?"
        params.append(f"%{task_name}%")
    if deadline:
        query += " AND deadline = ?"
        params.append(deadline)
    if estimated_time:
        query += " AND estimated_time = ?"
        params.append(estimated_time)
    if progress:
        query += " AND progress = ?"
        params.append(progress)
    if completed:
        query += " AND completed = ?"
        params.append(completed)
    if department:
        query += " AND department = ?"
        params.append(department)
    if priority:
        query += " AND priority = ?"
        params.append(priority)

    query += " ORDER BY deadline"
    print(query)
    print(params)

    #Execute query with parameters
    tasks = db.execute(query, *params)


    return render_template("index.html", tasks=tasks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was created
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was created
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation password was created
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation password", 400)

        # Ensure password and confirmation password matches
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords does not match", 400)

        # Look for user in database
        user_row = db.execute("SELECT * FROM users WHERE username = ?",
                              request.form.get("username"))

        # Is user already in the database?
        if len(user_row) != 0:
            return apology("Username already exist", 400)

        # Generate hash password
        hash_password = generate_password_hash(request.form.get("password"))

        # Add user to Database
        db.execute("INSERT INTO users (username, hash, role) VALUES(?, ?, ?)",
                   request.form.get("username"), hash_password, request.form.get("role"))

        # look for new added user
        user_row = db.execute("SELECT * FROM users WHERE username = ?",
                              request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = user_row[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")




@app.route("/change", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password"""
    if request.method == "POST":
        if not request.form.get("password"):
            return apology("must provide password", 400)

        if not request.form.get("new_password"):
            return apology("must provide a new password", 400)

        if not request.form.get("confirmation"):
            return apology("must provide the password confirmation for the new password", 400)

        password_row = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])
        current_password_hash = password_row[0]["hash"]

        if not check_password_hash(current_password_hash, request.form.get("password")):
            return apology("Invalid current password", 400)

        if request.form.get("new_password") != request.form.get("confirmation"):
            return apology("New passwords does not match", 400)

        hash_new_password = generate_password_hash(request.form.get("new_password"))

        # update password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash_new_password, session["user_id"])

        flash(f"Succesfull change of passwords for user {session["user_id"]}!")

        return redirect("/")

    else:
        return render_template("change.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_task():
    """Add a task"""
    if request.method == "POST":

        if not request.form.get("task_name"):
            return apology("must provide the name of the task", 400)

        if not request.form.get("deadline"):
            return apology("must provide a deadline", 400)

        if not request.form.get("estimated"):
            return apology("must provide the estimated amount of days to complete the task", 400)

        if not request.form.get("progress") or not int(request.form.get("progress")) >= 0 or not int(request.form.get("progress")) <= 2:
            return apology("Select progress from the given options", 400)

        if not request.form.get("priority") or not int(request.form.get("priority")) >= 0 or not int(request.form.get("priority")) <= 2:
            return apology("Select priority from the given options", 400)

        if not request.form.get("department"):
            return apology("Select department from the given options", 400)

        if not request.form.get("completed") or not int(request.form.get("completed")) >= 0 or not int(request.form.get("completed")) <= 1:
            return apology("Select yes or not for completed", 400)

        existing_taks = db.execute("SELECT * FROM tasks WHERE name = ?", request.form.get("task_name"))

        # Is user already in the database?
        if len(existing_taks) != 0:
            return apology("Task already exist", 400)

        # Add user to Database
        db.execute("INSERT INTO tasks (name, leader_id, deadline, estimated_time, progress, priority, department, completed) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                   request.form.get("task_name"), session["user_id"], request.form.get("deadline"), request.form.get("estimated"),
                   request.form.get("progress"), request.form.get("priority"), request.form.get("department"), request.form.get("completed"))

        flash(f"Succesfull added tasks {request.form.get("task_name")} with deadline {request.form.get("deadline")} and estimated days = {request.form.get("estimated")} for user ID: {session["user_id"]}!")

        return redirect("/")
    else:
        return render_template("task.html")


@app.route("/progress", methods=["GET", "POST"])
@login_required
def change_progress():
    """Change progress"""
    if request.method =="POST":

        # Loop through form submissions to update progress for each task
        for task_id, updated_progress in request.form.items():
            # Update progress in the database
            db.execute("UPDATE tasks SET progress = ? WHERE id = ?", updated_progress, task_id)

        # After updating progress, query tasks again to display the updated data
        tasks = db.execute("SELECT id, name, progress FROM tasks WHERE leader_id = ? ORDER BY id", session["user_id"])


        return render_template("progress.html", tasks=tasks)

    else:
        tasks = db.execute("SELECT id, name, progress FROM tasks WHERE leader_id = ? ORDER BY id", session["user_id"])
        return render_template("progress.html", tasks=tasks)



@app.route("/completed", methods=["GET", "POST"])
@login_required
def completed():
    """Mark as completed"""
    if request.method =="POST":

        # Loop through form submissions to update completed for each task
        for task_id, finished_status in request.form.items():
            # Update progress in the database
            db.execute("UPDATE tasks SET completed = ? WHERE id = ?", finished_status, task_id)

        # After updating completed, query tasks again to display the updated data
        tasks = db.execute("SELECT id, name, completed FROM tasks WHERE leader_id = ? ORDER BY id", session["user_id"])


        return render_template("completed.html", tasks=tasks)

    else:
        tasks = db.execute("SELECT id, name, completed FROM tasks WHERE leader_id = ? ORDER BY id", session["user_id"])
        return render_template("completed.html", tasks=tasks)


@app.route("/priority", methods=["GET", "POST"])
@login_required
def change_priority():
    """Change priority"""
    if request.method =="POST":

        # Loop through form submissions to update progress for each task
        for task_id, priority in request.form.items():
            # Update progress in the database
            db.execute("UPDATE tasks SET priority = ? WHERE id = ?", priority, task_id)

        # After updating progress, query tasks again to display the updated data
        tasks = db.execute("SELECT id, name, priority FROM tasks WHERE leader_id = ? ORDER BY id", session["user_id"])


        return render_template("priority.html", tasks=tasks)

    else:
        tasks = db.execute("SELECT id, name, priority FROM tasks WHERE leader_id = ? ORDER BY id", session["user_id"])
        return render_template("priority.html", tasks=tasks)


@app.route("/department", methods=["GET", "POST"])
@login_required
def change_department():
    """Change department"""
    if request.method =="POST":

        # Loop through form submissions to update department for each task
        for task_id, updated_department in request.form.items():
            # Update progress in the database
            db.execute("UPDATE tasks SET department = ? WHERE id = ?", updated_department, task_id)

        # After updating department, query tasks again to display the updated data
        tasks = db.execute("SELECT id, name, department FROM tasks WHERE leader_id = ? ORDER BY id", session["user_id"])


        return render_template("department.html", tasks=tasks)

    else:
        tasks = db.execute("SELECT id, name, department FROM tasks WHERE leader_id = ? ORDER BY id", session["user_id"])
        return render_template("department.html", tasks=tasks)
