from .connect import wrapper
import json
import psycopg2.extras

def insert(obj):
    def f(obj, c):
        c.execute("""INSERT INTO users (hash, username, created_at, description, api_key,
                  layer, public_key, private_key) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                  (obj["hash"], obj["username"], obj["created_at"], obj["description"],
                  obj["api_key"], obj["layer"], obj["public_key"], obj["private_key"]))
    wrapper(f, obj)

def select_by_timestamp(start, end):
    def f(start, end, c):
        c.execute("SELECT * FROM users WHERE created_at >= (%s) AND created_at <= (%s) ORDER BY created_at;", (start, end))
        return c.fetchall()
    return wrapper(f, start, end)

def query(target, value):
    def f(target, value, c):
        c.execute("SELECT * FROM users WHERE " + target + " = (%s);", (value,))
        return c.fetchall()
    return wrapper(f, target, value)

def select_by_username(username):
    def f(username, c):
        c.execute("SELECT * FROM users WHERE username = (%s);", (username,))
        return c.fetchone()
    return wrapper(f, username)

def select_by_hash(hash):
    def f(hash, c):
        c.execute("SELECT * FROM users WHERE hash = (%s);", (hash,))
        return c.fetchone()
    return wrapper(f, hash)

def select_by_layer(layer):
    def f(layer, c):
        c.execute("SELECT * FROM users WHERE layer = (%s);", (layer,))
        return c.fetchall()
    return wrapper(f, layer)

def get_user_amount():
    def f(c):
        c.execute("SELECT count(*) FROM users;")
        return c.fetchone()["count"]
    return wrapper(f)

def set_layer_by_username(username, layer):
    def f(username, layer, c):
        c.execute("UPDATE users SET layer = (%s) WHERE username = (%s);", (layer, username))
    wrapper(f, username, layer)
