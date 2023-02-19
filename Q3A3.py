import sqlite3
import os
import time
import matplotlib.pyplot as plt
import numpy as np

connection = None
cursor = None

# this function connects to the database using the path provided
def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    print("Connection to the database open.")
    connection.commit()
    return


# this function sets the scenario to uninformed mode
# where we create uninfomred tables, similar to the original tables
# without the primary and foreign keys and with the auto indexing switched off
def Uninformed():
    global connection,cursor
    cursor.execute('PRAGMA automatic_index = OFF;')
    cursor.execute("BEGIN TRANSACTION;")
    
    # create customers uninformed table
    # using data from customers table
    cursor.execute("""CREATE TABLE "Customers_uninformed" (
                    "customer_id"	TEXT,
                    "customer_postal_code"	INTEGER
                    );
                    """)
    cursor.execute("INSERT INTO Customers_uninformed SELECT * FROM Customers;")

    # create sellers uninformed table
    # using data from sellers table
    cursor.execute("""CREATE TABLE "Sellers_uninformed" (
                    "seller_id"	TEXT,
                    "seller_postal_code" INTEGER
                    );
                    """)
    cursor.execute("INSERT INTO Sellers_uninformed SELECT * FROM Sellers;")

    # create orders uninformed table
    # using data from orders table
    cursor.execute("""CREATE TABLE "Orders_uninformed" (
                        "order_id"	TEXT,
                        "customer_id"	INTEGER
                    )""")
    cursor.execute("INSERT INTO Orders_uninformed SELECT * FROM Orders;")
    # create orders items uninformed table
    # using data from orders items uninformed table
    cursor.execute("""CREATE TABLE "Order_items_uninformed" (
                        "order_id"	TEXT,
                        "order_item_id"	INTEGER,
                        "product_id"	TEXT,
                        "seller_id"	TEXT
                    )""")
    cursor.execute("INSERT INTO Order_items_uninformed SELECT * FROM Order_items;")

# this function sets the scenario to self optimized mode
# where we use the original tables
# with the auto indexing switched on
def selfoptimized():
    global connection,cursor
    cursor.execute(' PRAGMA foreign_keys=ON ;')
    cursor.execute("PRAGMA automatic_index = ON;")

# this function sets the scenario to user optimized mode
# where we use the original tables
# and we freely create indices that would optimize the performance of the query
def user_optimized():
    global connection,cursor
    cursor.execute("PRAGMA automatic_index=OFF")
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("BEGIN TRANSACTION;")
    cursor.execute("CREATE INDEX CustomersIdx1 ON Customers(customer_postal_code,customer_id);")
    cursor.execute("CREATE INDEX OrdersIdx1 ON Orders(order_id);")
    cursor.execute("CREATE INDEX Order_itemsIdx1 ON Order_items(order_item_id);")

# this function runs query one, which takes two strings as inputs
# the two strings are the customer and orders table
# which are being used in the query
# the function also generates random customer postal code each time it is run
# which is further used to run the final query
def query3(C,O, OI):
    global connection,cursor
    # Generate the random customer postal code
    cursor.execute("""Select customer_postal_code
                    from "{}"
                    ORDER BY RANDOM()
                    LIMIT 1;""".format(C.replace('"', '""')))
    row = cursor.fetchone()
    random_input = row['customer_postal_code']

    # create the view
    cursor.execute("""CREATE TABLE IF NOT EXISTS OrderSize AS
                    SELECT O.order_id AS oid, OI.order_item_id AS size
                    FROM "{}" OI, "{}" O
                    WHERE OI.order_id = O.order_id;
                    """.format(OI.replace('"', '""'),O.replace('"', '""')))
    
    # repeat query 1 adding the average
    cursor.execute("""SELECT COUNT(O.order_id), AVG(OS.size)
                    FROM "{}" O, "{}" C, OrderSize OS
                    WHERE O.customer_id = C.customer_id
                    AND OS.oid = O.order_id
                    AND C.customer_postal_code = ?
                    GROUP BY O.order_id;
                    """.format(O.replace('"', '""'),C.replace('"', '""')),(random_input,))

# this function runs the query with all 3 different scenarios 
# 50 times each, and calculates the average runtime in each scenario
# and store the times in a list and then returns the list
def runSmall():
    # this list will be used to store the average runtimes
    small_list=[]
    global connection,cursor
    # set the path to the small database
    db_path = os.getcwd()+"/A3Small.db"
    print(db_path)
    # create connection using function defined above
    connect(db_path)
    # set the mode to uninformed
    Uninformed()
    # start stores the start time
    start=time.time()
    for i in range(0,50):
        query3("Customers_uninformed","Orders_uninformed","Order_items_uninformed")
    # end stores the end time
    end=time.time()
    connection.close()
    # calculate the average time and store it in the list
    time_uninformed=((end-start)/50)*1000
    small_list.append(time_uninformed)
    
    # create connection using function defined above
    connect(db_path)
    # set the mode to self optimized
    selfoptimized()
    # start_02 stores the start time
    start_02=time.time()
    for i in range(0,50):
        query3("Customers","Orders","Order_items")
    # end_02 stores the end time
    end_02=time.time()
    connection.close()
    # calculate the average runtime and store it in the list
    time_self_optimized=((end_02-start_02)/50)*1000
    small_list.append(time_self_optimized)

    # create connection using function defined above
    connect(db_path)
    # set the mode to user optimized
    user_optimized()
    # start_03 stores the start time
    start_03=time.time()
    for i in range(0,50):
        query3("Customers","Orders","Order_items")
    # end_03 stores the end time
    end_03=time.time()
    connection.close()
    # calculate the average runtime and store it in the list
    time_user_optimized=((end_03-start_03)/50)*1000
    small_list.append(time_user_optimized)
    
    return small_list

