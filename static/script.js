// 心跳信息发送
setInterval(() => {
    sendHeartbeat();
}, 10000);

function sendHeartbeat() {
    // 发送心跳信息
    fetch('/heartbeat')
        .then(response => response.text())
        .then(data => console.log('Heartbeat sent:', data));
}


const touchpad = document.getElementById('touchpad');
let touchPoints = {};

touchpad.addEventListener('touchstart', (event) => {
    console.log('1');
    for (let touch of event.changedTouches) {
        touchPoints[touch.identifier] = { x: touch.clientX, y: touch.clientY };
    }
    sendAction('touchstart', touchPoints);
    event.preventDefault();
});

touchpad.addEventListener('touchmove', (event) => {
    console.log('2');
    for (let touch of event.changedTouches) {
        touchPoints[touch.identifier] = { x: touch.clientX, y: touch.clientY };
    }
    sendAction('touchmove', touchPoints);
    event.preventDefault();
});

touchpad.addEventListener('touchend', (event) => {
    console.log('3');
    for (let touch of event.changedTouches) {
        delete touchPoints[touch.identifier];
    }
    sendAction('touchend', touchPoints);
    event.preventDefault();
});


document.getElementById('leftButton').addEventListener('click', () => {
    console.log('左键点击');
    sendAction('leftClick');
});

document.getElementById('rightButton').addEventListener('click', () => {
    console.log('右键点击');
    sendAction('rightClick');
});

const joystick = document.getElementById('joystick');
let isDragging = false;

joystick.addEventListener('mousedown', (event) => {
    isDragging = true;
});

document.addEventListener('mouseup', () => {
    isDragging = false;
});

document.addEventListener('mousemove', (event) => {
    if (!isDragging) return;

    const container = joystick.parentElement;
    const containerRect = container.getBoundingClientRect();
    const joystickHeight = joystick.offsetHeight;
    let newY = event.clientY - containerRect.top - joystickHeight / 2;

    // 限制操作杆的移动范围
    newY = Math.max(0, Math.min(newY, container.offsetHeight - joystickHeight));
    
    joystick.style.bottom = `${container.offsetHeight - newY - joystickHeight}px`;

    // 计算当前值并发送
    const value = Math.round(((container.offsetHeight - newY - joystickHeight) / (container.offsetHeight - joystickHeight)) * 200 - 100); // 计算值范围为 -100 到 100
    sendAction('middleSlider', value);
});

// 双击操作杆重置为0
joystick.addEventListener('dblclick', () => {
    const container = joystick.parentElement;
    const containerHeight = container.offsetHeight;
    const joystickHeight = joystick.offsetHeight;

    // 计算中间位置
    const middlePosition = (containerHeight - joystickHeight) / 2;
    joystick.style.bottom = `${middlePosition}px`; // 重置操作杆到中间位置

    sendAction('middleSlider', 0); // 发送重置值
});

window.onload = function() {
    const container = document.getElementById('middleSliderContainer');
    const joystick = document.getElementById('joystick');

    const containerHeight = container.offsetHeight;
    const joystickHeight = joystick.offsetHeight;

    // 计算中间位置
    const middlePosition = (containerHeight - joystickHeight) / 2;
    joystick.style.bottom = `${middlePosition}px`; // 设置操作杆的初始位置
};




function sendAction(action, details = null) {
    const data = { action: action, details: details };
    fetch('/action', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => {
            if (response.ok) {
                return response.json(); // 确保处理为 JSON
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .then(data => {
            console.log('Action sent:', data);
        })
        .catch(error => console.error('Error sending action:', error));
}
