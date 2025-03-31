// WebSocket 连接与自动重连
let socket;
let reconnectInterval = 1000;
let maxReconnectInterval = 10000;
let isReconnecting = false; // 防止多次重连

function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    socket = new WebSocket(protocol + window.location.host + '/ws');

    socket.onopen = () => {
        console.log('WebSocket 连接已建立');
        reconnectInterval = 1000;
        isReconnecting = false;
    };

    socket.onmessage = (event) => {
        console.log('收到消息:', event.data);
    };

    socket.onclose = () => {
        if (isReconnecting) return;
        isReconnecting = true;
        console.log('WebSocket 连接已关闭，尝试重连...');
        clearTouchPoints(); // 清理触摸点状态
        setTimeout(() => {
            isReconnecting = false;
            connectWebSocket();
        }, reconnectInterval);
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
    if (!Array.isArray(pts) || pts.some(p => typeof p.id !== 'number' || typeof p.x !== 'number' || typeof p.y !== 'number')) {
        console.warn('发送的数据格式无效:', pts);
        return;
    }

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
    const uniquePoints = Object.keys(touchPoints).map(id => ({ id: Number(id), ...touchPoints[id] }));
    sendAction('ts', uniquePoints);
    event.preventDefault();
}, { passive: true }); // 设置为被动监听器

touchpad.addEventListener('touchmove', (event) => {
    for (let touch of event.changedTouches) {
        touchPoints[touch.identifier] = { x: touch.clientX, y: touch.clientY };
    }
    const uniquePoints = Object.keys(touchPoints).map(id => ({ id: Number(id), ...touchPoints[id] }));
    sendAction('tm', uniquePoints);
    event.preventDefault();
}, { passive: true }); // 设置为被动监听器

touchpad.addEventListener('touchend', (event) => {
    const endedTouches = [];
    for (let touch of event.changedTouches) {
        endedTouches.push({ id: touch.identifier, x: touch.clientX, y: touch.clientY });
        delete touchPoints[touch.identifier];
    }
    const uniquePoints = Object.keys(touchPoints).map(id => ({ id: Number(id), ...touchPoints[id] }));
    sendAction('te', endedTouches);

    // 如果没有触摸点了，清零 touchPoints
    if (Object.keys(touchPoints).length === 0) {
        clearTouchPoints();
    }
    event.preventDefault();
});

document.getElementById('leftButton').addEventListener('click', () => {
    sendAction('ck', [], 'l');
});

document.getElementById('rightButton').addEventListener('click', () => {
    sendAction('ck', [], 'r');
});

window.onload = () => {
    const joystick = document.getElementById('joystick');
    if (!joystick) {
        console.error("Joystick 元素未找到");
        return;
    }

    const container = document.getElementById('middleSliderContainer');
    const containerHeight = container.offsetHeight;
    const joystickHeight = joystick.offsetHeight;
    const middlePosition = (containerHeight - joystickHeight) / 2;
    joystick.style.bottom = `${middlePosition}px`;

    let isDragging = false;
    let lastSentTime = 0;
    const throttleInterval = 50; // 限制每 50ms 发送一次消息

    joystick.addEventListener('mousedown', () => isDragging = true);
    document.addEventListener('mouseup', () => isDragging = false);
    document.addEventListener('mousemove', (event) => {
        if (!isDragging) return;

        const now = Date.now();
        if (now - lastSentTime < throttleInterval) return; // 节流逻辑
        lastSentTime = now;

        const containerRect = container.getBoundingClientRect();
        let newY = event.clientY - containerRect.top - joystickHeight / 2;
        newY = Math.max(0, Math.min(newY, container.offsetHeight - joystickHeight)); // 限制范围

        joystick.style.bottom = `${container.offsetHeight - newY - joystickHeight}px`;

        const value = Math.round(((container.offsetHeight - newY - joystickHeight) / (container.offsetHeight - joystickHeight)) * 200 - 100);
        sendAction('ms', [{ id: 0, x: 0, y: value }]);
    });

    joystick.addEventListener('dblclick', () => {
        joystick.style.bottom = `${middlePosition}px`;
        sendAction('ms', [{ id: 0, x: 0, y: 0 }]);
    });
};

// 清理全局变量 touchPoints
function clearTouchPoints() {
    touchPoints = {};
    console.log("触摸点状态已清理");
}

// 页面卸载时清理全局变量
window.addEventListener('beforeunload', () => {
    clearTouchPoints();
});
