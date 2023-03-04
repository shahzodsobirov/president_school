from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import *
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, functions

db = SQLAlchemy()


def db_setup(app):
    app.config.from_object('backend.models.config')
    db.app = app
    db.init_app(app)
    Migrate(app, db)
    return db


class Role(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "role"
    name = Column(String)
    user = relationship("User", backref="role", uselist=False, order_by="User.id")


class User(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "user"
    name = Column(String)
    role_id = Column(Integer, ForeignKey("role.id"))


class Class(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "class"
    name = Column(String)
    timetable = relationship("TimeTable", secondary="user_class", backref="class", order_by="TimeTable.id")


db.Table('user_class',
         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
         db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
         )


class Permission(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "permission"
    name = Column(String)
    user = relationship("User", backref="permission", secondary="user_actions", order_by="User.id")


db.Table('user_actions',
         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
         db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
         )


class WeekDays(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "weekdays"
    name = Column(String)
    timetable = relationship("TimeTable", backref="weekdays", order_by="TimeTable.id")


class Time(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "time"
    start = Column(String)
    end = Column(String)
    timetable = relationship("TimeTable", backref="time", order_by="TimeTable.id")


class Room(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "room"
    name = Column(String)
    timetable = relationship("TimeTable", backref="room", order_by="TimeTable.id")


class TimeTable(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "timetable"
    class_id = Column(Integer, ForeignKey("class.id"))
    weekdays_id = Column(Integer, ForeignKey("weekdays.id"))
    time_id = Column(Integer, ForeignKey("time.id"))
    room_id = Column(Integer, ForeignKey("room.id"))
    user = relationship("User", backref="timetable", secondary="user_class", order_by="User.id")


db.Table('teacher_time_table',
         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
         db.Column('time_table_id', db.Integer, db.ForeignKey('timetable.id'))
         )
