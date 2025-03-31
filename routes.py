from flask import Flask, render_template, jsonify
from flask_sock import Sock
from touchpad_analyzer import TouchPadAnalyzer

app = Flask(__name__)
sock = Sock(app)

clients = set()  # 存储所有已连接的客户端
ta = TouchPadAnalyzer()  # 初始化 TouchPadAnalyzer

def register_routes(app: Flask):
    @app.route("/home")
    def home():
        return jsonify({"message": "Welcome to the app!"})

    @app.route("/status")
    def status():
        return jsonify({"status": "OK"})
    
    @app.route('/')
    def index():
        return render_template('index.html')

def websocket(ws):
    """WebSocket 路由逻辑"""
    print("WebSocket 路由被触发")
    clients.add(ws)
    try:
        while True:
            data = ws.receive()
            if data:
                # print(f"收到的数据: {data}")
                ta.process_data(data)
    except Exception as e:
        print('WebSocket 连接关闭或出现错误:', e)
    finally:
        clients.discard(ws)
        print("WebSocket 连接已关闭")

@sock.route('/ws')
def websocket_route(ws):
    websocket(ws)

if __name__ == '__main__':
    register_routes(app)
    app.run(debug=True,host='0.0.0.0', port=8888)
