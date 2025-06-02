import os
import json
from getpass import getpass  # 用于安全输入密码

def get_credentials_path():
    """获取存储凭证的完整路径（在上级文件夹中）"""
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取上级目录
    parent_dir = os.path.dirname(current_dir)
    # 返回上级目录中的凭证文件路径
    return os.path.join(parent_dir, 'user_credentials.json')

def save_credentials(username, password):
    """保存用户凭证到上级文件夹中的本地文件"""
    credentials = {
        'username': username,
        'password': password
    }
    try:
        credentials_path = get_credentials_path()
        with open(credentials_path, 'w') as f:
            json.dump(credentials, f)
        print("凭证保存成功")
    except Exception as e:
        print(f"保存凭证时出错: {e}")

def load_credentials():
    """从上级文件夹中的本地文件加载用户凭证"""
    try:
        credentials_path = get_credentials_path()
        if not os.path.exists(credentials_path):
            return None, None
            
        with open(credentials_path, 'r') as f:
            credentials = json.load(f)
            return credentials['username'], credentials['password']
    except Exception as e:
        print(f"加载凭证时出错: {e}")
        return None, None

def get_credentials(first_time=False):
    """获取用户凭证，如果是首次使用则提示保存"""
    if not first_time:
        username, password = load_credentials()
        if username and password:
            print("已找到保存的凭证，将自动使用")
            return username, password
    
    # 如果是首次使用或没有保存的凭证
    username = input("请输入您的学号：")
    password = getpass("请输入您的密码：")  # 使用getpass隐藏密码输入
    
    return username, password