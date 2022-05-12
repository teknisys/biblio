import sqlite3

conn = sqlite3.connect("database.sqlite3")
from datetime import datetime

cursor = conn.cursor()

conn.execute("DELETE FROM PRODUCT")
conn.execute("""DELETE FROM sqlite_sequence WHERE NAME == "product";""")
conn.commit()
print("=========================== Deleted all Previous Records ==========")

values = [
    {
        "name": "1984",
        "genre": "fiction",
        "price": 20,
        "quantity": 10,
        "business_id": 1,
    },
    {
        "name": "And Then There Were None",
        "genre": "thriller",
        "price": 30,
        "quantity": 10,
        "business_id": 1,
    },
    {
        "name": "Hitchhiker's Guide to Galaxy",
        "genre": "fiction",
        "price": 40,
        "quantity": 10,
        "business_id": 1,
    },
    {
        "name": "11.22.63",
        "genre": "thriller",
        "price": 50,
        "quantity": 10,
        "business_id": 1,
    },
    {
        "name": "Animal Farm",
        "genre": "fiction",
        "price": 70,
        "quantity": 10,
        "business_id": 1,
    },
]
time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
for i in values:
    conn.execute(
        """INSERT INTO PRODUCT ("name", "genre", "price", "date_published", "quantity", "business_id") values (?, ?, ?, ?, ?, ?);""",
        (i["name"], i["genre"], i["price"], time, i["quantity"], i["business_id"]),
    )


# Commit your changes in the database
conn.commit()
print("=========================== Records inserted ======================")

conn.close()
