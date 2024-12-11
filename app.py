from flask import Flask
from routes import main_routes

app = Flask(__name__)

# 注册路由
app.register_blueprint(main_routes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
