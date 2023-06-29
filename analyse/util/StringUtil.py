

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
