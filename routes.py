from flask import Flask, render_template
from flask_sock import Sock
from touchpad_analyzer import TouchPadAnalyzer

app = Flask(__name__)
sock = Sock(app)

clients = set()  # 存储所有已连接的客户端


@app.route('/')
def index():
    return render_template('index.html')

@sock.route('/ws')
def websocket(ws):
    clients.add(ws)
    try:
        while True:
            data = ws.receive()
            if data:
                print('收到的数据:', data)
                ta.process_data(data)
                # 可以在这里处理数据或广播给所有客户端
    except Exception as e:
        print('WebSocket 连接关闭或出现错误:', e)
    finally:
        clients.discard(ws)


if __name__ == '__main__':
    ta = TouchPadAnalyzer()
    app.run(debug=True,host='0.0.0.0', port=5000)
