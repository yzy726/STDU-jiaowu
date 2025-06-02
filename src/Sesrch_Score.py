from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def cjcx(driver):
    """成绩查询函数"""
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
        time.sleep(3)  # 等待下拉菜单展开
 
        # 4. 点击"个人课表查询"选项（注意：页面中有多个同名选项，需精准定位）
        # 使用更精确的XPath定位（在"信息查询"下拉菜单中的第二个"个人课表查询"）
        course_query_option = driver.find_element(
            By.XPATH,
            "//a[contains(text(),'信息查询')]/following-sibling::ul//a[contains(text(),'学生成绩查询')]"
        )
        course_query_option.click()

        # 获取打开的多个窗口句柄
        windows = driver.window_handles
        # 切换到当前最新打开的窗口
        driver.switch_to.window(windows[-1])

        
        # 切换到课表查询页面后，可能需要等待页面加载
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'xqm_chosen'))  # 替换为实际存在的元素ID
        )

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
        spring_semester = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'春')]"))
        )
        spring_semester.click()
        
        # 点击查询按钮
        search_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, 'search_go'))
        )
        search_button.click()

        time.sleep(10)
        
        print("成绩查询成功")

        # 点击导出按钮
        dc_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "btn_dc"))
        )
        dc_button.click()
        
        
        time.sleep(2)

        # 等待输入框加载完成
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "exportFileName"))
        )
        
        # 获取value属性的值
        file_name_value = input_element.get_attribute("value")
        
        # 打印获取到的值
        print("提取到的value值:", file_name_value)
        
        # 你可以将这个值存储到变量中以供后续使用
        stored_value = file_name_value

        # 点击导出按钮
        dcdc_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "btn_bcdc"))
        )
        dcdc_button.click()
        time.sleep(10)
        return stored_value
    
    except Exception as e:
        print(f"成绩查询出错: {e}")
        # 可以在这里添加截图功能帮助调试
        driver.save_screenshot('error_screenshot.png')



def display_student_grades(driver,excel_path, window_handle):
    """
    从Excel文件读取学生成绩信息，并显示课程名称、成绩和绩点
    
    参数:
        excel_path: Excel文件路径
    """
    try:
        time.sleep(10)

        # 读取Excel文件
        df = pd.read_excel(excel_path)
        
        # 检查必要的列是否存在
        required_columns = ['课程名称', '成绩', '绩点']
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            print(f"错误：Excel文件中缺少必要的列: {', '.join(missing_cols)}")
            return
        
        # 获取学生基本信息（假设第一行是当前学生的记录）
        if len(df) > 0:
            student_id = str(df.iloc[0]['学号']) if '学号' in df.columns and pd.notna(df.iloc[0]['学号']) else "未知"
            student_name = str(df.iloc[0]['姓名']) if '姓名' in df.columns and pd.notna(df.iloc[0]['姓名']) else "未知"
        
        # 提取并显示成绩信息
        print("\n学生成绩信息")
        print("=" * 60)
        print(f"学号: {student_id}  姓名: {student_name}")
        print("=" * 60)
        print(f"{'序号':<5}{'课程名称':<30}{'成绩':<10}{'绩点':<10}")
        print("-" * 60)
        
        total_gpa_points = 0
        total_credits = 0
        
        for idx, row in df.iterrows():
            course_name = str(row['课程名称']) if pd.notna(row['课程名称']) else "未命名课程"
            grade = str(row['成绩']) if pd.notna(row['成绩']) else "未录入"
            gpa = float(row['绩点']) if pd.notna(row['绩点']) else 0.0
            credit = float(row['学分']) if '学分' in df.columns and pd.notna(row['学分']) else 0.0
            
            print(f"{idx+1:<5}{course_name:<30}{grade:<10}{gpa:<10.2f}")
            
            # 计算总绩点和总学分（如果数据完整）
            if pd.notna(row.get('学分')) and pd.notna(row.get('绩点')):
                total_gpa_points += credit * gpa
                total_credits += credit
        
        print("=" * 60)
        
        # 如果有完整的学分和绩点数据，计算平均绩点
        if total_credits > 0:
            avg_gpa = total_gpa_points / total_credits
            print(f"平均绩点: {avg_gpa:.2f}  (总学分: {total_credits:.1f})")
        print(f"共 {len(df)} 门课程成绩")

        # driver.switch_to.window(global_window_handle)
        # driver.close()
        # driver.switch_to.window(window_handle)
        
    except FileNotFoundError:
        print(f"错误：找不到文件 {excel_path}")
    except Exception as e:
        print(f"读取文件时出错: {e}")
