import datetime
from __init__ import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

class User(db.Model):
    user_id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(200), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "- USER - user_id: {}, email: {}, first_name: {}, last_name: {}, date_created: {}".format(self.user_id, self.email, self.first_name, self.last_name, self.date_created)

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_created': self.date_created
        }

class Note(db.Model):
    note_id = Column(Integer, primary_key=True)
    note_title = Column(String(100), nullable=False)
    note_content = Column(String(1000), nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)

    def __repr__(self):
        return "- NOTE - note_id: {}, note_title: {}, note_content: {}, completed: {}, date_created: {date_created}, user_id: {}".format(self.note_id, self.note_title, self.note_content, self.completed, self.date_created, self.user_id)

    @property
    def serialize(self):
        return {
            'note_id': self.note_id,
            'note_title': self.note_title,
            'note_content': self.note_content,
            'date_created': self.date_created,
            'completed': self.completed,
        }

class Scratch(db.Model):
    scratch_id = Column(Integer, primary_key=True)
    scratch_title = Column(String(100), nullable=False)
    scratch_content = Column(String(1000), nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)

    def __repr__(self):
            return "- SCRATCH - scratch_id: {}, scratch_title: {}, scratch_content: {}, completed: {}, date_created: {date_created}, user_id: {}".format(self.scratch_id, self.scratch_title, self.scratch_content, self.completed, self.date_created, self.user_id)

    @property
    def serialize(self):
        return {
            'scratch_id': self.scratch_id,
            'scratch_title': self.scratch_title,
            'scratch_content': self.scratch_content,
            'date_created': self.date_created,
            'completed': self.completed,
        }