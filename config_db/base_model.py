from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phonenumber = db.Column(db.String(15))
    last_haircut = db.Column(db.String(50))


def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
