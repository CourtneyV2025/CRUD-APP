from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/checkout')
def checkout_page():
    return render_template('checkout.html')

@app.route('/return')
def return_page():
    return render_template('return.html')

@app.route('/library')
def library():
    return render_template('library.html')

@app.route('/return', methods=['POST'])
def return_book():
     task_content = request.form['content']
     new_task = Task(content=task_content)
     db.session.add(new_task)
     db.session.commit()
     return render_template('return.html')

@app.route('/checkout', methods=['POST'])
def checkout_book():
     task_content = request.form['content']
     new_task = Task(content=task_content)
     db.session.add(new_task)
     db.session.commit()
     return render_template('checkout.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route("/api/data")
def get_data():
    # displays data file returned from an API call
    # can do more Python work to format this later
    return app.send_static_file("data.json")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)