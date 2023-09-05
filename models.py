from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class REST_INFO(db.Model):
    __tablename__ = 'REST_INFO'
    REST_Name = db.Column(db.String(255), primary_key=True,unique = True)
    REST_Type  = db.Column(db.String(255))
    REST_Address = db.Column(db.String(255))
    REST_Web  = db.Column(db.String(255))
    Tel  = db.Column(db.Integer)
    
class REST_MENU(db.Model):
    __tablename__ = 'REST_MENU'
    Num = db.Column(db.Integer, primary_key=True)
    REST_Name = db.Column(db.String(255),db.ForeignKey('REST_INFO.REST_Name'))
    MENU_Name = db.Column(db.String(255))
    MENU_Price = db.Column(db.String(255), default='0')
    
class REST_REVIEW(db.Model):
    __tablename__ = 'REST_REVIEW'
    Num = db.Column(db.Integer, primary_key=True)
    REST_Name = db.Column(db.String(255), db.ForeignKey('REST_INFO.REST_Name'))
    R_Text = db.Column(db.String(255))
    R_Date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    R_Score = db.Column(db.String(255))
    