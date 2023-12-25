from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phonenumber = db.Column(db.String(15))
    last_haircut = db.Column(db.String(50))


@app.route('/')
def index():
    schedule = User.query.all()
    return render_template('index.html', schedule=schedule)


@app.route('/make_appointment', methods=['POST'])
def make_appointment():
    if request.method == 'POST':
        date = request.form['date']
        hour = int(request.form['hour'])
        user_id = request.form['user_id']
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phonenumber = request.form['phonenumber']
        last_haircut = request.form['last_haircut']

        new_appointment = User(date=date, hour=hour, user_id=user_id, username=username,
                               first_name=first_name, last_name=last_name,
                               phonenumber=phonenumber, last_haircut=last_haircut)

        db.session.add(new_appointment)
        db.session.commit()

        return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
