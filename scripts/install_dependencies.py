import os
import subprocess

def install_dependencies():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    requirements_file = os.path.join(project_root, "requirements.txt")
    
    if os.path.exists(requirements_file):
        try:
            subprocess.check_call(["pip", "install", "-r", requirements_file])
            print("依赖安装完成！")
        except subprocess.CalledProcessError as e:
            print(f"安装依赖时出错: {e}")
    else:
        print(f"未找到 {requirements_file} 文件，请确保它存在于项目根目录。")

if __name__ == "__main__":
    install_dependencies()
