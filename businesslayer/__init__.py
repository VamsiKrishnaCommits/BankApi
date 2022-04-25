import json
import random
import secrets
from flask import Flask, request
import requests
from databaselayer import db, get_balanceDB, add_userDB, get_detailsDB, update_balanceDB


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:vamsi@localhost/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "vamsi"
db.init_app(app)



# API to create a new user and add it to the database
@app.route("/user", methods=["POST", "GET"])
def create_user():
    try:
        data = json.loads(request.data)
        name = data["name"]
        address = data["address"]
        phone = data["phone"]
    except:
        return json.dumps({"status": "error"}), 400

    acno = random.randint(1000000000, 9999999999)
    ifsc = secrets.token_hex(9)
    balance = 1000
    add_userDB(name, address, phone, acno, ifsc, balance)
    return {"Bank Account Number": acno, "IFSC Number": ifsc}, 200

#API to get the balance of the user
@app.route("/balance", methods=["GET"])
def get_balance():
    try:
        data = json.loads(request.data)
        acno = str(data["acno"])
        ifsc = data["ifsc"]
    except:
        return json.dumps({"status": "error"}), 400

    balance = get_balanceDB(acno, ifsc)
    if balance:
        return {"Balance": balance}, 200
    else:
        return {"Error": "Account Number or IFSC Number is incorrect"}, 400

# API to transfer money from one account to another
@app.route("/transaction", methods=["PUT"])
def transactionDebit():
    try:
        data = json.loads(request.data)
        Sacno = str(data["sacno"])
        Sifsc = data["sifsc"]
        Racno = str(data["racno"])
        Rifsc = data["rifsc"]
        amount = data["amount"]
        if data["usd"] == 1:
            exchangeRate = requests.get(
                "https://v6.exchangerate-api.com/v6/1af736fc7aa68a3132bc9678/latest/USD"
            )
            amount = amount * exchangeRate.json()["conversion_rates"]["INR"]
    except:
        return json.dumps({"status": "error"}), 400

    sbalance = get_balanceDB(Sacno, Sifsc)
    if sbalance is None:
        return {"Error": "Sender Account Number or IFSC Number is incorrect"}, 400

    rbalance = get_balanceDB(Racno, Rifsc)
    if rbalance is None:
        return {"Error": "Receiver Account Number or IFSC Number is incorrect"}, 400

    if sbalance >= amount:
        if (
            update_balanceDB(Sacno, Sifsc, sbalance - amount)
            is False
        ):
            return {"Error": "Something went wrong"}, 400
        if (
            update_balanceDB(Racno, Rifsc, rbalance + amount)
            is False
        ):
            return {"Error": "Something went wrong"}, 400
        return {"Transaction Successful": "Successfully transferred"}, 200

    else:
        return {"Error": "Insufficient Balance"}, 400

# Get details of a user
@app.route("/details", methods=["GET"])
def get_details():
    try:
        data = json.loads(request.data)
        acno = str(data["acno"])
        ifsc = data["ifsc"]
    except:
        return json.dumps({"status": "error"}), 400
    user = get_detailsDB(acno, ifsc)
    if user:
        return {
            "Name": user.name,
            "Address": user.address,
            "Phone": user.phone,
            "Balance": user.balance,
        }, 200
    else:
        return {"Error": "Account Number or IFSC Number is incorrect"}, 400
