import sqlite3
import random
import string
import os

# 确保数据库目录存在
db_path = r'C:\Users\yuling\vscode_test\smartae\database'
os.makedirs(db_path, exist_ok=True)

# 创建数据库连接
db_file = os.path.join(db_path, 'smartae_database.db')
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 删除已存在的表（如果存在）
cursor.execute('DROP TABLE IF EXISTS registers')

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS registers (
    id INTEGER PRIMARY KEY,
    regname TEXT,
    addr INTEGER,
    field TEXT,
    msb INTEGER,
    lsb INTEGER,
    value TEXT,
    description TEXT
)
''')

# 生成随机字符串的函数
def random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# 生成随机字段描述的函数
def random_description():
    descriptions = [
        "配置寄存器",
        "状态寄存器",
        "控制寄存器",
        "中断使能",
        "数据寄存器"
    ]
    return random.choice(descriptions) + "_" + random_string(4)

# 生成随机regname的函数
def random_regname():
    components = ["SWB", "PSTM"]
    modules = ["PQM", "ADM", "NVT", "ISWP", "ESWP"]
    planes = ["0", "1"]
    func_level1 = ["INT", "XOFF"]
    func_level2 = ["SET", "ENABLE", "STATUS"]
    
    return "_".join([
        random.choice(components),
        random.choice(modules),
        "B" + random.choice(planes),
        random.choice(func_level1),
        random.choice(func_level2)
    ])

# 插入100条数据
current_id = 1
for i in range(1, 31):  # 生成30个不同的寄存器
    regname = random_regname()  # 使用新的regname生成函数
    addr = i * 4
    
    # 为每个寄存器生成1-32个随机field
    field_count = random.randint(1, 32)
    
    # 跟踪已使用的bit位
    used_bits = set()
    
    for _ in range(field_count):
        if current_id > 100:  # 确保总记录数不超过100
            break
            
        field = "FIELD_" + random_string(4)
        
        # 寻找未使用的bit位范围
        available_ranges = []
        start = 0
        while start <= 31:
            if start not in used_bits:
                end = start
                while end < 31 and end + 1 not in used_bits:
                    end += 1
                if end - start >= 0:  # 至少需要1位
                    available_ranges.append((start, end))
                start = end + 1
            else:
                start += 1
        
        if not available_ranges:
            break
            
        # 随机选择一个可用范围
        start, end = random.choice(available_ranges)
        max_width = min(4, end - start + 1)  # 限制最大宽度为4
        lsb = start
        msb = random.randint(lsb, min(lsb + max_width - 1, end))
        
        # 标记已使用的bit位
        used_bits.update(range(lsb, msb + 1))
        
        # 生成随机的16进制值
        bit_width = msb - lsb + 1
        max_value = (1 << bit_width) - 1
        value = hex(random.randint(0, max_value))
        
        description = random_description()
        
        # 插入数据
        cursor.execute('''
        INSERT INTO registers (id, regname, addr, field, msb, lsb, value, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (current_id, regname, addr, field, msb, lsb, value, description))
        
        current_id += 1
        if current_id > 100:
            break

# 提交更改
conn.commit()

# 打印数据库内容
print("数据库内容：")
print("ID\tREGNAME\t\tADDR\tFIELD\t\tMSB\tLSB\tVALUE\tDESCRIPTION")
print("-" * 100)

cursor.execute('SELECT * FROM registers')
for row in cursor.fetchall():
    print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}\t{row[7]}")

# 关闭连接
conn.close()
