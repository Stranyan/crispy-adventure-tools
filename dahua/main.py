import get_qj_ip
import dahua_get_copy
import Json_Excel

workbook_url = r'C:\Users\winor\Documents\我的数据库-20240319.xlsx'
sheet_num = 0
qj_ip = get_qj_ip.get_qj_info(workbook_url, sheet_num)

ip_chno_pairs = [(data['ip'], data['chno']) for data in qj_ip.values()]
pwd = "wlmbds123"

# 循环迭代 IP 和通道号
for ip, chno in ip_chno_pairs:
    preset_file = dahua_get_copy.get_dahua_preset(ip, pwd)
    print("IP:", ip, "通道号:", chno)

Json_Excel.get_output()