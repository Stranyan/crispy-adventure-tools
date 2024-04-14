import xlrd
import requests
import re

#  pip uninstall xlrd
#  pip install xlrd==1.2.0

read_path = r"C:\Users\winor\Desktop\Files\丽香\香格里拉/video.xlsx"

bk = xlrd.open_workbook(read_path)
shxrange = range(bk.nsheets)
try:
    sh = bk.sheet_by_name("video")
except:
    print("no sheet in %s named video" % read_path)
#获取总行数
nrows = sh.nrows
print("nrows=",nrows)
for i in range(nrows):
    if i < 1320:
        i = i + 1
        name = sh.cell_value(i,7) #读取图片名称
        namestr = str(name)
        url = sh.cell_value(i,16) #依次读取每行第16列的数据，也就是URL
        # pointname = namestr[:namestr.index(".")]
        pointname = re.sub(r'/','-', namestr)
        pic_name = "D:\Shell\GoodTool\SnapPic-xgllhjs" + pointname + "." + "jpg"
        err_name = "D:\Shell\GoodTool\SnapPic-xgllhjs" + pointname + "." + "JPG"
        if "http" in url:
            f = requests.get(url) #下载图片
            with open(pic_name, "wb") as code:
                code.write(f.content) #保存文件
            print("完成下载：" + pointname,i)
        else:
            with open(err_name, "w") as code:
                code.write("NoNoNo") #保存文件
            print("null：" + pointname,i)
    else:
        print("完成！")