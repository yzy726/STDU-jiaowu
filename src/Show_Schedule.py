import pandas as pd
from datetime import datetime

def get_current_week(SEMESTER_START_DATE):
    """计算当前是第几周"""
    today = datetime.now()
    delta = today - SEMESTER_START_DATE
    current_week = delta.days // 7 + 1  # 计算完整的周数，+1是因为第一周从1开始
    return current_week

def show_current_week_courses(excel_path, SEMESTER_START_DATE):
    """
    从Excel文件读取课程表，并显示当前周数和星期的课程
    
    参数:
        excel_path: Excel文件路径
    """
    # 读取Excel文件
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"无法读取Excel文件: {e}")
        return
    
    # 获取当前周数和星期
    current_week = get_current_week(SEMESTER_START_DATE)
    current_weekday = datetime.now().strftime("%A")
    weekday_map = {
        "Monday": "星期一",
        "Tuesday": "星期二",
        "Wednesday": "星期三",
        "Thursday": "星期四",
        "Friday": "星期五",
        "Saturday": "星期六",
        "Sunday": "星期日"
    }
    current_weekday_chinese = weekday_map.get(current_weekday, "未知")
    
    # 筛选当前周数和星期的课程
    def is_current_week(course_weeks):
        """检查课程是否在当前周"""
        if not course_weeks or pd.isna(course_weeks):
            return False
        
        # 处理多种周数格式
        week_ranges = str(course_weeks).replace("周", "").split(",")
        for week_range in week_ranges:
            if "-" in week_range:
                try:
                    start, end = map(int, week_range.split("-"))
                    if start <= current_week <= end:
                        return True
                except ValueError:
                    continue
            else:
                try:
                    if current_week == int(week_range):
                        return True
                except ValueError:
                    continue
        return False
    
    # 筛选符合条件的课程
    current_courses = df[
        (df["星期"] == current_weekday_chinese) & 
        (df["上课周数"].apply(is_current_week))
    ].sort_values("节次")
    
    # 输出结果到屏幕
    print(f"\n当前是第 {current_week} 周 {current_weekday_chinese}")
    print("="*40)
    
    if current_courses.empty:
        print("今天没有课程")
    else:
        for _, row in current_courses.iterrows():
            print(f"节次: {row['节次']}")
            print(f"课程: {row['课程名']}")
            print(f"教师: {row['教师名']}")
            print(f"教室: {row['教室名']}")
            print("-"*30)
