from flask import Flask, render_template, url_for, request, redirect  # ""request"" for the user request by post or get
from flask_sqlalchemy import SQLAlchemy  #allows us to configure our database and to initialyse it
from datetime import datetime

# configuration of flask app
app = Flask(__name__)

# configuration sqlalchemy with a set up name of our database "test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# initialyse the database
db = SQLAlchemy(app)

app.app_context().push()

# Model is a table in the database.
# So a Model has some properties that define it like id, name, address
class Todo(db.Model):
    """ creating a table in the database with an id as primary key,..... """
    
    id = db.Column(db.Integer, primary_key=True)
    # db.String(200) the colunm can contain 200 characters and nullable=False is a way of say the colunm can not be empty(null)
    content = db.Column(db.String(200), nullable=False)
    # datetime.utcnow allows the column to store a default time
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # this function returns a string format ofany user in our database 
    def __repr__(self):
        return '<Task %r>' % self.id




@app.route("/", methods=["POST", "GET"])
def index():

    if request.method == "POST":
        task_content = request.form["content"]

        # create an instance/object of our Todo model
        new_task = Todo(content=task_content)

        # then try to push it to our database
        try:
            # to add the user content in the database
            db.session.add(new_task)
            # to save the user content in the database
            db.session.commit()

            # after add the user task to the database we redirect him/her to the index page again
            return redirect("/")
        except:
            return "There was an issue adding your task"

    # to fetch all the todo task that the user has in the "Todo" table and then to order then by the date_created
    tasks = Todo.query.order_by(Todo.date_created).all()
    
    
    return render_template("index.html", tasks=tasks)

# the route will have the todo id as it will be pass by the index page 
@app.route("/delete/<int:id>")
def delete(id):
    # the function will query to Todo by id and if it does not found the id it will return a 404 error
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        
        # after deletint the task it should redirect us to index
        return redirect("/")
    except:
        return "There was a problem deleting the task."

# we need the methods because the update.html will have a submit buttom
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):

    # the function will query to Todo by id and if it does not found the id it will return a 404 error
    task = Todo.query.get_or_404(id)
     
    if request.method == "POST":
        # the updated content of the task
        task_to_update = request.form["content"]
        
        # setting a new new to our content row
        task.content = task_to_update
        

        try:
            db.session.commit()
            
            # after updating the task it should redirect us to index
            return redirect("/")
        except:
            return "There was a problem updating the task."
    
    return render_template("update.html", task = task)


# this statement is to allow this file run 
# when executing python3 app.py on debug mode
if __name__ == "__main__":
    app.run(debug=True)