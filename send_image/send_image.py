from datetime import date, timedelta

import requests
import yaml
from jsonpath import jsonpath
from selenium import webdriver
from time import sleep


class TestImage:

    # 获取表单列表，提取符合条件的表单name及token
    def get_forms(self):
        url = 'https://jinshuju.net/api/v1/forms'

        headers = {
            'Authorization': 'Basic RkFUS2VqbFlwUkdSSVFfVGM3T1gwUTpZMVRLYk1uNm42S0FlckVDM1Y4b0Rn'
        }
        res = requests.get(url, headers=headers)
        name = jsonpath(res.json(), "$.data..name")[0:10]
        token = jsonpath(res.json(), "$.data..token")[0:10]
        yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d").replace("-","")
        form_dict = dict(zip(name, token))
        s1 = {}
        for i, k in form_dict.items():
            a = str(i).split("-")[0].strip()[-8:]
            if a.isdigit() and a == yesterday:
                s1.setdefault(k, i)
        return s1


    def get_cookie(self):
        options = webdriver.ChromeOptions()
        options.debugger_address = '127.0.0.1:9222'
        driver = webdriver.Chrome(options=options)
        file = open('cookies.yaml', 'w', encoding="utf-8")
        yaml.dump(driver.get_cookies(), file)
        file.close()

    def load_cookie(self):
        return yaml.safe_load(open(r'C:\Users\89703\PycharmProjects\hogwarts19\test_image\cookies.yaml', encoding='utf-8'))


    def screen_shot(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get('https://jinshuju.net/form_folders/m1LtU8')
        for cookie in self.load_cookie():
            self.driver.add_cookie(cookie)

        data = self.get_forms()
        base_url = 'https://jinshuju.net/forms'
        form_token = [i for i in data.keys()]
        filename_list = []
        for i in form_token:
            url = f'{base_url}/{i}/entries'
            self.driver.get(url)
            self.driver.refresh()
            self.driver.save_screenshot(f'{data[i]}.png')
            sleep(3)

            filename_list.append(f'{data[i]}.png')
        return filename_list
        # return len(filename_list)
        # print(filename_list)
            # filename = f'{data[i]}.png'
            # print(type(filename))


    def get_token(self):
        ID = 'wwf911a5604c031a07'
        SECRET = '0ZKm_0el5XSXnI3EhaivnJ-fl0jno9c8FkQfs5-CR5M'
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {'corpid': ID,
                  'corpsecret': SECRET}
        res = requests.get(url, params=params)
        # print(res.json())
        access_token = res.json()["access_token"]
        return access_token

    def upload_image(self):
        access_token = self.get_token()
        filename_list=self.screen_shot()
        # mediaid_list = []
        for filename in filename_list:
            upload_url = 'https://qyapi.weixin.qq.com/cgi-bin/media/uploadimg'
            params = {'access_token': access_token}
            payload = {
                'filename':filename,
            }
            files = [(filename,open(f'C:\\Users\\89703\\PycharmProjects\\send_image\\send_image\\{filename}','rb'),'image/png')]
            res = requests.post(upload_url,params=params, data=payload,files=files)
            print(res.json())
            img_url = res.json()['url']
            url = "https://login.ceshiren.com/dev/custom/send"
            data = {
                "robotId": "5ce171070a60e234ae563927",
                "group_name": "测吧助教群2021",
                "type": 1,
                "payload": {
                    "url": img_url,
                    "size": 1024
                }

            }


            # media_id = res.json()['media_id']
            # mediaid_list.append(media_id)
            # send_url = ' https://qyapi.weixin.qq.com/cgi-bin/message/send'
            # params = {'access_token':access_token}
            # payload = {
            #     "touser":"@all",
            #     'msgtype':"mpnews",
            #     'agentid':1000002,
            #     'mpnews':{
            #         'articles':[
            #             {'title':'课后调查',
            #              'thumb_media_id':media_id,
            #              'content':filename}
            #         ]
            #     }
            # }
            # res = requests.post(send_url,params=params,json=payload)
            # print(res.json())


if __name__ == '__main__':
    TestImage().upload_image()