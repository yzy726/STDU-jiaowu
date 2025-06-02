from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .src.user import get_credentials
from .src.user import get_credentials_path
from .src.user import save_credentials
from .src.login import login_with_selenium
from .src.login import loginn_with_selenium
from .src.Sesrch_Exams import kscx
from .src.Sesrch_Exams import display_exam_schedule
from .src.Sesrch_Schedule import kbcx
from .src.Sesrch_Schedule import wjbc
from .src.Sesrch_Score import cjcx
from .src.Sesrch_Score import display_student_grades
from .src.Show_Schedule import show_current_week_courses


# 全局状态管理类
class GlobalState:
    def __init__(self):
        self.driver = None
        self.main_window_handle = None
        self.current_window_handle = None

# 创建全局状态实例
global_state = GlobalState()

Countinue = 0

SEMESTER_START_DATE = datetime(2025, 2, 17)  # 本学期开学时间

if __name__ == "__main__":
    
    # 检查是否是首次运行
    first_time = not os.path.exists(get_credentials_path())
    
    # 获取凭证
    username, password = get_credentials(first_time)
    
    # 设置 Chrome 选项
    chrome_options = Options()

    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建下载目录的路径
    download_dir = os.path.join(script_dir, 'download')
    
    # 确保下载目录存在
    os.makedirs(download_dir, exist_ok=True)
     
    # 配置 Chrome 选项
    chrome_prefs = {
        'download.default_directory': download_dir,  # 设置下载目录
        'download.prompt_for_download': False,      # 禁用下载提示
        'download.directory_upgrade': True,         # 确保下载目录升级
        'safebrowsing.enabled': True                # 启用安全浏览
    }
     
    chrome_options.add_experimental_option('prefs', chrome_prefs)
    chrome_options.add_argument('--log-level=3')    # 0=INFO, 1=WARNING, 2=ERROR, 3=FATAL
    chrome_options.add_argument('--headless')       # 启用无头模式
    chrome_options.add_argument('--disable-gpu')    # 通常与无头模式一起使用，禁用 GPU 加速
    chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口大小
 
    # 初始化 WebDriver
    global_state.driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 统一登录
        cookies = login_with_selenium(username, password, global_state.driver)
        if cookies:
            print("登录成功")
            Countinue = 1
            if first_time:
                save = input("是否要保存您的凭证以便下次使用？(y/n): ").lower()
                if save == 'y':
                    save_credentials(username, password)
            cookiess = loginn_with_selenium(username, password, global_state.driver)
            # 保存主窗口句柄到全局状态
            global_state.main_window_handle = global_state.driver.current_window_handle
            global_state.current_window_handle = global_state.main_window_handle
            
            # 检查是否成功获取 Cookie
            if cookiess:
                print("登录成功，Cookie:", cookiess)
            else:
                print("登录失败，请重新运行该程序。。")
        else:
            print("登录失败，请重新运行该程序。")
    except Exception as e:
        print(f"程序运行出错: {e}")
    
    if Countinue == 1:
        try:
            while True:
                # 打印菜单选项
                print("\n请选择要执行的操作：")
                print("1. 查看课程表")
                print("2. 查看考试安排")
                print("3. 查看成绩")
                print("4. 退出程序")
    
                # 获取用户输入
                choice = input("请输入您的选择（1-4）：")
    
                if choice == '1':
                    # 调用查看课程表的函数
                    kbcx(global_state.driver)
                    excel_origon_path = download_dir
                    renamed_file = wjbc(excel_origon_path, global_state.driver, global_state.main_window_handle)
                    global_state.driver.close()
                    global_state.driver.switch_to.window(global_state.main_window_handle)
                    show_current_week_courses(renamed_file, SEMESTER_START_DATE)
                elif choice == '2':
                    # 调用查看考试安排的函数
                    kaoshifile = kscx(global_state.driver)
                    excel_path1 = fr'{download_dir}\{kaoshifile}.xlsx'
                    global_state.driver.close()
                    global_state.driver.switch_to.window(global_state.main_window_handle)
                    display_exam_schedule(global_state.driver, excel_path1, global_state.main_window_handle)
                elif choice == '3':
                    # 调用查看成绩的函数
                    chengjifile = cjcx(global_state.driver)
                    excel_path2 = fr'{download_dir}\{chengjifile}.xlsx'
                    display_student_grades(global_state.driver, excel_path2, global_state.main_window_handle)
                    global_state.driver.close()
                    global_state.driver.switch_to.window(global_state.main_window_handle)
                elif choice == '4':
                    # 退出程序
                    print("程序退出。")
                    break
                else:
                    # 输入无效选项
                    print("无效的输入，请输入1-4之间的数字。")
    
        except Exception as e:
            print(f"发生错误: {str(e)}")

    global_state.driver.quit()
