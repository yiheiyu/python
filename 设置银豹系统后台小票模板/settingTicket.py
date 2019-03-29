# -*- coding: utf-8 -*-
import re
import requests


class settingTicket:

    # 登陆
    def login(self,username):
        login_url = "http://beta15.pospal.cn/account/SignIn?noLog="
        returnurl = "http://beta15.pospal.cn/Cashier/Manage"
        perfix = username[0:2]
       

        if perfix not in ['nx','tg','NX','TG']:
            return '门店编号不正确！'
        
        pdpass = {
            'nx':'密码',
            'tg':'密码'
        }

        datas = {
            'userName':username,
            'password':pdpass[perfix],
            'returnUrl':returnurl
        }

        try:
            session = requests.session()
            r = session.post(login_url,data=datas)
            s = r.text.replace('true','\"true\"')
            reault = eval(s)
            reault.update({'session':session})
            reault.update({'brand':str(perfix).upper()})
            return reault
        except Exception as e:
            return '登陆失败'
    
   

    

    # 设置小票打印机模板
    def settingtpt(self,login):

        try:
            
            request_url = "http://beta15.pospal.cn/Setting/UpdateStoreOption"
            session = login['session']
            brand = login['brand']

            t = self.readtpt(brand)
            if t is None:
                return '获取tpt文件异常/失败，或者文件丢失'

            datas = {
                'attribute':'ticketPrinterTemplate80',
                'value':t
            }

            r = session.post(request_url,data=datas)
            s = r.text.replace('true','\"true\"')
            # print(r.text)
            return s

        except Exception as e:
            return None



    # 获取tpt模板文件
    def readtpt(self,brand):

        b = {
            'NX':'ticket_nx.tpt',
            'TG':'ticket_tg.tpt'
        }
        
        try:
            
            f = open(b[brand])
            return f.read()
            f.close()

        except Exception as e:
            return None
        
        
    def run(self):

        print('\n脚本用于自动修改门店收银小票模板\n')
        print('注：请将 ticket_nx.tpt 和 ticket_tg.tpt 两个模板文件放在该文件目录下')

        while True:

            user = self.login(input('\n请输入要修改小票模板的门店编号:'))
            # user = self.login('nxsh0001')
    
            if type(user) is not dict:
                print(user)
                continue
            else:
                s = self.settingtpt(user)
                if s is not None:
                    print('修改成功！ 返回结果:',s)
                else:
                    print('修改失败！ 返回结果:',s)
                continue

        
def main():
    st = settingTicket()
    st.run()
    
    
if __name__ == "__main__":
    main()









