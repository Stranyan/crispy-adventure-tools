import subprocess, os, datetime, time, re

# 获取当前工作目录
current_directory = os.getcwd()
print("当前工作目录：", current_directory)

def ping_and_save_result(ip):
    # 执行 Ping 命令
    result = subprocess.run(['ping', '-n', '4', ip], capture_output=True, text=True)
    print(result.stdout)

    # 获取当前时间
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.strftime('%H:%M:%S')

    # 提取时间和丢包率
    time_pattern = r"最短 = .*?ms，最长 = .*?ms，平均 = .*?ms"
    loss_pattern = r"\(.*? 丢失\)"
    time_match = re.search(time_pattern, result.stdout)
    loss_match = re.search(loss_pattern, result.stdout)
    time_str = time_match.group() if time_match else "None"
    loss_str = loss_match.group() if loss_match else "None"

    # 保存结果到文件
    with open('ping_results.txt', 'a+') as file:
        last_recorded_date = get_last_recorded_date(file)

        if current_date != last_recorded_date:
            file.write(f'Date: {current_date}\n')
            file.write('\n')

        file.write(f'IP: {ip}\n')
        file.write(f'Time: {current_time}\n')
        file.write(f'Status: {time_str}\n')
        file.write(f'Loss: {loss_str}\n')
        file.write('\n')

def get_last_recorded_date(file):
    file.seek(0)  # Move the file pointer to the beginning of the file
    lines = file.readlines()
    for line in reversed(lines):
        if line.startswith('Date: '):
            date_str = line.split('Date: ')[1].strip()
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    return None

# 要ping的IP列表
ip_list = [
    "10.73.221.210",
    "10.73.221.211",
    "10.73.221.212",
    "10.84.107.218",
    "10.73.221.209",
    "10.84.109.146",
    "10.73.221.226",
    "10.73.221.227",
    "10.73.221.228",
    "10.84.109.146",
    "10.73.221.225",
    "10.84.109.145",
    "10.75.165.98",
    "10.75.165.100",
    "10.75.165.99",
    "10.86.250.126",
    "10.73.221.225",
    "10.86.250.125",
    "10.73.226.50",
    "10.73.226.52",
    "10.73.226.51",
    "10.73.226.54",
    "10.73.226.49",
    "10.73.226.18",
    "10.73.226.20",
    "10.73.226.19",
    "10.73.226.21",
    "10.73.226.17"
    ]

# 每隔一定时间执行 Ping 命令并保存结果
while True:
    for ip in ip_list:
        ping_and_save_result(ip)
    time.sleep(10)  # 暂停
