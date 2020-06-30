import psycopg2

def connectdb(dbname="scoin"):
    try:
        db = psycopg2.connect(database="scoin", user="scoin", password="scoinsodope", host="127.0.0.1", port="5432")
        return db
    except psycopg2.OperationalError as e:
        print("Error connecting database: %s" % (e))

