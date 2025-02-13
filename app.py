from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app =  Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # database name is todo.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This is to suppress warning

# initialize the database
db = SQLAlchemy(app)

# Model for the database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'


with app.app_context():
    db.create_all()


@app.route('/', methods = ['GET', 'POST']) # homepage route
def home():
    # add a task
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"ERROR :{e}")
            return 'There was an issue adding your task'
    # see all current tasks
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)  # render index.html page


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was problem deleting task ☠ ' 

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task = task_to_update)



if __name__ == "__main__":
    app.run(debug=True, port=3000) #start the flask server
