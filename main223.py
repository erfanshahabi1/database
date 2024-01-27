#!/usr/bin/env python
"""
Licensed under the MIT Licence, Copyright (c) 2014 Sinch AB

This demonstrates a basic partner backend for generating authentication tokens.
In this example the user database is persistent using sqlite3.
See rows ~100-120 for code on generating a Sinch compatible authentication token.
"""
import tornado.ioloop
import tornado.web
from tornado.web import Finish
from datetime import datetime
import json
import uuid
import hmac
import hashlib
import base64
import sqlite3  # import sqlite3 module

# Port
HTTP_PORT = 2048

# App key + secret
APPLICATION_KEY = 'INSERT_YOUR_APP_KEY_HERE'
APPLICATION_SECRET = 'INSERT_YOUR_APP_SECRET_HERE'
userBase = dict()
# Database file
DB_FILE = 'user_db.sqlite'

# Create a connection to the database file
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Create a table for users if not exists
cur.execute('CREATE TABLE IF NOT EXISTS users (username VARCHAR, salt VARCHAR, password VARCHAR)')
conn.commit()


# Generate Sinch authentication ticket. Implementation of:
# http://www.sinch.com/docs/rest-apis/api-documentation/#Authorization
def getAuthTicket(user):
    userTicket = {
        'identity': {'type': 'username', 'endpoint': user['username']},
        'expiresIn': 3600,  # 1 hour expiration time of session when created using this ticket
        'applicationKey': APPLICATION_KEY,
        'created': datetime.utcnow().isoformat()
    }

    userTicketJson = json.dumps(userTicket).replace(" ", "")
    userTicketBase64 = base64.b64encode(userTicketJson)

    # TicketSignature = Base64 ( HMAC-SHA256 ( ApplicationSecret, UTF8 ( UserTicketJson ) ) )
    digest = hmac.new(base64.b64decode(
        APPLICATION_SECRET), msg=userTicketJson, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)

    # UserTicket = TicketData + ":" + TicketSignature
    signedUserTicket = userTicketBase64 + ':' + signature
    return {'userTicket': signedUserTicket}


# REST endpoints
class PingHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def get(self):
        self.write('pong')


class RestResource(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def write_error(self, status_code, **kwargs):
        data = {}
        for key, value in kwargs.iteritems():
            data[key] = value
        try:
            del data['exc_info']
        except:
            pass

        self.write(json.dumps(data))
        self.set_status(status_code)
        raise Finish()


class RegisterHandler(RestResource):

    def post(self):
        user = json.loads(self.request.body)

        if 'username' not in user:
            self.write_error(400, errorCode=40001, message='username not found')
        if 'password' not in user:
            self.write_error(400, errorCode=40002, message='password not found')

        # Check if user exists in the database
        cur.execute('SELECT * FROM users WHERE username = ?', (user['username'],))
        if cur.fetchone():
            self.write_error(400, errorCode=40003, message='user already registered')

        salt = uuid.uuid4().hex
        password = hashlib.sha256(
            salt + user['password'] + '31337 salted').hexdigest()

        # Insert user into the database
        cur.execute('INSERT INTO users (username, salt, password) VALUES (?, ?, ?)', (user['username'], salt, password))
        conn.commit()

        print('Created user, now the user base is:')
        for row in cur.execute('SELECT * FROM users'):
            print('\t' + row[0] + '\t' + row[2])

        self.write(json.dumps(getAuthTicket(user)))


class LoginHandler(RestResource):

    def post(self):
        user = json.loads(self.request.body)

        if 'username' not in user:
            self.write_error(400, errorCode=40001, message='username not found')
        if 'password' not in user:
            self.write_error(400, errorCode=40002, message='password not found')
        if user['username'] not in userBase:
            self.write_error(400, errorCode=40004, message='user not registered')

        salt = userBase[user['username']][0]
        correctPassHash = userBase[user['username']][1]
        candidatePassHash = hashlib.sha256(
            salt + user['password'] + '31337 salted').hexdigest()

        if candidatePassHash != correctPassHash:
            self.write_error(401, errorCode=40100, message='incorrect password')
        elif candidatePassHash == correctPassHash:  # Correct password
            self.write(json.dumps(getAuthTicket(user)))


backend = tornado.web.Application([
    (r"/ping", PingHandler),
    (r"/register", RegisterHandler),
    (r"/login", LoginHandler),
])

if __name__ == "__main__":

    print ("Starting Sinch demo backend on port: \033[1m" + str(HTTP_PORT) +'\033[0m')
    print ("Application key: \033[1m" + APPLICATION_KEY +'\033[0m')
    print ("Post JSON object to \033[1m/register\033[0m to create user")
    print ("Post JSON object to \033[1m/login\033[0m to retrieve authentication token")
    print ("Example JSON: {username: 'someUserName', password: 'highlySecurePwd'}")
    print ("--- LOG ---")
    conn.close()
    backend.listen(HTTP_PORT)
    tornado.ioloop.IOLoop.instance().start()