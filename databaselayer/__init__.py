import json
import random
import secrets
from urllib import response
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def add_userDB(name, address, phone, acno, ifsc, balance):
    user = MyClass(
        name=name, address=address, phone=phone, acno=acno, ifsc=ifsc, balance=balance
    )
    db.session.add(user)
    db.session.commit()


def get_balanceDB(acno, ifsc):
    user = MyClass.query.filter_by(acno=acno, ifsc=ifsc).first()
    if user:
        return user.balance
    else:
        return None


def get_detailsDB(acno, ifsc):
    user = MyClass.query.filter_by(acno=acno, ifsc=ifsc).first()
    if user:
        return user
    else:
        return None


def update_balanceDB(acno, ifsc, amount):
    user = MyClass.query.filter_by(acno=acno, ifsc=ifsc).first()
    if user:
        user.balance = amount
        db.session.commit()
        return True
    else:
        return False


class MyClass(db.Model):

    __tablename__ = "details"
    name = db.Column(db.String(100))
    address = db.Column(db.String(1000))
    phone = db.Column(db.String(13))
    acno = db.Column(db.String(20), primary_key=True)
    ifsc = db.Column(db.String(20), primary_key=True)
    balance = db.Column(db.Integer)

    def __init__(self, name, address, phone, acno, ifsc, balance):
        self.name = name
        self.address = address
        self.phone = phone
        self.acno = acno
        self.ifsc = ifsc
        self.balance = balance
