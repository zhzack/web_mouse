from flask import Flask
from routes import register_routes, websocket  # 导入 WebSocket 路由
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)  # 初始化 Flask-Sock

# 注册 HTTP 路由
register_routes(app)

# 注册 WebSocket 路由
sock.route('/ws')(websocket)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)
