
import sys
import os
from xml.dom import minidom
from ftplib import FTP
import cchardet as chardet

#FTP
host,username,password = '192.168.10.10','hujie','hujie'

file_txt = []


for files in os.walk(os.getcwd()):
  for file in files[2]:
    if os.path.splitext(file)[1] == '.txt':
      file_txt.append(file)
      # print(file)
      # print(os.path.realpath(file))
      

if len(file_txt) == 0:
  sys.exit()


if len(file_txt) > 1:
  print("\n注：请将txt文件放到此程序目录下。txt文本文件里面的内容格式必须为 餐厅名称  餐厅编号  餐厅IP段")
  print("\n请选择你要生成的StoreInfo.xml文件的txt文本")
  for index in range(len(file_txt)) :
    print(" {}\t{}".format(index + 1,file_txt[index]))
  number = int(input("\n请输入文件编号："))
  txt_filename = file_txt[number - 1]
else:
  txt_filename = file_txt[0]


# 获取文件编码格式
c = chardet.detect(open(txt_filename, "rb").read())

print("{} 的编码格式为：{}\n".format(txt_filename,c['encoding']))

f = open(txt_filename,'r',encoding=c['encoding'])

line = f.readline()
# 18666862607
stores = []

while line:

  
  if len(line.split()) != 0 :
  
    stores.append(line.split())

  line = f.readline()

f.close()
# print(stores)


dom = minidom.Document()
stores_node=dom.createElement('Stores')
dom.appendChild(stores_node)

try:
  for store in stores:
    store_node=dom.createElement('Store')
    print(store[1],store[0],store[2])
    stores_node.appendChild(store_node)
    store_node.setAttribute('id',store[1])
    store_node.setAttribute('name',store[0])
    if store[2][-1] != '.':
      store[2] = store[2] + '.'
    store_node.setAttribute('ip',store[2])

except Exception as e:
  input('添加XML出现异常')
  os.close()



try:
  with open('StoreInfo.xml','w',encoding='UTF-8') as fh:
    # 4.writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
    # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
    dom.writexml(fh,indent='',addindent='\t',newl='\n',encoding='UTF-8')
    print('写入StoreInfo.xml OK!')
except Exception as err:
    input('写入文件失败！错误信息：{0}'.format(err))
    os.close()


#region

try:
    ftp = FTP(host=host,user=username,passwd=password)

    fp = open('StoreInfo.xml','rb')
    result = ftp.storbinary('STOR StoreInfo.xml',fp)
    print(result,'上传文件成功！')
    fp.close()
except FileNotFoundError as e:
    print('StoreInfo.xml 文件不存在！')
except Exception as a:
    print('StoreInfo.xml 文件上传失败！')

#endregion



os.system('pause')
