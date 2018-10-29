from flask import Flask, request, render_template
from geventwebsocket.websocket import WebSocket
from geventwebsocket.websocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

import json

app = Flask(__name__,template_folder='template')


@app.route("/index")
def index():
    return render_template("pri_chat.html")

user_socket_list = []
user_socket_dict = {}


@app.route("/ws/<username>")
def ws(username):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if not user_socket:
        return "请使用WebSocket方式连接"
    user_socket_dict[username] = user_socket   # 我们在这里保存用户名与socket连接。
    print(user_socket_dict)
    while True:
        try:
            user_msg = user_socket.receive()   # 接收消息。
            user_msg=json.loads(user_msg)      # 反序列化消息。
            to_user_socket=user_socket_dict.get(user_msg.get("to_user")) # 从前端发过来的数据中取到消息目的用户。
            send_msg={
                "send_msg":user_msg.get("send_msg"),
                "send_user":username}          # 序列胡发送的数据。

            to_user_socket.send(json.dumps(send_msg))  # 序列化数据。
            # for user_name, u_socket in user_socket_dict.items():
            #     who_send_msg = {
            #         "send_user": username,
            #         "send_msg": user_msg
            #     }
            #     if user_socket == u_socket:
            #         continue
            #     u_socket.send(json.dumps(who_send_msg))
        except WebSocketError as e:
            user_socket_dict.pop(username)
            print(user_socket_dict)
            print(e)


if __name__ == '__main__':
    # app.run("0.0.0.0",9527,debug=True)
    http_serv = WSGIServer(("127.0.0.1", 9521), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
