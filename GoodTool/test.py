ip_1 = "192"
ip_2 = "168"
ip_3 = "0-10"
ip_4 = "1-10"

def if_ip(ip):
    ip_list = []
    if "-" in ip:
        ip_start, ip_end = ip.split('-', 1)
        ip_range = [str(i) for i in range(int(ip_start), int(ip_end) + 1)]
        ip_list.extend(ip_range)
    else:
        ip_list.append(ip)
    return ip_list
def if_list(ip_list_1, ip_list_2, ip_list_3, ip_list_4):
    ip_lists = [ip_list_1, ip_list_2, ip_list_3, ip_list_4]
    result = []
    for ip_list in ip_lists:
        if len(ip_list) > 1:
            for i in ip_lists[0]:
                for j in ip_lists[1]:
                    for k in ip_lists[2]:
                        for l in ip_lists[3]:
                            combined = f"{i}.{j}.{k}.{l}"
                            result.append(combined)
    return result
ip_list_1 = if_ip(ip_1)
ip_list_2 = if_ip(ip_2)
ip_list_3 = if_ip(ip_3)
ip_list_4 = if_ip(ip_4)
result = if_list(ip_list_1, ip_list_2, ip_list_3, ip_list_4)
print("result",result)



# def if_ip(ip):
#     ip_list = []
#     if "-" in ip:
#         ip_start, ip_end = ip.split('-', 1)
#         ip_range = [str(i) for i in range(int(ip_start), int(ip_end) + 1)]
#         ip_list.extend(ip_range)
#     else:
#         ip_list.append(ip)
#     return ip_list
# def if_list(ip_list_1, ip_list_2, ip_list_3, ip_list_4):
#     ip_lists = [ip_list_1, ip_list_2, ip_list_3, ip_list_4]
#     result = []
#     for ip_list in ip_lists:
#         if len(ip_list) > 1:
#             for index, item in enumerate(ip_lists):
#                 if item == ip_list:
#                     position = index
#                     break
#             for i in ip_list:
#                 if position == 0:
#                     combined = f"{i}.{''.join(ip_lists[1])}.{''.join(ip_lists[2])}.{''.join(ip_lists[3])}"
#                 elif position == 1:
#                     combined = f"{''.join(ip_lists[0])}.{i}.{''.join(ip_lists[2])}.{''.join(ip_lists[3])}"
#                 elif position == 2:
#                     combined = f"{''.join(ip_lists[0])}.{''.join(ip_lists[1])}.{i}.{''.join(ip_lists[3])}"
#                 elif position == 3:
#                     combined = f"{''.join(ip_lists[0])}.{''.join(ip_lists[1])}.{''.join(ip_lists[2])}.{i}"
#                 result.append(combined)
#     return result
# ip_list_1 = if_ip(ip_1)
# ip_list_2 = if_ip(ip_2)
# ip_list_3 = if_ip(ip_3)
# ip_list_4 = if_ip(ip_4)
# result = if_list(ip_list_1, ip_list_2, ip_list_3, ip_list_4)
# print("result",result)