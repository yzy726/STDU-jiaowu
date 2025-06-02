from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

## 课表查询

def kbcx(driver):
    """课表查询函数"""
    try:
        # 等待信息查询菜单
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'信息查询')]"))
        )
 
        # 1. 找到"信息查询"菜单项
        info_query_menu = driver.find_element(By.XPATH, "//a[contains(text(),'信息查询')]")
        
        # 2. 鼠标点击在"信息查询"菜单上以显示下拉菜单
        info_query_menu.click()
        
        # 3. 等待下拉菜单出现
        time.sleep(5)  # 等待下拉菜单展开
 
        # 4. 点击"个人课表查询"选项（注意：页面中有多个同名选项，需精准定位）
        # 使用更精确的XPath定位（在"信息查询"下拉菜单中的第二个"个人课表查询"）
        course_query_option = driver.find_element(
            By.XPATH,
            "//a[contains(text(),'信息查询')]/following-sibling::ul//a[contains(text(),'个人课表查询')][1]"
        )
        course_query_option.click()

        time.sleep(5)

        # 获取打开的多个窗口句柄
        windows = driver.window_handles
        # 切换到当前最新打开的窗口
        driver.switch_to.window(windows[-1])

        
        # 切换到课表查询页面后，可能需要等待页面加载
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'xqm_chosen'))  # 替换为实际存在的元素ID
        )

        time.sleep(5)

##        # 选择学年
##        academicyear_dropdown = WebDriverWait(driver, 30).until(
##            EC.element_to_be_clickable((By.ID, 'xnm_chosen'))
##        )
##        academicyear_dropdown.click()
        
        # 选择学期
        semester_dropdown = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, 'xqm_chosen'))
        )
        semester_dropdown.click()
        
        # 选择某季学期
        valid_semesters = ["秋", "春", "夏"]
        
        # 初始化用户输入
        user_input = ""
        
        # 循环直到用户输入有效的学期
        while user_input not in valid_semesters:
            user_input = input("请输入您想查询的学期（秋/春/夏）：").strip()
            if user_input not in valid_semesters:
                print("无效的学期输入，请重新输入！")
        
        # 用户输入有效，继续执行选择学期的操作
        try:
            semester_element = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(),'{user_input}')]"))
            )
            semester_element.click()
        except Exception as e:
            print(f"选择学期时出错: {e}")
        
        time.sleep(5)

        # 点击查询按钮
        search_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, 'search_go'))
        )
        search_button.click()

        time.sleep(10)
        
        print("课表查询成功")

        # 点击查询按钮
        lb_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='tb']/button[3]"))
        )
        lb_button.click()

    except Exception as e:
        print(f"课表查询出错: {e}")
        # 可以在这里添加截图功能帮助调试
        driver.save_screenshot('error_screenshot.png')


def rename(username):
    timestamp = int(time.time())
    new_filename = f"{username}_{timestamp}.pdf" 
    return new_filename  # 返回重命名后的文件名

def wjbc(excel_path, driver, window_handle):
    '''
    保存页面课程表内容到excel文件
    '''
    time.sleep(10)
    # 获取页面HTML内容
    html = driver.page_source

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(5)

    # 找到课程表容器
    tab_pane = soup.find('div', {'id': 'table2'})
    if not tab_pane:
        raise Exception("无法找到课程表容器")

    # 准备存储数据的列表
    data = []
    last_time_slot = ""  # 用于记录上一门课程的节次

    # 处理每一天的课程
    for day in range(1, 6):  # 周一到周五
        tbody = tab_pane.find('tbody', {'id': f'xq_{day}'})
        if not tbody:
            continue
            
        # 获取星期几
        weekday = tbody.find('span', {'class': 'week'}).text if tbody.find('span', {'class': 'week'}) else f"星期{day}"
        
        # 处理该天的所有课程
        courses = tbody.find_all('tr')[1:]  # 跳过标题行
        
        for course in courses:
            # 获取节次
            time_slot = course.find('span', {'class': 'festival'})
            current_time_slot = time_slot.text.strip() if time_slot else ""
            
            # 如果当前节次为空，则使用上一门课程的节次
            if not current_time_slot and data:
                current_time_slot = last_time_slot
            elif current_time_slot:
                last_time_slot = current_time_slot  # 更新最后记录的节次
            
            # 处理一个tr中可能的多门课程
            course_divs = course.find_all('div', {'class': 'timetable_con'})
            
            for course_div in course_divs:
                # 初始化课程信息
                course_info = {
                    '星期': weekday,
                    '节次': current_time_slot,
                    '课程名': '',
                    '教师名': '',
                    '教室名': '',
                    '上课周数': ''  # 新增的上课周数字段
                }
                
                # 获取课程名
                title = course_div.find('span', {'class': 'title'}) or course_div.find('u', {'class': 'title'})
                if title:
                    course_name = title.text.strip()
                    if '【调】' in course_name:
                        course_name = course_name.replace('【调】', '').strip()
                    course_info['课程名'] = course_name
                
                # 获取教师、教室和周数信息
                details = course_div.find_all('font', {'color': 'blue'})
                for detail in details:
                    text = detail.text.strip()
                    if '教师 ：' in text:
                        course_info['教师名'] = text.replace('教师 ：', '')
                    elif '上课地点：' in text:
                        course_info['教室名'] = text.split('上课地点：')[-1].strip()
                    elif '周数：' in text:  # 提取周数信息
                        course_info['上课周数'] = text.replace('周数：', '')
                
                data.append(course_info)

    # 处理其他课程
    other_courses_div = tab_pane.find('div', class_='timetable_title', string='其它课程：')
    if other_courses_div:
        other_courses_span = other_courses_div.find_next_sibling('span')
        if other_courses_span:
            for course in other_courses_span.text.split(';'):
                if course.strip():
                    parts = course.split('/')
                    if len(parts) >= 2:
                        data.append({
                            '星期': '其他课程',
                            '节次': '网络课',
                            '课程名': parts[0].strip(),
                            '教师名': '网络教师',
                            '教室名': '网络课程',
                            '上课周数': parts[1].strip()  # 从其他课程中提取周数
                        })

    # 创建DataFrame
    df = pd.DataFrame(data)

    # 指定列顺序（新增了上课周数列）
    columns = ['星期', '节次', '课程名', '教师名', '教室名', '上课周数']
    df = df[columns]

    # 指定导出目录（修改为你想要的路径）
    export_directory = excel_path  # 替换为你的目标路径
    
    # 确保目录存在
    os.makedirs(export_directory, exist_ok=True)
    
    # 生成文件名（包含完整路径）
    filename = os.path.join(export_directory, f"课程表_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    
    # 导出到Excel
    df.to_excel(filename, index=False)

    print(f"课程表已成功导出到 {filename}")
    print(f"共提取了 {len(df)} 门课程")
    # driver.close()
    # driver.switch_to.window(window_handle)
    return filename
