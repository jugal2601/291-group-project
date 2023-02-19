CMPUT 291, Fall 2021
Assignment #3

GROUP 28 -> We declare that we did not collaborate with anyone outside our own group in this assignment
famobiwo: Moyinoluwa Famobiwo 
ashire1: Alia Shire
sadhnani: Jugal Khubchand Sadhnani
nkokeke: Kingsley Okeke

Query #1: 

We executed the following SQL query:

SELECT Count(order_id) 
FROM Customers C, Orders O 
where C.customer_postal_code=? 
AND C.customer_id=O.customer_id;

We assumed that SQLITE would create indices on the primary keys customer_id, 
but in any possible scenario that it does not, we still created the indices on customer_id. 
We did not create any indices on order_id because we assumed that it was gonna be created by SQLITE. 
Then we also created indices on customer_potal_code.
 

Query #2: 

We executed the following SQL query:

SELECT COUNT(O.order_id), AVG(OS.size)
FROM Orders O, Customers C, OrderSize OS
WHERE O.customer_id = C.customer_id
AND OS.oid = O.order_id
AND C.customer_postal_code = ?
GROUP BY O.order_id

We created indices on customer_id, customer_postal_code, order_id, and order_items_id.
Creating the index on customer_postal_code assisted with optimizing the query under
the constraint "C.customer_postal_code = ?". 
Because we would be using the fields customer_id, order_id and order_items_id,
we enforced those indices to avoid accessing unnecessary tables.

Query #3: 

We executed the following SQL query:

SELECT COUNT(O.order_id), AVG(OS.size)
FROM Orders O, Customers C, OrderSize OS
WHERE O.customer_id = C.customer_id
AND OS.oid = O.order_id
AND C.customer_postal_code = ?
GROUP BY O.order_id

We created indices on customer_id, customer_postal_code, order_id, and order_items_id.
Creating the index on customer_postal_code assisted with optimizing the query under
the constraint "C.customer_postal_code = ?". 
Because we would be using the fields customer_id, order_id and order_items_id,
we enforced those indices to avoid accessing unnecessary tables.


QUERY #4:

We executed the following SQL query:

SELECT COUNT(DISTINCT S.seller_postal_code)
FROM (SELECT order_id
    FROM Order_items
    ORDER BY random()
    LIMIT 1) Random_Result, Order_items O, Sellers S
WHERE S.seller_id = O.seller_id and O.order_id = Random_Result.order_id

We assumed that SQLITE would create indices on the primary keys order_id, but in any possible scenario that it does not, we still created the indices on order_id. We did not create
any indices on seller_id because we assumed that it was gonna be created by SQLITE.Then in all, we created composite indices on both Tables, Sellers (order_id and seller_id) along with 
composite keys on Order_Items (seller_postal_code and seller_id).
