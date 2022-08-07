import sqlite3
from datetime import datetime


def populateDB():
    conn = sqlite3.connect("database.sqlite3")

    cursor = conn.cursor()

    cursor.execute("DELETE FROM PRODUCT")
    cursor.execute("""DELETE FROM sqlite_sequence WHERE NAME == "product";""")
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
        cursor.execute(
            """INSERT INTO PRODUCT ("name", "genre", "price", "date_published", "quantity", "business_id") values (?, ?, ?, ?, ?, ?);""",
            (i["name"], i["genre"], i["price"], time, i["quantity"], i["business_id"]),
        )

    conn.commit()
    print("=========================== Records inserted ======================")

    conn.close()


def populationControl():
    pass


populateDB()
