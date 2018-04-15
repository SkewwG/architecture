# hello.py
from urllib.parse import parse_qs
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.pcc
user_set = db.user
like_set = db.like
friends_set = db.friends



def action_like(uid, oid):
    like_list = like_set.find_one({'oid': oid})['uids']
    body = {'oid': oid, 'uid': uid, 'list_list': like_list}
    return str(body)

def action_is_like(uid, oid):
    like_list = like_set.find_one({'oid': oid})['uids']
    is_like = 1 if uid in like_list else 0
    body = {'oid': oid, 'uid': uid, 'is_like': is_like}
    return str(body)

def action_count(uid, oid):
    like_list = like_set.find_one({'oid': oid})['uids']
    count = len(like_list)
    body = {'oid': oid, 'count': count}
    return str(body)

def action_list(uid, oid):
    body = {'oid': oid, 'list_list': [{"1":"nickname"},{"2","Jerry"}], 'next_cursor': 1234}
    return str(body)

def error(uid, oid):
    body = {"error_code": 501, "error_message": "object already been liked.", "oid": uid, "uid": oid}
    return str(body)

# 替代if elif else语句
fun = {'like': action_like, 'is_like': action_is_like, 'count': action_count}

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    q = parse_qs(environ['QUERY_STRING'])
    action, uid, oid = q['action'][0], q['uid'][0], q['oid'][0]
    return [fun[action](uid, oid).encode('utf-8')]
