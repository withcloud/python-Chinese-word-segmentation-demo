import eventlet
import socketio
from snownlp import SnowNLP
import jieba
import argparse
import json

sio = socketio.Server()
app = socketio.WSGIApp(sio)

# 1. jieba
r1 = jieba.cut("你好", cut_all=False)
# ...

# 2. snownlp
r2 = SnowNLP("你好")

# final save and print
# { result1, result2 }
data = {
    "result1": {
        "words": list(r1)
    },
    "result2": {
        "sentiments": r2.sentiments,
        "words": r2.words,
        "sentiments": r2.sentiments,
    }
}
print(data)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)
    # 1. jieba
    r1 = jieba.cut(data, cut_all=False)
    # ...

    # 2. snownlp
    r2 = SnowNLP(data)

    # final save and print
    # { result1, result2 }
    result = {
        "result1": {
            "words": list(r1)
        },
        "result2": {
            "sentiments": r2.sentiments,
            "words": r2.words,
            "sentiments": r2.sentiments,
        }
    }
    print(result)
    sio.emit('my response', {'response': result})
    print('message end ')

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 3000)), app)