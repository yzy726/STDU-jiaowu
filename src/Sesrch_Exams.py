from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def kscx(driver):
    """考试查询函数"""
    try:
        # 获取当前窗口句柄
        original_window = driver.current_window_handle

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
            "//a[contains(text(),'信息查询')]/following-sibling::ul//a[contains(text(),'考试信息查询')]"
        )
        course_query_option.click()


        # # 切换到课表查询页面后，可能需要等待页面加载
        # WebDriverWait(driver, 30).until(
        #     EC.presence_of_element_located((By.ID, 'search_go'))  # 替换为实际存在的元素ID
        # )

        # 等待新窗口打开
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
 
        # 获取所有窗口句柄
        all_window_handles = driver.window_handles
 
        # 切换到新窗口
        for handle in all_window_handles:
            if handle != original_window:
                driver.switch_to.window(handle)
                print("切换到新窗口:", driver.title)
                break

##        # 选择学年
##        academicyear_dropdown = WebDriverWait(driver, 30).until(
##            EC.element_to_be_clickable((By.ID, 'xnm_chosen'))
##        )
##        academicyear_dropdown.click()
        
        # # 选择学期
        # semester_dropdown = WebDriverWait(driver, 30).until(
        #     EC.element_to_be_clickable((By.ID, 'xqm_chosen'))
        # )
        # semester_dropdown.click()
        
        # # 选择某季学期
        # spring_semester = WebDriverWait(driver, 30).until(
        #     EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'春')]"))
        # )
        # spring_semester.click()
        

        # 等待主界面加载完成
        time.sleep(3)
        
        # 1. 点击主界面的导出按钮
        main_export_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn_dc"))
        )
        main_export_button.click()
        print("已点击主界面导出按钮")
        
        # 2. 等待二级界面弹出
        time.sleep(3)  # 等待弹窗加载
        
        # 3. 切换到二级界面（模态框）
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-dialog.modal-dialog-reset.ui-draggable"))
        )

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

        # 4. 在二级界面中点击导出按钮
        secondary_export_button = WebDriverWait(modal, 10).until(
            EC.element_to_be_clickable((By.ID, "btn_bcdc"))
        )
        secondary_export_button.click()
        print("已点击二级界面导出按钮")
        
        # 5. 等待导出操作完成
        time.sleep(10)  # 根据实际需要调整等待时间

        # driver.switch_to.window(global_window_handle)

        return stored_value
    
    except Exception as e:
        print(f"考试查询出错: {e}")
        # 可以在这里添加截图功能帮助调试
        driver.save_screenshot('error_screenshot.png')


def display_exam_schedule(driver,excel_path, window_handle):
    """
    从Excel文件读取考试信息，并显示考试时间、地点和座号
    
    参数:
        excel_path: Excel文件路径
    """
    try:
        time.sleep(10)

        # 读取Excel文件
        df = pd.read_excel(excel_path)
        
        # 检查必要的列是否存在
        required_columns = ['考试时间', '考试地点', '考试座号']
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            print(f"错误：Excel文件中缺少必要的列: {', '.join(missing_cols)}")
            return
        
        # 提取并显示考试信息
        print("\n考试安排信息：")
        print("=" * 60)
        print(f"{'序号':<5}{'考试时间':<25}{'考试地点':<20}{'考试座号':<10}")
        print("-" * 60)
        
        for idx, row in df.iterrows():
            exam_time = str(row['考试时间']) if pd.notna(row['考试时间']) else "未安排"
            exam_place = str(row['考试地点']) if pd.notna(row['考试地点']) else "未安排"
            exam_seat = str(row['考试座号']) if pd.notna(row['考试座号']) else "未安排"
            
            print(f"{idx+1:<5}{exam_time:<25}{exam_place:<20}{exam_seat:<10}")
        
        print("=" * 60)
        print(f"共找到 {len(df)} 场考试")
        # driver.switch_to.window(global_window_handle)
        # driver.close()
        # driver.switch_to.window(window_handle)
        
    except FileNotFoundError:
        print(f"错误：找不到文件 {excel_path}")
    except Exception as e:
        print(f"读取文件时出错: {e}")
