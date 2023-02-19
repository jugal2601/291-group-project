import sqlite3
import os
import time
import matplotlib.pyplot as plt
import numpy as np

connection = None
cursor = None


def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    print("Connection to the database open.")
    connection.commit()
    return

def Uninformed():
    global connection,cursor
    cursor.execute("PRAGMA foreign_keys=OFF;")
    cursor.execute('PRAGMA automatic_index = OFF;')
    cursor.execute("BEGIN TRANSACTION;")

    cursor.execute("""CREATE TABLE "Customers_uninformed" (
                    "customer_id"	TEXT,
                    "customer_postal_code"	INTEGER
                    );
                    """)
    cursor.execute("INSERT INTO Customers_uninformed SELECT * FROM Customers;")


    cursor.execute("""CREATE TABLE "Sellers_uninformed" (
                    "seller_id"	TEXT,
                    "seller_postal_code" INTEGER
                    );
                    """)
    cursor.execute("INSERT INTO Sellers_uninformed SELECT * FROM Sellers;")


    cursor.execute("""CREATE TABLE "Orders_uninformed" (
                        "order_id"	TEXT,
                        "customer_id"	INTEGER
                    )""")
    cursor.execute("INSERT INTO Orders_uninformed SELECT * FROM Orders;")

    cursor.execute("""CREATE TABLE "Order_items_uninformed" (
                        "order_id"	TEXT,
                        "order_item_id"	INTEGER,
                        "product_id"	TEXT,
                        "seller_id"	TEXT
                    )""")
    cursor.execute("INSERT INTO Order_items_uninformed SELECT * FROM Order_items;")
    cursor.execute("PRAGMA foreign_keys=ON;")

def selfoptimized():
    global connection,cursor
    cursor.execute(' PRAGMA foreign_keys=OFF;')
    cursor.execute("PRAGMA automatic_index = ON;")
    cursor.execute("BEGIN TRANSACTION;")
    cursor.execute("""CREATE TABLE "Customers_self_optimized" (
                        "customer_id"	TEXT,
                        "customer_postal_code"	INTEGER,
                        PRIMARY KEY("customer_id")
                    );
                    """)
    cursor.execute("INSERT INTO Customers_self_optimized SELECT * FROM Customers;")

    cursor.execute("""CREATE TABLE "Sellers_self_optimized" (
                        "seller_id"	TEXT,
                        "seller_postal_code"	INTEGER,
                        PRIMARY KEY("seller_id")
                    );
                    """)
    cursor.execute("INSERT INTO Sellers_self_optimized SELECT * FROM Sellers;")

    cursor.execute("""CREATE TABLE "Orders_self_optimized" (
                    "order_id"	TEXT,
                    "customer_id"	INTEGER,
                    FOREIGN KEY("customer_id") REFERENCES "Customers"("customer_id"),
                    PRIMARY KEY("order_id")
                );""")
    cursor.execute("INSERT INTO Orders_self_optimized SELECT * FROM Orders;")

    cursor.execute("""CREATE TABLE "Order_items_self_optimized" (
                        "order_id"	TEXT,
                        "order_item_id"	INTEGER,
                        "product_id"	TEXT,
                        "seller_id"	TEXT,
                        PRIMARY KEY("order_id","order_item_id","product_id","seller_id"),
                        FOREIGN KEY("order_id") REFERENCES "Orders"("order_id"),
                        FOREIGN KEY("seller_id") REFERENCES "Sellers"("seller_id")
                    )""")
    cursor.execute("INSERT INTO Order_items_self_optimized SELECT * FROM Order_items;")
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    


def user_optimized():
    global connection,cursor
    cursor.execute("PRAGMA automatic_index = off;")
    cursor.execute("BEGIN TRANSACTION;")
    cursor.execute("CREATE INDEX SellerIdx1 ON Sellers(seller_id,seller_postal_code);")
    cursor.execute("CREATE INDEX OrderItemIdx1 ON Order_items(order_id, seller_id);")
    #cursor.commit()


def query4():
    global connection, cursor
    cursor.execute(
        """SELECT COUNT(DISTINCT S.seller_postal_code)
FROM (SELECT order_id
    FROM Order_items
    ORDER BY random()
    LIMIT 1) Random_Result, Order_items O, Sellers S
WHERE S.seller_id = O.seller_id and O.order_id = Random_Result.order_id"""
    )

