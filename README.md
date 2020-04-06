# Decathlon Offsite Test

Assuming q1.csv, q2.csv, q3.csv are stored in ./data/

requirement.txt is generated from colab directly for question 3 only

### Question 1

Running on google cloud platform VM instance
Machine type: n1-highmem-2 (2 vCPUs, 13 GB memory)
Image: ubuntu-1604-xenial-v20200317
Postgresql version: psql (PostgreSQL) 9.5.21

Install and start PostgreSQL
```
sudo apt-get update 
sudo apt-get install postgresql postgresql-contrib

sudo -i -u postgres
psql
```

Create Table and Load csv
```
CREATE TABLE transaction_detail ( transaction_id varchar(60), rfid varchar(18), type_detail varchar(10), transaction_date timestamp);

\copy transaction_detail FROM '/home/data/q1.csv' DELIMITER ',' CSV HEADER;
```


### Question 2

The question is ambigious on whether "LABEL" or "ITEM CODE" is to be counted. I decided to count ITEM CODE because the customers cant buy
the items if their suitable sizes are not available.

pandas version = '0.25.0'
python version = 3.7.1


### Question 3 

The ipynb is developed on google colab. Created a folder "data" and q3.csv is upload to "./data"

The ipynb contains two models 

1. Foresting the turnover for each store in year 2020 before the start of 2020

2. Foresting the turnover for each store x days before

Catboost is chosen because there are many categorical features and catboost is a fast, convenient, and performant model to deal with them.

