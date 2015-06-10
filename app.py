# import the Flask class from the flask module
from flask import Flask, render_template,session, redirect, url_for, request
import smtplib, imaplib, os, sys, time
from gevent import monkey
from socketio.server import SocketIOServer
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
    if 'username' in session :
         return render_template('index.html')  # render a template
    return render_template('login.html')
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session :
	return render_template('index.html')
    if request.method == 'POST':
        if request.form['username'] != 'admin@gmail.com' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
	    session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)



@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'/chat': ChatNamespace}, request)
    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

app.secret_key = 'A0Zr98j-3yX?R~XHH!j9p1LWX/azRT'
# start the server with the 'run()' method

class ChatNamespace(BaseNamespace, BroadcastMixin):
    def initialize(self):
        self.logger = app.logger
        self.log("Socketio session started")

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def recv_connect(self):
        self.log("New connection")

    def recv_disconnect(self):
        self.log("Client disconnected")

    def on_join(self, email):
        self.log("%s joined chat" % email)
	self.session['email'] = email
        return True, email

    def on_message(self, message):
        self.log('got a message: %s' % message)
        self.broadcast_event_not_me("message",{ 
        "sender" : self.session["email"], 
        "content" : message})
	self.broadcast_event_not_me("message", message)
        return True, message

if __name__ == '__main__':
    #app.run(debug=True)
    handler = RotatingFileHandler('chat.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    SocketIOServer(
        ('',5000), 
        app,
        resource="socket.io").serve_forever()