def runMedium():
    # this list will be used to store the average runtimes
    medium_list=[]
    global connection,cursor
    # set the path to the medium database
    db_path = os.getcwd()+"/A3Medium.db"
    print(db_path)
    # create connection using function defined above
    connect(db_path)
    # set the mode to uninformed
    Uninformed()
    # start stores the start time
    start=time.time()
    for i in range(0,50):
        query3("Customers_uninformed","Orders_uninformed","Order_items_uninformed")
    # end stores the end time
    end=time.time()
    connection.close()
    # calculate the average time and store it in the list
    time_uninformed=((end-start)/50)*1000
    medium_list.append(time_uninformed)
    ## create connection using function defined above
    connect(db_path)
    # set the mode to self optimized
    selfoptimized()
    # start_02 stores the start time
    start_02=time.time()
    for i in range(0,50):
        query3("Customers","Orders","Order_items")
    # end_02 stores the end time
    end_02=time.time()
    connection.close()
    # calculate the average runtime and store it in the list
    time_self_optimized=((end_02-start_02)/50)*1000
    medium_list.append(time_self_optimized)

    # create connection using function defined above
    connect(db_path)
    # set the mode to user optimized
    user_optimized()
    # start_03 stores the start time
    start_03=time.time()
    for i in range(0,50):
        query3("Customers","Orders","Order_items")
    # end_03 stores the end time
    end_03=time.time()
    connection.close()
    # calculate the average runtime and store it in the list)
    time_user_optimized=((end_03-start_03)/50)*1000
    medium_list.append(time_user_optimized)
    
    return medium_list
    
def runLarge():
    # this list will be used to store the average runtimes
    large_list=[]
    global connection,cursor
    # set the path to the large database
    db_path = os.getcwd()+"/A3Large.db"
    print(db_path)
    # create connection using function defined above
    connect(db_path)
    # set the mode to uninformed
    Uninformed()
    # start stores the start time
    start=time.time()
    for i in range(0,50):
        query3("Customers_uninformed","Orders_uninformed","Order_items_uninformed")
    # end stores the end time
    end=time.time()
    connection.close()
    # calculate the average time and store it in the list
    time_uninformed=((end-start)/50)*1000
    large_list.append(time_uninformed)

    # create connection using function defined above
    connect(db_path)
    # set the mode to self optimized
    selfoptimized()
    # start_02 stores the start time
    start_02=time.time()
    for i in range(0,50):
        query3("Customers","Orders","Order_items")
    # end_02 stores the end time
    end_02=time.time()
    connection.close()
    # calculate the average runtime and store it in the list
    time_self_optimized=((end_02-start_02)/50)*1000
    large_list.append(time_self_optimized)

    # create connection using function defined above
    connect(db_path)
    # set the mode to user optimized
    user_optimized()
    # start_03 stores the start time
    start_03=time.time()
    for i in range(0,50):
        query3("Customers","Orders","Order_items_uninformed")
    # end_03 stores the end time
    end_03=time.time()
    connection.close()
    # calculate the average runtime and store it in the list
    time_user_optimized=((end_03-start_03)/50)*1000
    large_list.append(time_user_optimized)
    
    return large_list


def main():
    labels=["SmallDB","MediumDB","LargeDB"]
    # all these lists store times like: [time uninformed, time self optimized, time user optimized]
    list_01 = runSmall()
    list_02 = runMedium()
    list_03 = runLarge()
    
    # creating a list with just uninformed values
    uninformed_values=[]
    uninformed_values.append(list_01[0])
    uninformed_values.append(list_02[0])
    uninformed_values.append(list_03[0])
    
    # creating a list with just self optimized values
    self_optimized_values=[]
    self_optimized_values.append(list_01[1])
    self_optimized_values.append(list_02[1])
    self_optimized_values.append(list_03[1])
    # creating a list with just user optimized values
    user_optimized_values=[]
    user_optimized_values.append(list_01[2])
    user_optimized_values.append(list_02[2])
    user_optimized_values.append(list_03[2])
    print(uninformed_values)
    print(self_optimized_values)
    print(user_optimized_values)
    # using numpy to define the y arrays
    y1=np.array([elem for elem in uninformed_values])
    y2=np.array([elem for elem in self_optimized_values])
    y3=np.array([elem for elem in user_optimized_values])
    
    # using the matplotlib to plot our stacked bar chart
    plt.bar(labels,y1)
    plt.bar(labels,y2,bottom=y1)
    plt.bar(labels,y3,bottom=y1+y2)
    plt.title("Query 3 (runtime in ms)")
    plt.legend(["Uninformed","Self Optimized", "User Optimized"])
    plt.savefig("Q3A3chart.png")
    
   
  
# run main method when program starts
if __name__ == "__main__":
    main()