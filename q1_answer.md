# Assumption

Assume that the propose of this task is to understand the period between sales and restock 
And to find out which items require more time to restock

For each ‘sale’ record of specific rfid, left join the next ‘return’ record of that item and calculate the days difference.

Four different queries are created to show:

1. Total days difference between ‘sale’ and ‘return’ for each item in October 2019

2. Average days difference between ‘sale’ and ‘return’ for each item in October 2019

3. Items with only‘sale’record

4. Items with only‘return’record


### Total days difference between ‘sale’ and ‘return’ for each item in October 2019 where both‘sale’ and ‘return’exist

```
WITH T_SALE AS 
(SELECT * FROM transaction_detail WHERE type_detail = 'sale'), 
T_RETURN AS 
(SELECT * FROM transaction_detail WHERE type_detail = 'return'),
TMP_RESULTS AS
(SELECT T_SALE.rfid, T_SALE.transaction_date AS sale_date, MIN(T_RETURN.transaction_date) AS return_date, 
DATE_PART('day', age(MIN(T_RETURN.transaction_date), T_SALE.transaction_date)) AS days_diff 
FROM T_SALE LEFT JOIN T_RETURN ON T_SALE.rfid = T_RETURN.rfid AND T_RETURN.transaction_date > T_SALE.transaction_date GROUP BY T_SALE.rfid, T_SALE.transaction_date)
SELECT rfid, SUM(days_diff) AS days_diff_sum FROM TMP_RESULTS GROUP BY rfid HAVING SUM(days_diff) IS NOT NULL ORDER BY SUM(days_diff) DESC;
```


### Average days difference between ‘sale’ and ‘return’ for each item in October 2019

```
WITH T_SALE AS 
(SELECT * FROM transaction_detail WHERE type_detail = 'sale'), 
T_RETURN AS 
(SELECT * FROM transaction_detail WHERE type_detail = 'return'),
TMP_RESULTS AS
(SELECT T_SALE.rfid, T_SALE.transaction_date AS sale_date, MIN(T_RETURN.transaction_date) AS return_date, 
DATE_PART('day', age(MIN(T_RETURN.transaction_date), T_SALE.transaction_date)) AS days_diff 
FROM T_SALE LEFT JOIN T_RETURN ON T_SALE.rfid = T_RETURN.rfid AND T_RETURN.transaction_date > T_SALE.transaction_date GROUP BY T_SALE.rfid, T_SALE.transaction_date)
SELECT rfid, AVG(days_diff) AS days_diff_avg FROM TMP_RESULTS GROUP BY rfid HAVING AVG(days_diff) IS NOT NULL ORDER BY AVG(days_diff) DESC;
```


### Items with only‘sale’record

```
WITH T_SALE AS 
(SELECT * FROM transaction_detail WHERE type_detail = 'sale'), 
T_RETURN AS 
(SELECT * FROM transaction_detail WHERE type_detail = 'return'),
TMP_RESULTS AS
(SELECT T_SALE.rfid, T_SALE.transaction_date AS sale_date, MIN(T_RETURN.transaction_date) AS return_date, 
DATE_PART('day', age(MIN(T_RETURN.transaction_date), T_SALE.transaction_date)) AS days_diff 
FROM T_SALE LEFT JOIN T_RETURN ON T_SALE.rfid = T_RETURN.rfid AND T_RETURN.transaction_date > T_SALE.transaction_date GROUP BY T_SALE.rfid, T_SALE.transaction_date)
SELECT rfid, SUM(days_diff) AS total_days_diff FROM TMP_RESULTS GROUP BY rfid HAVING SUM(days_diff) IS NULL;
```


### Items with only‘return’record

```
WITH T_SALE AS 
(SELECT * FROM transaction_detail WHERE type_detail = 'sale'), 
T_RETURN AS 
(SELECT * FROM transaction_detail WHERE type_detail = 'return'),
TMP_RESULTS AS
(SELECT T_SALE.rfid, T_SALE.transaction_date AS sale_date, MIN(T_RETURN.transaction_date) AS return_date, DATE_PART('day', age(MIN(T_RETURN.transaction_date), T_SALE.transaction_date)) AS days_diff FROM T_SALE LEFT JOIN T_RETURN ON T_SALE.rfid = T_RETURN.rfid AND T_RETURN.transaction_date > T_SALE.transaction_date GROUP BY T_SALE.rfid, T_SALE.transaction_date),
SALE_EXIST AS
(SELECT rfid, SUM(days_diff) AS days_diff_sum FROM TMP_RESULTS GROUP BY rfid)
SELECT T.* FROM transaction_detail AS T LEFT JOIN SALE_EXIST AS S ON T.rfid = S.rfid WHERE S.rfid IS NULL;
```
