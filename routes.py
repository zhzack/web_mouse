from flask import Blueprint, request, jsonify, render_template
import socket
import threading
import config

main_routes = Blueprint('main', __name__)

# 启动 UDP 监听
def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((config.UDP_IP, config.UDP_PORT))
    while True:
        data, addr = sock.recvfrom(1024)
        print("Received message:", data.decode(), "from", addr)

# 启动 UDP 监听线程
threading.Thread(target=udp_listener, daemon=True).start()

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({'status': 'success', 'message': 'Heartbeat received'})

@main_routes.route('/action', methods=['POST'])
def handle_action():
    data = request.json  # 获取 JSON 数据
    action = data.get('action')
    details = data.get('details')
    print('Action received:', action, details)

    # 发送 UDP 消息
    send_udp(action, details)

    return jsonify({'status': 'success', 'message': 'Action received'})

def send_udp(action, details=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"{action}: {details}" if details else action
    sock.sendto(message.encode(), (config.UDP_IP, config.UDP_PORT))
