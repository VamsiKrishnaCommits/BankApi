# BankApi

The code of this project is seperated into two folders : DatabaseLayer , BusinessLayer

This is to ensure easy maintanence and migration to a different database becomes seamless if the business logic is not aware of the 
  kind of database that is being used. In a nutshell , the database is abstracted from the business logic.

The code is written in python and the database used is PostgreSQL 

The requirements asked are satisfied by using the APIs that are built

Accepts only JSON format to process requests for simplicity

There are 4 APIs  -
1) "/user" - POST - used to create a user - { "name" : "xxx" , "phone" : "XXX" , "address" : "xxx" } 

    A nominal amount of 1000 INR is credit for every account created

2) "/balance" - GET - used to fetch available funds - {"acno" : "xxx" , "ifsc" : "xxx"}

3) "/transaction" - PUT - used to perform a money transfer - {"sacno" : "xxx" ,"sifsc" : "xxx" , "racno" :"xxx" , "rifsc" : "xxx" , "usd" : 1/0 , "amount" : xx }
    
    If you are trying to send USD , the usd field in the PUT request must be set to 1 else the field must be set to 0

4) "/details" - GET - used to fetch the complete information of the user - {"acno" : "xxx" , "ifsc" : "xxx"} 

All the fields are MANDATORY , missing any of them would yeild an error 
