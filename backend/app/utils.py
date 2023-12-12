from flask import request
import session
import threading
import time
from queue import Queue


def check_csrf_token(token):
    if token == session.get('csrf_token'):
        return True
    return False


def dispatch():
    pass

