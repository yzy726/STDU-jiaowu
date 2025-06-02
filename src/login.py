## 登录函数

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

global_window_handle = None

# 定义一个函数，用于通过 Selenium 自动化登录
def login_with_selenium(username, password, driver):
    # 打开指定的 URL
    driver.get('https://jw.stdu.edu.cn/xtgl/login_slogin.html')

    try:
        # 等待用户名输入框加载并变为可交互，最多等待 10 秒
        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'username'))
        )
        # 在用户名输入框中输入用户名
        username_field.send_keys(username)

        # 等待密码输入框加载并变为可交互，最多等待 10 秒
        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ppassword'))  # 使用 ID 定位密码输入框
        )
        # 在密码输入框中输入密码
        password_field.send_keys(password)

        # 等待登录按钮加载并变为可交互，最多等待 10 秒
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'dl'))
        )
        # 点击登录按钮
        login_button.click()

        # 获取打开的多个窗口句柄
        windows = driver.window_handles
        # 切换到当前最新打开的窗口
        driver.switch_to.window(windows[-1])
        windows_current = driver.current_window_handle

        # if windows_current == windows :
        #     print("账号或密码错误，请检查后重试！")
        #     driver.quit()
        #     # 返回 None，表示登录失败
        #     return None

        error_elements = driver.find_elements("id", "errormsg")
        if error_elements:
            print("请检查您输入的账号和密码")
            return None

        # 获取当前页面的所有 Cookie
        cookies = driver.get_cookies()
        
        # 返回获取到的 Cookie
        return cookies

    except TimeoutException:
        # 如果发生超时异常，打印提示信息
        print("登录超时，请检查网络或凭证。")
        # 关闭浏览器
        driver.quit()
        # 返回 None，表示登录失败
        return None

# 定义一个函数，用于通过 Selenium 自动化登录
def loginn_with_selenium(username, password, driver):
    global global_window_handle  # 声明使用全局变量

    try:
        # 等待用户名输入框加载并变为可交互，最多等待 10 秒
        username_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'yhm'))
        )
        # 在用户名输入框中输入用户名
        username_field.send_keys(username)

        # 等待密码输入框加载并变为可交互，最多等待 10 秒
        password_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'mm'))  # 使用 ID 定位密码输入框
        )
        # 在密码输入框中输入密码
        password_field.send_keys(password)

        # 等待登录按钮加载并变为可交互，最多等待 10 秒
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'dl'))
        )
        # 点击登录按钮
        login_button.click()

        # 获取所有窗口句柄
        all_window_handles = driver.window_handles
        print("所有窗口句柄:", all_window_handles)
 
        # 存储当前页面句柄
        window_handle = driver.current_window_handle
        print("存储的窗口句柄:", window_handle)
        

        # 获取当前页面的所有 Cookie
        cookies = driver.get_cookies()
        
        # 返回获取到的 Cookie
        return cookies
    
    except TimeoutException:
        # 如果发生超时异常，打印提示信息
        print("登录超时，请检查网络或凭证。")
        # 关闭浏览器
        driver.quit()
        # 返回 None，表示登录失败
        return None

def return_handle():
    return global_window_handle