from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Sites(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def flush(self):
        db.session.add(self)
        db.session.flush()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
