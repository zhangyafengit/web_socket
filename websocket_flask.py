from flask import Flask, request,render_template
from geventwebsocket.websocket import WebSocket
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

app = Flask(__name__,template_folder='template')

# 首先我们程序进来之后访问index返回一个ws页面。
@app.route('/index')
def index():
    return render_template("ws.html")

user_socket_list = []


@app.route('/ws')
def ws():
    user_socket = request.environ.get('wsgi.websocket')
    print(request.environ)
    print(user_socket)
    if not user_socket:
        return "请使用WebSocket方式连接"
    user_socket_list.append(user_socket)
    print(user_socket_list)
    while True:
        user_msg = user_socket.receive()
        print(user_msg)
        for i in user_socket_list:
            if user_socket == i:       # 也就是自己给自己发，跳过。
                continue

            i.send(user_msg)
            # send_msg=input('input you word>>>>:')
            # user_socket.send(send_msg)


if __name__ == '__main__':
    http_serv = WSGIServer(('127.0.0.1', 9520), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
