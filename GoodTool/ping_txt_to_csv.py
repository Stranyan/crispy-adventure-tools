import csv

ips = ["10.73.221.210",
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
       "10.73.226.17",
]
tips = ["枣林NVR",
        "枣林通信管理机",
        "枣林数据库",
        "枣林路由器",
        "枣林网关1",
        "枣林网关2",
        "东河南NVR",
        "东河南通信管理机",
        "东河南数据库",
        "东河南路由器",
        "东河南网关1",
        "东河南网关2",
        "大同南NVR",
        "大同南通信管理机",
        "大同南数据库",
        "大同南路由器",
        "大同南网关1",
        "大同南网关2",
        "运城北NVR",
        "运城北通信管理机",
        "运城北数据库",
        "运城北路由器",
        "运城北网关",
        "半坡村NVR",
        "半坡村通信管理机",
        "半坡村数据库",
        "半坡村路由器",
        "半坡村网关",
]

# Read the text file and split it into lines
with open('ping_results.txt', 'r') as file:
    lines = file.read().splitlines()

# Create a list to store the data
data = []
current_date = ''
current_ip = ''
current_time = ''
current_status = ''
current_loss = ''

# Iterate over the lines and extract the relevant information
for line in lines:
    if line.startswith('Date:'):
        current_date = line.split(': ')[1]
    elif line.startswith('IP:'):
        current_ip = line.split(': ')[1]
    elif line.startswith('Time:'):
        current_time = line.split(': ')[1]
    elif line.startswith('Status:'):
        current_status = line.split(': ')[1]
        if current_status != 'None':
            min_value = current_status.split('，')[0].split('=')[1].strip().split('ms')[0]
            max_value = current_status.split('，')[1].split('=')[1].strip().split('ms')[0]
            avg_value = current_status.split('，')[2].split('=')[1].strip().split('ms')[0]
        else:
            min_value = max_value = avg_value = '999'
    elif line.startswith('Loss:'):
        current_loss = line.split(': ')[1]
        ip_index = ips.index(current_ip)  # Get the index of the current IP
        tip_value = tips[ip_index]  # Get the corresponding value from the other list
        data.append([current_date, current_time, current_ip, tip_value, min_value, max_value, avg_value, current_loss])

# Create a CSV file and write the data
with open('ping_results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Time', 'IP', 'Description', 'Min(ms)', 'Max(ms)', 'Avg(ms)', 'Loss'])  # Write the header
    writer.writerows(data)  # Write the data rows
    print('Done!!!')
