from flask import Flask, send_file, jsonify
import json

app = Flask(__name__)


@app.route("/index/<filename>")  # 会通过filename将文件发送过去。
def index(filename):
    return send_file(filename)


@app.route("/json")
def get_json():
    res = {
        "user_id": 1,
        "password": "123123"
    }

    return jsonify(res)   # 返回一个序列化的数据结构。


if __name__ == '__main__':
    app.run()
