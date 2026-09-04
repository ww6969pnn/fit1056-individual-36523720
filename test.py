# test.py - 快速测试
import json
import os

# 测试1: 直接读取JSON
with open('data/msms.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== JSON内容 ===")
print(f"students: {data.get('students')}")
print(f"next_student_id: {data.get('next_student_id')}")
print(f"next_student_id 类型: {type(data.get('next_student_id'))}")
print(f"teachers: {data.get('teachers')}")

# 测试2: 导入ScheduleManager
print("\n=== 导入ScheduleManager ===")
from app.schedule import ScheduleManager
manager = ScheduleManager()

print(f"\nmanager.next_student_id = {manager.next_student_id}")
print(f"manager.next_student_id 类型 = {type(manager.next_student_id)}")

print("\n测试添加学生:")
manager.add_student("测试", ["piano"])
print("✅ 测试完成")