def runSmall():
    small_list=[]
    global connection,cursor
    # we will hard code the database name, could also get from user

    db_path = os.getcwd()+"/A3Small.db"
    print(db_path)
    # create connection using function defined above
    connect(db_path)

    Uninformed()
    start=time.time()
    for i in range(0,50):
        query4()
    end=time.time()
    connection.close()
    time_uninformed=((end-start)/50)*1000
    small_list.append(time_uninformed)

    connect(db_path)
    #selfoptimized
    selfoptimized()
    start_02=time.time()
    for i in range(0,50):
        query4()
    end_02=time.time()
    connection.close()
    time_self_optimized=((end_02-start_02)/50)*1000
    small_list.append(time_self_optimized)

    connect(db_path)
    user_optimized()
    start_03=time.time()
    for i in range(0,50):
        query4()
    end_03=time.time()
    connection.close()
    time_user_optimized=((end_03-start_03)/50)*1000
    small_list.append(time_user_optimized)
    
    return small_list

def runMedium():
    medium_list=[]
    global connection,cursor

    db_path = os.getcwd()+"/A3Medium.db"
    print(db_path)
    # create connection using function defined above
    connect(db_path)

    Uninformed()
    start=time.time()
    for i in range(0,50):
        query4()
    end=time.time()
    connection.close()
    time_uninformed=((end-start)/50)*1000
    medium_list.append(time_uninformed)

    connect(db_path)
    #selfoptimized
    selfoptimized()
    start_02=time.time()
    for i in range(0,50):
        query4()
    end_02=time.time()
    connection.close()
    time_self_optimized=((end_02-start_02)/50)*1000
    medium_list.append(time_self_optimized)

    connect(db_path)
    user_optimized()
    start_03=time.time()
    for i in range(0,50):
        query4()
    end_03=time.time()
    connection.close()
    time_user_optimized=((end_03-start_03)/50)*1000
    medium_list.append(time_user_optimized)
    
    return medium_list
    
def runLarge():
    large_list=[]
    global connection,cursor
    # we will hard code the database name, could also get from user

    db_path = os.getcwd()+"/A3Large.db"
    print(db_path)
    # create connection using function defined above
    connect(db_path)

    Uninformed()
    start=time.time()
    for i in range(0,50):
        query4()
    end=time.time()
    connection.close()
    time_uninformed=((end-start)/50)*1000
    large_list.append(time_uninformed)

    connect(db_path)
    #selfoptimized
    selfoptimized()
    start_02=time.time()
    for i in range(0,50):
        query4()
    end_02=time.time()
    connection.close()
    time_self_optimized=((end_02-start_02)/50)*1000
    large_list.append(time_self_optimized)

    connect(db_path)
    user_optimized()
    start_03=time.time()
    for i in range(0,50):
        query4()
    end_03=time.time()
    connection.close()
    time_user_optimized=((end_03-start_03)/50)*1000
    large_list.append(time_user_optimized)
    
    return large_list


def main():
    labels=["SmallDB","MediumDB","LargeDB"]
    list_01 = runSmall()
    list_02 = runMedium()
    list_03 = runLarge()

    uninformed_values=[]
    uninformed_values.append(list_01[0])
    uninformed_values.append(list_02[0])
    uninformed_values.append(list_03[0])
    
    self_optimized_values=[]
    self_optimized_values.append(list_01[1])
    self_optimized_values.append(list_02[1])
    self_optimized_values.append(list_03[1])
    
    user_optimized_values=[]
    user_optimized_values.append(list_01[2])
    user_optimized_values.append(list_02[2])
    user_optimized_values.append(list_03[2])
    
    print(uninformed_values)
    print(self_optimized_values)
    print(user_optimized_values)
    
    y1=np.array([elem for elem in uninformed_values])
    y2=np.array([elem for elem in self_optimized_values])
    y3=np.array([elem for elem in user_optimized_values])
    
    plt.bar(labels,y1)
    plt.bar(labels,y2,bottom=y1)
    plt.bar(labels,y3,bottom=y1+y2)
    plt.title("Query 4 (runtime in ms)")
    plt.legend(["Uninformed","Self Optimized", "User Optimized"])
    plt.show()
   
  
# run main method when program starts
if __name__ == "__main__":
    main()