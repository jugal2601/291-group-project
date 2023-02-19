# assignment3
GROUP 28 -> We declare that we did not collaborate with anyone outside our own group in this assignment
famobiwo 
ashire1 
sadhnani Jugal Khubchand Sadhnani
nkokeke Kingsley Okeke

QUERY #1
SELECT Count(order_id)
    FROM Customers C, Orders O
    where C.customer_postal_code=? 
    AND C.customer_id=O.customer_id;

We assumed that SQLITE would create indices on the primary keys customer_id, but in any possible scenario that it does not, we still created the indices on customer_id. We did not create any indices on order_id because we assumed that it was gonna be created by SQLITE. Then we also created indices on customer_potal_code.

QUERY #4
SELECT COUNT(DISTINCT S.seller_postal_code)
FROM (SELECT order_id
    FROM Order_items
    ORDER BY random()
    LIMIT 1) Random_Result, Order_items O, Sellers S
WHERE S.seller_id = O.seller_id and O.order_id = Random_Result.order_id

We assumed that SQLITE would create indices on the primary keys order_id, but in any possible scenario that it does not, we still created the indices on order_id. We did not create
any indices on seller_id because we assumed that it was gonna be created by SQLITE.Then in all, we created composite indices on both Tables, Sellers(seller_postal_code and seller_id) along with 
composite keys on Order_Items (order_id and seller_id).
