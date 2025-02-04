# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import re

import pyinputplus as pyip

# def mypyip():

# userin = pyip.inputCustom(mypyip)
userin = "写寄存器 IPSC 域段 COS 值 1"
# userin = "写寄存器 IPSC 值 2"
# userin = "读寄存器 IPSC"
# userin = "连续读寄存器 IPSC 读 3"
# userin = "读直接表项 IPSC_TBL 地址 0x1"
# userin = "连续读直接表项 IPSC_TBL 地址 0x1 读 4"

rsn = r'\s*[A-Z0-9{}_]+\s*'
rsf = r'\s*[A-Za-z0-9_]+\s*'
chn = r'\s*[\u4e00-\u9fff]*\s*'
eng = r'\s*[a-zA-Z0-9_]+\s*'

write_reg_field = re.search(rf"写寄存器({rsn})域段*({rsf})值\s*(\d+)", userin)
write_reg = re.search(rf"写寄存器({rsn})值\s*(\d+)", userin)
read_reg = re.match(rf"读寄存器({rsn})", userin)
read_regs = re.search(rf"连续读寄存器({rsn})读\s*(\d+)", userin)
read_tbl = re.match(rf"读直接表项({rsn})地址({rsf})", userin)
read_tbls = re.match(rf"连续读直接表项({rsn})地址({rsf})读\s*(\d+)", userin)

if write_reg_field:
    print("write_reg_field matched")
    print(write_reg_field.group(1),write_reg_field.group(2),write_reg_field.group(3))
elif write_reg:
    print("write_reg matched")
    print(write_reg.group(1),write_reg.group(2))
elif read_reg:
    print("read_reg matched")
    print(read_reg.group(1))
elif read_regs:
    print("read_regs matched")
    print(read_regs.group(1),read_regs.group(2))
elif read_tbl:
    print("read_tbl matched")
    print(read_tbl.group(1),read_tbl.group(2))
elif read_tbls:
    print("read_tbls matched")
    print(read_tbls.group(1),read_tbls.group(2),read_tbls.group(3))


# 按间距中的绿色按钮以运行脚本。
# if __name__ == '__main__':
#     print_hi("读寄存器 IPSC 地址 1")

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
