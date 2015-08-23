"""
This script runs the FlaskRestTest application using a development server.
"""

from os import environ
from FlaskRestTest import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int('5555')
    except ValueError:
        PORT = 5555
    app.debug = True
    app.run(HOST, PORT)
