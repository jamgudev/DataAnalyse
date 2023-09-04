import re

def check_package_name(package_name):
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)*$'  # 正则表达式模式
    match = re.match(pattern, package_name)  # 进行匹配
    return bool(match)  # 返回匹配结果

# 测试包名
test_package1 = "com.example.app"      # 符合格式
test_package2 = "com.example.app_v1"   # 符合格式
test_package3 = "com.example.app123"   # 符合格式
test_package4 = "com.example.app."     # 不符合格式
test_package5 = "tv.app.v1"   # 符合格式
test_package6 = "com.example.app_"     # 不符合格式

# 检查包名格式
print(check_package_name(test_package1))  # True
print(check_package_name(test_package2))  # True
print(check_package_name(test_package3))  # True
print(check_package_name(test_package4))  # False
print(check_package_name(test_package5))  # True
print(check_package_name(test_package6))  # False