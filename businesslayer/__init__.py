import json
import random
import secrets
from flask import Flask, request
import requests
from databaselayer import db, get_balanceDB, add_userDB, get_detailsDB, update_balanceDB
import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.PostGres["URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.PostGres["TRACK_MODIFICATIONS"]
app.secret_key = config.PostGres["SECRET KEY"]
db.init_app(app)


# API to create a new user and add it to the database
@app.route("/user", methods=["POST"])
def create_user():
    try:
        data = json.loads(request.data)
        name = data["name"]
        address = data["address"]
        phone = data["phone"]
    except:
        return json.dumps({"status": "error"}), 400

# random number generator to generate account number and ifsc code
    acno = random.randint(1000000000, 9999999999)
    ifsc = secrets.token_hex(9)
    balance = 1000

# add_userDB is a function in databaselayer to add a new user to the database
    add_userDB(
        name, address, phone, acno, ifsc, balance
    )
    return {"Bank Account Number": acno, "IFSC Number": ifsc}, 200


# API to get the balance of the user
@app.route("/balance", methods=["GET"])
def get_balance():
    try:
        data = json.loads(request.data)
        acno = str(data["acno"])
        ifsc = data["ifsc"]
    except:
        return json.dumps({"status": "error"}), 400

 # get_balanceDB is a function in databaselayer to get the balance of the user
    balance = get_balanceDB(
        acno, ifsc
    )
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
        amount = int(data["amount"])

# API call to get the exchange rate of USD to INR
        if data["usd"] == 1:
            exchangeRate = requests.get(
                config.ExchangeAPI["URL"]
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

 # update_balanceDB is a function in databaselayer to update the balance
    if sbalance >= amount:
        if (
            update_balanceDB(
                Sacno, Sifsc, sbalance - amount
            )
            is False
        ):
            return {"Error": "Something went wrong"}, 400
        if update_balanceDB(Racno, Rifsc, rbalance + amount) is False:
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

# get_detailsDB is a function in databaselayer to get the details of the user
    user = get_detailsDB(
        acno, ifsc
    )
    if user:
        return {
            "Name": user.name,
            "Address": user.address,
            "Phone": user.phone,
            "Balance": user.balance,
        }, 200
    else:
        return {"Error": "Account Number or IFSC Number is incorrect"}, 400
