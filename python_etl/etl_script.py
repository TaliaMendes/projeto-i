import pandas as pd
import psycopg2
import math
from pymongo import MongoClient

#conectando com o banco de dados no postgress
conn = psycopg2.connect(
    dbname="projeto-1",
    user="root",
    password="root",
    host="postgres",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_product (
    product_id VARCHAR PRIMARY KEY,
    product_category_name VARCHAR,
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id VARCHAR PRIMARY KEY,
    customer_unique_id VARCHAR,
    customer_zip_code_prefix VARCHAR,
    customer_city VARCHAR,
    customer_state VARCHAR
)
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_payment (
    payment_id SERIAL PRIMARY KEY,
    order_id VARCHAR REFERENCES fact_irder(order_id),
    payment_sequential INT,
    payment_type VARCHAR,
    payment_installments INT,
    payment_value DECIMAL
)
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_item (
        item_id SERIAL PRIMARY KEY,
        order_id VARCHAR,
        order_item_id VARCHAR,
        product_id VARCHAR REFERENCES dim_product(product_id),
        seller_id VARCHAR,
        shipping_limit_date TIMESTAMP,
        price DECIMAL,
        freight_value DECIMAL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS fact_order (
        order_id VARCHAR PRIMARY KEY,
        customer_id VARCHAR REFERENCES dim_customer(customer_id),
        order_status VARCHAR,
        order_purchase_timestamp TIMESTAMP,
        order_approved_at TIMESTAMP,
        order_delivered_carrier_date TIMESTAMP,
        order_delivered_customer_date TIMESTAMP,
        order_estimated_delivery_date TIMESTAMP
    );
""")


tabela1 = pd.read_csv("/input/olist_products_dataset.csv",sep=',')
for _, row in tabela1.iterrows():
    values = []
    for item in row: 
        if isinstance(item, float) and not math.isnan(item):
            values.append(int(item))
        else:
            values.append(item if item == item else None)
    cursor.execute(
        "INSERT INTO dim_product VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        tuple(values)
    )

tabela2 = pd.read_csv("/input/olist_customers_dataset.csv",sep=',')
for _, row in tabela2.iterrows():
    values = []
    for item in row: 
        if isinstance(item, float) and not math.isnan(item):
            values.append(int(item))
        else:
            values.append(item if item == item else None)
    cursor.execute(
        "INSERT INTO dim_customer VALUES (%s,%s,%s,%s,%s)",
        tuple(values)
    )


tabela3 = pd.read_csv("/input/olist_order_payments_dataset.csv",sep=',')
for _, row in tabela3.iterrows():
    values = []
    for item in row: 
        if isinstance(item, float) and not math.isnan(item):
            values.append(int(item))
        else:
            values.append(item if item == item else None)
    cursor.execute(
        "INSERT INTO dim_payment(order_id,payment_sequential,payment_type,payment_installments,payment_value) VALUES (%s,%s,%s,%s,%s)",
        tuple(values)
    )

tabela4 = pd.read_csv("/input/olist_order_items_dataset.csv",sep=',')
for _, row in tabela4.iterrows():
     values = []
     for item in row: 
         if isinstance(item, float) and not math.isnan(item):
             values.append(int(item))
         else:
             values.append(item if item == item else None)
     cursor.execute(
         "INSERT INTO dim_item(order_id,order_item_id,product_id,seller_id,shipping_limit_date,price,freight_value) VALUES (%s,%s,%s,%s,%s,%s,%s)",
         tuple(values)
     )


tabela5 = pd.read_csv("/input/olist_orders_dataset.csv",sep=',')
for _, row in tabela5.iterrows():
     values = []
     for item in row: 
         if isinstance(item, float) and not math.isnan(item):
             values.append(int(item))
         else:
             values.append(item if item == item else None)
     cursor.execute(
         "INSERT INTO fact_order VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
         tuple(values)

     )

     cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_reviews (
        review_id VARCHAR PRIMARY KEY,
        order_id VARCHAR,
        review_score INT,
        review_comment_title VARCHAR,
        review_comment_message TEXT,
        review_creation_date TIMESTAMP,
        review_answer_timestamp TIMESTAMP
    );
""")

mongo_client = MongoClient('mongodb://mongodb:27017/')

mongo_db = mongo_client['ecommerce']

mongo_collection = mongo_db['order_reviews']

cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_reviews (
        review_id VARCHAR PRIMARY KEY,
        order_id VARCHAR,
        review_score INT,
        review_comment_title VARCHAR,
        review_comment_message TEXT,
        review_creation_date TIMESTAMP,
        review_answer_timestamp TIMESTAMP
    );
""")

sql_insert = """
    INSERT INTO order_reviews (
        review_id, order_id, review_score,
        review_comment_title, review_comment_message,
        review_creation_date, review_answer_timestamp
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
for document in mongo_collection.find():
    values = (
        document['review_id'],
        document['order_id'],
        int(document['review_score']),
        document['review_comment_title'],
        document['review_comment_message'],
        document['review_creation_date'],
        document['review_answer_timestamp']
    )
    cursor.execute(sql_insert, values)

conn.commit()

cursor.close()
conn.close()
