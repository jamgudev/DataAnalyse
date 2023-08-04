import re


# 将完整的文件路径名改成简短的
def get_short_file_name_for_print(fullFileName: str) -> str:
    if fullFileName:
        offPathLen = fullFileName.rfind("/")
        originLen = len(fullFileName)
        if offPathLen < originLen:
            return fullFileName[offPathLen + 1: originLen]
        else:
            return fullFileName
    else:
        return fullFileName


def get_mobile_number_start_pos(text: str):
    phone_pattern = r'\b1[34578]\d{9}\b'
    match = re.search(phone_pattern, text)
    if match:
        return match.start()
    else:
        return -1


# 从字符串中识别电话号码并返回，需满足这样的格式：sss/13266297720_平板/sss
def get_user_name(text: str):
    import re
    # 有时候可能text末尾不带/，这里手动补一个
    text += "/"
    pattern = r'/1\d{10}_[^/]+/'
    matches = re.findall(pattern, text)

    if matches:
        # 输出所有匹配的字符串
        for match in matches:
            result = match.replace("/", "")
            return result
    else:
        return ""
