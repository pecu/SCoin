from .connect import wrapper
import json
import psycopg2.extras

def insert(obj):
    def f(obj, c):
        c.execute("""INSERT INTO transactions 
                  (hash, sender, receiver, description, timestamp, spent) VALUES (%s, %s, %s, %s, %s, %s);""",
                  (obj["hash"], obj["sender"], obj["receiver"], obj["description"], obj["timestamp"], obj["spent"]))
    wrapper(f, obj)


def select_by_timestamp(start, end):
    def f(start, end, c):
        c.execute("SELECT * FROM transactions WHERE timestamp >= (%s) AND timestamp <= (%s) ORDER BY timestamp;", (start, end))
        return c.fetchall()
    return wrapper(f, start, end)

def select_by_hash(hash):
    def f(hash, c):
        c.execute("SELECT * FROM transactions WHERE hash = (%s);", (hash,))
        return c.fetchone()
    return wrapper(f, hash)

def select_unspent_by_username(username):
    def f(hash, c):
        c.execute("SELECT * FROM transactions WHERE receiver = (%s) AND spent = '0';", (username,))
        return c.fetchall()
    return wrapper(f, hash)

def spend_transaction(hash):
    def f(hash, c):
        c.execute("UPDATE transactions SET spent = '1' WHERE hash = (%s);", (hash,))
    return wrapper(f, hash)
