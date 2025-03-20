// WebSocket 连接与自动重连
let socket;
let reconnectInterval = 1000;
let maxReconnectInterval = 10000;

// {
//     "t": "事件类型 (如 'ts' 表示 touchstart, 'tm' 表示 touchmove, 'te' 表示 touchend, 'ck' 表示点击, 'ms' 表示滑块移动)",
//     "ts": "时间戳 (毫秒)",
//     "pts": [
//         {"id": 触摸点ID, "x": X坐标(小数保留3位), "y": Y坐标(小数保留3位)}
//     ],
//     "btn": "点击事件的按钮类型 ('l' 表示左键, 'r' 表示右键)"
// }

function connectWebSocket() {
    socket = new WebSocket('ws://' + window.location.host + '/ws');

    socket.onopen = () => {
        console.log('WebSocket 连接已建立');
        reconnectInterval = 1000;
    };

    socket.onmessage = (event) => {
        console.log('收到消息:', event.data);
    };

    socket.onclose = () => {
        console.log('WebSocket 连接已关闭，尝试重连...');
        setTimeout(connectWebSocket, reconnectInterval);
        reconnectInterval = Math.min(reconnectInterval * 2, maxReconnectInterval);
    };

    socket.onerror = (error) => {
        console.error('WebSocket 错误:', error);
        socket.close();
    };
}

connectWebSocket();

const touchpad = document.getElementById('touchpad');
let touchPoints = {};

function sendAction(t, pts = [], btn = null) {
    const data = {
        t: t,
        ts: Date.now(),
        pts: pts.map(p => ({
            id: p.id,
            x: +p.x.toFixed(3),
            y: +p.y.toFixed(3)
        }))
    };
    if (btn) data.btn = btn;

    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(data));
        console.log('发送的数据:', data);
    } else {
        console.warn('WebSocket 连接未打开，消息未发送');
    }
}

touchpad.addEventListener('touchstart', (event) => {
    for (let touch of event.changedTouches) {
        touchPoints[touch.identifier] = { x: touch.clientX, y: touch.clientY };
    }
    sendAction('ts', Object.keys(touchPoints).map(id => ({ id: Number(id), ...touchPoints[id] })));
    event.preventDefault();
});

touchpad.addEventListener('touchmove', (event) => {
    for (let touch of event.changedTouches) {
        touchPoints[touch.identifier] = { x: touch.clientX, y: touch.clientY };
    }
    sendAction('tm', Object.keys(touchPoints).map(id => ({ id: Number(id), ...touchPoints[id] })));
    event.preventDefault();
});

touchpad.addEventListener('touchend', (event) => {
    for (let touch of event.changedTouches) {
        delete touchPoints[touch.identifier];
    }
    sendAction('te', Object.keys(touchPoints).map(id => ({ id: Number(id), ...touchPoints[id] })));
    event.preventDefault();
});

document.getElementById('leftButton').addEventListener('click', () => {
    sendAction('ck', [], 'l');
});

document.getElementById('rightButton').addEventListener('click', () => {
    sendAction('ck', [], 'r');
});

const joystick = document.getElementById('joystick');
let isDragging = false;
joystick.addEventListener('mousedown', () => isDragging = true);
document.addEventListener('mouseup', () => isDragging = false);
document.addEventListener('mousemove', (event) => {
    if (!isDragging) return;
    const container = joystick.parentElement;
    const containerRect = container.getBoundingClientRect();
    const joystickHeight = joystick.offsetHeight;
    let newY = event.clientY - containerRect.top - joystickHeight / 2;
    newY = Math.max(0, Math.min(newY, container.offsetHeight - joystickHeight));
    joystick.style.bottom = `${container.offsetHeight - newY - joystickHeight}px`;
    const value = Math.round(((container.offsetHeight - newY - joystickHeight) / (container.offsetHeight - joystickHeight)) * 200 - 100);
    sendAction('ms', [{ id: 0, x: 0, y: value }]);
});

joystick.addEventListener('dblclick', () => {
    const container = joystick.parentElement;
    const containerHeight = container.offsetHeight;
    const joystickHeight = joystick.offsetHeight;
    const middlePosition = (containerHeight - joystickHeight) / 2;
    joystick.style.bottom = `${middlePosition}px`;
    sendAction('ms', [{ id: 0, x: 0, y: 0 }]);
});

window.onload = () => {
    const container = document.getElementById('middleSliderContainer');
    const joystick = document.getElementById('joystick');
    const containerHeight = container.offsetHeight;
    const joystickHeight = joystick.offsetHeight;
    const middlePosition = (containerHeight - joystickHeight) / 2;
    joystick.style.bottom = `${middlePosition}px`;
};
