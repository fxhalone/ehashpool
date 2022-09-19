import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from auto.util.LogUtil import *
from auto.util.MySqlUtil import *
from auto.util.RedisUtil import *
from auto.util.ExcelUtil import *
from auto.util.googleUtil import *
import pytest
import random
import time
import json
import allure
import requests
logger = LogUtil.initLogger()
mysqlUtil = MySqlUtil()
redisUtil = RedisUtil()

headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }



class test_ehashpool:

    def setup_class(self):
        print('初始化数据')
        '''清除用户数据'''
        mysqlUtil.initEhashAccount()

    def teardown_class(self):
        print("测试结束")


    '''获取首页数据'''
    def home(self):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + HOME + "</h1>", name='url',attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method',attachment_type=allure.attachment_type.HTML)
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + HOME, headers=headers)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200



    '''发送邮箱验证码'''
    def sendEmailCode(self,codeTYpe):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS+SEND_EMAIL_CODE + "</h1>", name='url',attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        params = {
            'email':EMAIL,
            'codeType':codeTYpe
        }
        # dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(params) + "</h1>", name='requestParams', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS+SEND_EMAIL_CODE,headers=headers,params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData', attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code'])==200



    '''检查验证码'''
    def checkUserSignIn(self):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS+CHECK_USER_SIGNIN + "</h1>", name='url',attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {'email': EMAIL, 'verification_code': redisUtil.getEmailCode(EMALIL_CODE_SINGUP), 'invitation_code': ""}
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + CHECK_USER_SIGNIN, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200


    '''注册用户'''
    def addETHUser(self):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS+ADD_ETH_USER + "</h1>", name='url',attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            'username': "test"+str(int(time.time()*1000)),
            'email': EMAIL,
            'password': ACCOUNT_PASSWORD,
            'verification_code': redisUtil.getEmailCode(EMALIL_CODE_SINGUP)
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + ADD_ETH_USER, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200





    '''登陆(返回tonken)'''
    def login(self,verifyCode='0',GACode=0):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS+LOGIN + "</h1>", name='url',attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)

        data = {
            "email": EMAIL,
            "password": ACCOUNT_PASSWORD,
            # "email": '369959466@qq.com',
            # "password": ACCOUNT_PASSWORD,
            "GACode": GACode,
            "verifyCode": verifyCode
        }


        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + LOGIN, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200
        return response.json()['data']['token']



    '''创建子账户'''
    def createMiner(self,headers,uid):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS+CREATE_MINER + "</h1>", name='url',attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            "name": 'miner'+str(int(time.time()*1000)),
            'uid':uid
        }

        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + CREATE_MINER, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200

    '''获取子账户列表'''
    def getMinerList(self,headers,uid):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + GET_MINER_LIST + "</h1>", name='url',attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            'uid': uid
        }

        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + GET_MINER_LIST, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200
        return response.json()['data'][0]['name'],response.json()['data'][0]['minerId']

    '''检查子账号'''
    def checkMinerName(self,minerName):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + CHECK_MINER_NAME + "</h1>", name='url',attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        params = {
            'name': minerName
        }

        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + CHECK_MINER_NAME, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200




    '''获取子账号汇总数据'''
    def getStatSummary(self,headers,minerId):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_STAT_SUMMARY + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            'minerId': minerId
        }

        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_STAT_SUMMARY, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200


    '''获取子账号汇总数据'''
    def getHashRate(self,headers,minerId,span):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_HASHRATE + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            'minerId': minerId,
        }

        params = {
            # 'startTime': 1663017697632,
            # 'endTime': 1663060897632,
            'startTime': int(time.time() * 1000)-24*3600*1000,
            'endTime': int(time.time() * 1000),
            'span': span
        }
        allure.attach("<h1>"+str(params)+"</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_HASHRATE, headers=headers, data=dataJson,params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200


    '''导出子账号算力图表'''
    def exportHashrate(self,headers,minerId,span):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + EXPORT_HASHRATE + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            'minerId': minerId,
        }

        params = {
            # 'startTime': 1663017697632,
            # 'endTime': 1663060897632,
            'startTime': int(time.time() * 1000) - 24 * 3600 * 1000,
            'endTime': int(time.time() * 1000),
            'span': span
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + EXPORT_HASHRATE, headers=headers, data=dataJson, params=params)
        allure.attach("<h1>" + "文件" + "</h1>", name='responseData',attachment_type=allure.attachment_type.HTML)
        with open('./download/hashRate'+span+headers['Coin-Type']+'.xlsx', 'wb') as fd:
            for chunk in response.iter_content():
                fd.write(chunk)


    '''#获取矿机列表'''
    def getWorkerList(self,headers,minerId):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_WORKER_LIST + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            'minerId': minerId,
        }

        params = {
            'page': 1,
            'pageSize': 10,
            'sort': 'workerFullName',
            'orderBy': 'desc',
            'search': '',
            'status': 0,
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_WORKER_LIST, headers=headers, data=dataJson,params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200



    '''重置密码邮箱校验'''
    def checkUserEmail(self,codeType):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + CHECK_USER_EMAIL + "</h1>", name='url',attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            "codeType": codeType,
            "email": EMAIL,
            "invitation_code": "",
            "verification_code": redisUtil.getEmailCode(codeType)
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + CHECK_USER_EMAIL, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200


    '''修改密码'''
    def forgot(self):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + FORGOT + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            "codeType": EMALIL_CODE_FORGOT_PASSWORD,
            "code": redisUtil.getEmailCode(EMALIL_CODE_FORGOT_PASSWORD),
            "email": EMAIL,
            "newPassword": ACCOUNT_PASSWORD
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + FORGOT, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200

    '''获取登陆历史'''
    def loginHistory(self,headers):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + LOGIN_HISTORY + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + LOGIN_HISTORY, headers=headers)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200

    '''获取用户信息'''
    def info(self,headers):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + INFO + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + INFO, headers=headers)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200



    '''更新用户信息'''
    def updateETHUser(self,headers,uid):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + UPDATE_ETH_USER + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            "oldPassword": ACCOUNT_PASSWORD,
            "password": ACCOUNT_PASSWORD,
            "uid": uid
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + UPDATE_ETH_USER, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200

    '''获取用户子账号天收益图表数据'''
    def getMinerEarnSummary(self,headers,minerId):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_MINER_EARN_SUMMARY + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)


        params = {
            'minerId': minerId,
            'startTime': int(time.time() * 1000) - 48 * 3600 * 1000,
            'endTime': int(time.time() * 1000)
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_MINER_EARN_SUMMARY, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200

    '''获取用户子账号收益列表'''
    def getMinerEarnList(self,headers,minerId):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_MINER_EARNLIST + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)


        params = {
            'minerId': minerId,
            'startTime': int(time.time() * 1000) - 48 * 3600 * 1000,
            'endTime': int(time.time() * 1000),
            'page':1,
            'pageSize':10
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_MINER_EARNLIST, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200


    '''获取用户付款记录列表'''
    def getPaymentRecordList(self, headers, minerId):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_PAYMENT_RECORDLIST + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)

        params = {
            'startTime': int(time.time() * 1000) - 48 * 3600 * 1000,
            'endTime': int(time.time() * 1000),
            'page': 1,
            'pageSize': 10
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_PAYMENT_RECORDLIST, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200


    '''是否开启二次验证'''
    def updateSecondAuth(self,headers,state,emailCode):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + UPDATE_SECOND_AUTH + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            "GACode": 0,
            "status": state,
            "verifyCode":emailCode
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + UPDATE_SECOND_AUTH, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200


    '''新增观察者链接'''
    def createObserveLink(self,headers,minerId):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + CREATE_OBSERVE_LINK + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            "minerId": minerId,
            "remark": "test",
            "workers": 1,
            "earnings": 1
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + CREATE_OBSERVE_LINK, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200

    '''获取观察者列表'''
    def watch(self,headers):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + WATCH + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        params = {
            "page": 1,
            "pageSize": 10
        }

        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + WATCH, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200

        return response.json()['data']['observeList'][0]['token'],response.json()['data']['observeList'][0]['uid']


    '''获取观察者链接子账号信息'''
    def getMiner(self,token):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + GET_MINER + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        params = {
            "token": token
        }

        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + GET_MINER, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200



    '''获取观察者链接权限'''
    def getStatSummaryWatch(self,headers,watchToken):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_STAT_SUMMARY_WATCH + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        params = {
            'token':watchToken
        }
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_STAT_SUMMARY_WATCH, headers=headers,params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200


    '''获取观察者链接算力统计'''
    def getHashRateWatch(self, headers, span,watchToken):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_HASHRATE_WATCH + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)


        params = {
            'startTime': int(time.time() * 1000) - 24 * 3600 * 1000,
            'endTime': int(time.time() * 1000),
            'span': span,
            'token':watchToken
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_HASHRATE_WATCH, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200


    '''获取观察者链接收益算力统计'''
    def getMinerEarnSummaryWatch(self, headers, watchToken):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_MINER_EARN_SUMMARY_WATCH + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)

        params = {
            'token': watchToken,
            'startTime': int(time.time() * 1000) - 48 * 3600 * 1000,
            'endTime': int(time.time() * 1000)
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_MINER_EARN_SUMMARY_WATCH, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200

    '''获取观察者链接收益列表'''
    def getMinerEarnListWatch(self, headers, watchToken):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_MINER_EARNLIST_WATCH + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)

        params = {
            'token': watchToken,
            'startTime': int(time.time() * 1000) - 48 * 3600 * 1000,
            'endTime': int(time.time() * 1000),
            'page': 1,
            'pageSize': 10
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_MINER_EARNLIST_WATCH, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200



    '''#获取观察者链接矿机列表'''
    def getWorkerListWatch(self,headers,watchToken):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_WORKER_LIST_WATCH + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)

        params = {
            'page': 1,
            'pageSize': 10,
            'sort': 'workerFullName',
            'orderBy': 'desc',
            'search': '',
            'status': 0,
            'token':watchToken
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        # dataJson = json.JSONEncoder().encode(data)
        # allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_WORKER_LIST_WATCH, headers=headers,params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200

    '''删除观察者'''
    def deleteWatch(self,headers,wathcId):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + DELETE_WATCH + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)

        params = {
            'observeId':wathcId
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + DELETE_WATCH, headers=headers,params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200


    '''修改收藏'''
    def favorites(self,headers,isDelete,observeId=0):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + FAVORITES + "</h1>", name='url',attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            "delete": isDelete,
            "url": "http://ehash.test.poolx.io/watchDashboard/watchId=0fdff0a915cf49c07006e21aab43f8ef",
            "remark": "123",
            'observeId':observeId
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + FAVORITES, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200

    '''获取收藏者列表'''
    def getFavList(self,headers):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + GET_FAVLIST + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + GET_FAVLIST, headers=headers)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200

        return response.json()['data']['favList'][0]['uid']



    '''获取邀请码'''
    def createUserInvitationCode(self,headers):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + CREATE_USER_INVITATION_CODE + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + CREATE_USER_INVITATION_CODE, headers=headers)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200
        return response.json()['data']['invitation_code']


    '''获取邀请页面大部分数据的接口'''
    def getUserInvitationInfo(self,headers):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + GET_USER_INVITATION_INFO + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + GET_USER_INVITATION_INFO, headers=headers)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200

    '''换绑返佣子账号'''
    def updateCommissionMinerId(self,headers,minerId):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + UPDATE_COMMISSION_MINERID + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        params = {
            'minerId':minerId
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + UPDATE_COMMISSION_MINERID, headers=headers,params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200

    '''统计渠道邀请码'''
    def callInvitationCode(self,code):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + CALL_INVITATION_CODE + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        params = {
            'code':code
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + CALL_INVITATION_CODE, headers=headers,params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200


    '''获取子账号设置'''
    def getMinerSetting(self,headers,minerId):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_MINER_SETTING + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        params = {
            'minerId': minerId
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_MINER_SETTING, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200



    '''二次验证发送邮箱验证码'''
    def getPayAddressCode(self,headers,minerId):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + GET_PAYADDRESS_CODE + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        params = {
            'minerId': minerId
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + GET_PAYADDRESS_CODE, headers=headers,params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200


    '''配置子账号设置'''
    def minerSetting(self,headers,minerId,coinType,emailCode):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + MINER_SETTING + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            "billNotificationEnabled": True,
            "coinType": coinType,
            "minerId": minerId,
            "withdrawAddress": "0x05ebf81e06396658fc56333cbfe6e125ce1d7f1f",
            "locked": False,
            "withdrawMinAmount": "100000000000000000",
            "validatorCode": emailCode
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=NEW_EHASHPOOL_ADDRESS + MINER_SETTING, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200


    '''获取子账号通知配置列表'''
    def getMinerNotifySettingList(self,headers,uid):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_MINER_NOTIFYSETTING_LIST + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        params = {
            'uid': uid,
            'page':1,
            'pageSize':10
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_MINER_NOTIFYSETTING_LIST, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200


    '''获取子账号通知配置'''
    def getMinerNotifySetting(self,headers,minerId):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + GET_MINER_NOTIFYSETTING + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        params = {
            'minerId': minerId
        }
        allure.attach("<h1>" + str(params) + "</h1>", name='params', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=NEW_EHASHPOOL_ADDRESS + GET_MINER_NOTIFYSETTING, headers=headers, params=params)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200


    '''配置子账号设置'''
    def editMinerNotifySetting(self, headers, minerId, coinType):
        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + EDIT_MINER_NOTIFYSETTING + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            "coinType": coinType,
            "emails": "1035717636@qq.com,1035717636@qq.com,1035717636@qq.com",
            "enabled": 1,
            "interval": 3600,
            "minerId": minerId,
            "phones": ""
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=NEW_EHASHPOOL_ADDRESS + EDIT_MINER_NOTIFYSETTING, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200

    '''打开或关闭账号通知'''
    def enabledMinerNotifySetting(self,headers,coinType,minerId,enable):

        allure.attach("<h1>" + NEW_EHASHPOOL_ADDRESS + ENABLED_MINER_NOTIFYSETTING + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
             "coinType": coinType,
             "enabled": enable,
             "minerId": minerId
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=NEW_EHASHPOOL_ADDRESS + ENABLED_MINER_NOTIFYSETTING, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200



    '''google密钥获取'''
    def createSecret(self,headers):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + CREATE_SECRET + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>GET</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        response = requests.get(url=OLD_EHASHPOOL_ADDRESS + CREATE_SECRET, headers=headers)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)
        assert int(response.json()['code']) == 200
        return response.json()['data']['secretKey']


    '''google验证绑定'''
    def confirmGoogle(self,headers,secretKey,GACode,status):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + CONFIRM_GOOGLE + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            "GACode": GACode,
            "secretKey": secretKey,
            "status": status
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + CONFIRM_GOOGLE, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200


    '''删除子账号'''
    def deletedMiner(self,headers,minerId,uid):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + DELETE_DMINER + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
            "minerId": minerId,
            "uid": uid
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + DELETE_DMINER, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200



    '''工单提交'''
    def submitWorkerOrder(self,headers):
        allure.attach("<h1>" + OLD_EHASHPOOL_ADDRESS + SUBMIT_WORKER_ORDER + "</h1>", name='url',
                      attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>POST</h1>", name='method', attachment_type=allure.attachment_type.HTML)
        allure.attach("<h1>" + str(headers) + "</h1>", name='headers', attachment_type=allure.attachment_type.HTML)
        data = {
              "content": "test",
              "email": EMAIL,
              "title": "test",
              "url": [
                "http:test.com"
              ]
        }
        dataJson = json.JSONEncoder().encode(data)
        allure.attach("<h1>" + str(data) + "</h1>", name='requestData', attachment_type=allure.attachment_type.HTML)
        response = requests.post(url=OLD_EHASHPOOL_ADDRESS + SUBMIT_WORKER_ORDER, headers=headers, data=dataJson)
        allure.attach("<h1>" + str(response.json()) + "</h1>", name='responseData',
                      attachment_type=allure.attachment_type.HTML)

        assert int(response.json()['code']) == 200







    # '''流程'''
    # '''首页模块'''
    # @allure.epic("EhashPool")
    # @allure.feature("home")
    # def test_home(self):
    #     self.home() #获取首页数据



    '''注册模块'''
    @allure.epic("EhashPool")
    @allure.feature("singUp")
    def test_singUp(self):

        with allure.step('step1:sendEmailCode'):
            self.sendEmailCode(EMALIL_CODE_SINGUP) #发送注册验证码

        with allure.step('step2:checkUserSignIn'):
            self.checkUserSignIn() #检查验证码

        with allure.step('step3:addETHUser'):
            self.addETHUser() #注册用户


    '''算力模块'''
    @allure.epic("EhashPool")
    @allure.feature("hashRate")
    def test_hashRate(self):
        RP_Token = ''

        with allure.step('step1:login'):
            RP_Token = self.login() #登陆

        '''将RP_Token加入headers'''
        newHeaders = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'RP-Token':RP_Token
        }
        uid = mysqlUtil.getUidWithEmail()

        with allure.step('step2:createMiner'):
            self.createMiner(newHeaders,uid) #创建子账户



    #     minerName = ''
    #     minerId = ''
    #     with allure.step('step3:getMinerList'):
    #         minerName,minerId = self.getMinerList(newHeaders,uid) #获取子账户列表
    #
    #
    #
    #     with allure.step('step4:checkMinerName'):
    #         self.checkMinerName(minerName) #检查子账户名称



    #
    #     with allure.step('step5:getStatSummary'):
    #         newHeaders['Miner-Id'] = str(minerId)
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getStatSummary(newHeaders,minerId)#获取子账号汇总数据
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getStatSummary(newHeaders,minerId)
    #
    #     with allure.step('step6:getHashRate'):
    #         newHeaders['Miner-Id'] = str(minerId)
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getHashRate(newHeaders,minerId,'10m')#获取子账号算力图表
    #         self.getHashRate(newHeaders, minerId, '1h')
    #         self.getHashRate(newHeaders, minerId, '1d')
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getHashRate(newHeaders, minerId, '10m')
    #         self.getHashRate(newHeaders, minerId, '1h')
    #         self.getHashRate(newHeaders, minerId, '1d')
    #
    #
    #     with allure.step('step7:exportHashrate'):
    #         newHeaders['Miner-Id'] = str(minerId)
    #         newHeaders['Coin-Type'] = 'ETC'
    #
    #         self.exportHashrate(newHeaders,minerId,'1h')# #导出子账号算力图表
    #         count = getRowsCount('./download/hashRate1hETC.xlsx','ETC1')
    #         assert count==1+24 #表头+数据
    #
    #         self.exportHashrate(newHeaders, minerId, '10m')
    #         count = getRowsCount('./download/hashRate10mETC.xlsx', 'ETC1')
    #         assert count == 1 + 144  # 表头+数据
    #
    #         self.exportHashrate(newHeaders, minerId, '1d')
    #         count = getRowsCount('./download/hashRate1dETC.xlsx', 'ETC1')
    #         assert count == 1 + 1  # 表头+数据
    #
    #
    #
    #         newHeaders['Coin-Type'] = 'ETH'
    #
    #         self.exportHashrate(newHeaders, minerId, '1h')
    #         count = getRowsCount('./download/hashRate1hETH.xlsx', 'ETH1')
    #         assert count == 1 + 24  # 表头+数据
    #
    #         self.exportHashrate(newHeaders, minerId, '10m')
    #         count = getRowsCount('./download/hashRate10mETH.xlsx', 'ETH1')
    #         assert count == 1 + 144  # 表头+数据
    #
    #         self.exportHashrate(newHeaders, minerId, '1d')
    #         count = getRowsCount('./download/hashRate1dETH.xlsx', 'ETH1')
    #         assert count == 1 + 1  # 表头+数据

        # '''有问题'''
        # with allure.step('step8:submitWorkerOrder'):
        #     self.submitWorkerOrder(newHeaders)#提交工单





    # '''工人模块'''
    # @allure.epic("EhashPool")
    # @allure.feature("worker")
    # def test_worker(self):
    #     RP_Token = ''
    #
    #     with allure.step('step1:login'):
    #         RP_Token = self.login() #登陆
    #
    #     '''将RP_Token加入headers'''
    #     newHeaders = {
    #         'accept': 'application/json',
    #         'Content-Type': 'application/json',
    #         'RP-Token':RP_Token
    #     }
    #     uid = mysqlUtil.getUidWithEmail()
    #     minerName = ''
    #     minerId = ''
    #     with allure.step('step2:getMinerList'):
    #         minerName,minerId = self.getMinerList(newHeaders,uid) #获取子账户列表
    #
    #     with allure.step('step3:getWorkerList'):
    #         newHeaders['Miner-Id'] = str(minerId)
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getWorkerList(newHeaders,minerId)##获取矿机列表
    #     secretKey = ''
    #     with allure.step('step12:createSecret'):
    #         secretKey = self.createSecret(newHeaders)  # google密钥获取
    #
    #     with allure.step('step13:confirmGoogle'):
    #         googleCode = int(getGoogleCode(secretKey))
    #         self.confirmGoogle(newHeaders, secretKey, googleCode, 1)  # google验证绑定
    #         googleCode = int(getGoogleCode(secretKey))
    #         self.confirmGoogle(newHeaders, secretKey, googleCode, 0)  # google验证解除



    # '''账户管理模块'''
    # @allure.epic("EhashPool")
    # @allure.feature("accountOpertion")
    # def test_account(self):
    #
    #     with allure.step('step1:sendEmailCode'):
    #         self.sendEmailCode(EMALIL_CODE_FORGOT_PASSWORD) #发送忘记密码邮箱验证码
    #
    #
    #     with allure.step('step2:checkEmailCode'):
    #         self.checkUserEmail(EMALIL_CODE_FORGOT_PASSWORD)#重置密码邮箱校验
    #
    #     with allure.step('step3:updatePassword'):
    #         self.forgot()#修改密码
    #
    #     RP_Token = ''
    #
    #     with allure.step('step4:login'):
    #         RP_Token = self.login() #登陆
    #
    #     '''将RP_Token加入headers'''
    #     newHeaders = {
    #         'accept': 'application/json',
    #         'Content-Type': 'application/json',
    #         'RP-Token':RP_Token
    #     }
    #     uid = mysqlUtil.getUidWithEmail()
    #
    #     with allure.step('step5:loginHIstory'):
    #         self.loginHistory(newHeaders)#获取登陆历史
    #
    #     with allure.step('step6:info'):
    #         self.info(newHeaders)#获取用户信息
    #
    #
    #     with allure.step('step7:updateETHUser'):
    #         self.updateETHUser(headers,uid)#更新用户信息
    #
    #     with allure.step('step8:sendEmailCode'):
    #         self.sendEmailCode(EMALIL_CODE_SECOND_AUTH_ON)#发送开启二次验证的验证码
    #     with allure.step('step9:checkEmailCode'):
    #         self.checkUserEmail(EMALIL_CODE_SECOND_AUTH_ON)#开启二次验证校验
    #     with allure.step('step:10:updateSecondAuth'):
    #         code = redisUtil.getEmailCode(EMALIL_CODE_SECOND_AUTH_ON)
    #         self.updateSecondAuth(newHeaders,1,code)#开启二次验证
    #
    #     with allure.step('step11:sendEmailCode'):
    #         self.sendEmailCode(EMALIL_CODE_SECOND_AUTH_LOGIN)#发送二次验证登陆验证码
    #
    #     with allure.step('step12:loginBysecondAuth'):
    #         code = redisUtil.getEmailCode(EMALIL_CODE_SECOND_AUTH_LOGIN)
    #         RP_Token = self.login(verifyCode=code)#二次验证登陆
    #
    #     newHeaders['RP-Token'] = RP_Token
    #
    #     with allure.step('step8:sendEmailCode'):
    #         self.sendEmailCode(EMALIL_CODE_SECOND_AUTH_OFF)#发送关闭二次验证的验证码
    #     with allure.step('step9:checkEmailCode'):
    #         self.checkUserEmail(EMALIL_CODE_SECOND_AUTH_OFF)#关闭二次验证校验
    #     with allure.step('step:10:updateSecondAuth'):
    #         code = redisUtil.getEmailCode(EMALIL_CODE_SECOND_AUTH_OFF)
    #         self.updateSecondAuth(newHeaders,0,code)#关闭二次验证








    #
    # '''收益模块'''
    # @allure.epic("EhashPool")
    # @allure.feature("earn")
    # def test_earn(self):
    #
    #
    #     RP_Token = ''
    #     with allure.step('step1:login'):
    #         RP_Token = self.login() #登陆
    #
    #     '''将RP_Token加入headers'''
    #     newHeaders = {
    #         'accept': 'application/json',
    #         'Content-Type': 'application/json',
    #         'RP-Token':RP_Token
    #     }
    #     uid = mysqlUtil.getUidWithEmail()
    #
    #
    #     minerName = ''
    #     minerId = ''
    #     with allure.step('step2:getMinerList'):
    #         minerName,minerId = self.getMinerList(newHeaders,uid) #获取子账户列表
    #
    #
    #     newHeaders['Miner-Id'] = str(minerId)
    #
    #     with allure.step('step3:getMinerEarnSummary'):
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getMinerEarnSummary(newHeaders,minerId)#获取用户子账号天收益图表数据
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getMinerEarnSummary(newHeaders, minerId)
    #
    #
    #     with allure.step('step4:getMinerEarnList'):
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getMinerEarnList(newHeaders,minerId)#获取用户子账号收益列表
    #
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getMinerEarnList(newHeaders,minerId)#获取用户子账号收益列表
    #
    #     with allure.step('step5:getPaymentRecordList'):
    #         newHeaders['Coin-Type'] = 'ETC'
    #         newHeaders['timezone'] = '8'
    #         self.getPaymentRecordList(newHeaders,minerId)#获取用户子账号收益列表
    #
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getPaymentRecordList(newHeaders,minerId)#获取用户子账号收益列表


    #
    # '''观察者模块'''
    # @allure.epic("EhashPool")
    # @allure.feature("watch")
    # def test_watch(self):
    #     RP_Token = ''
    #     with allure.step('step1:login'):
    #         RP_Token = self.login() #登陆
    #
    #     '''将RP_Token加入headers'''
    #     newHeaders = {
    #         'accept': 'application/json',
    #         'Content-Type': 'application/json',
    #         'RP-Token':RP_Token
    #     }
    #     uid = mysqlUtil.getUidWithEmail()
    #     minerName = ''
    #     minerId = ''
    #     with allure.step('step2:getMinerList'):
    #         minerName,minerId = self.getMinerList(newHeaders,uid) #获取子账户列表
    #
    #     newHeaders['Miner-Id'] = str(minerId)
    #
    #     with allure.step('step3:createObserveLink'):
    #         self.createObserveLink(newHeaders,minerId)#创建观察者连接
    #
    #     watchToken = ''
    #     watchId = ''
    #     with allure.step('step4:watch'):
    #         watchToken,watchId = self.watch(newHeaders)#获取观察者列表
    #
    #
    #     with allure.step('step5:getMiner'):
    #         self.getMiner(watchToken)#获取观察者链接子账号信息
    #
    #     with allure.step('step5:getStatSummaryWatch'):
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getStatSummaryWatch(newHeaders,watchToken)#获取观察者链接权限
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getStatSummaryWatch(newHeaders, watchToken)  # 获取观察者链接权限
    #
    #     with allure.step('step6:getHashRateWatch'):
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getHashRateWatch(newHeaders,'10m',watchToken)#获取观察者链接算力统计
    #         self.getHashRateWatch(newHeaders, '1h', watchToken)  # 获取观察者链接算力统计
    #         self.getHashRateWatch(newHeaders, '1d', watchToken)  # 获取观察者链接算力统计
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getHashRateWatch(newHeaders,'10m',watchToken)#获取观察者链接算力统计
    #         self.getHashRateWatch(newHeaders, '1h', watchToken)  # 获取观察者链接算力统计
    #         self.getHashRateWatch(newHeaders, '1d', watchToken)  # 获取观察者链接算力统计
    #
    #     with allure.step('step7:getMinerEarnSummaryWatch'):
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getMinerEarnSummaryWatch(newHeaders,watchToken)#获取观察者链接收益算力统计
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getMinerEarnSummaryWatch(newHeaders,watchToken)#获取观察者链接收益算力统计
    #
    #     with allure.step('step8:getMinerEarnListWatch'):
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getMinerEarnListWatch(newHeaders,watchToken)#获取观察者链接收益列表
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getMinerEarnListWatch(newHeaders,watchToken)#获取观察者链接收益列表
    #
    #     with allure.step('step9:getWorkerListWatch'):
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getWorkerListWatch(newHeaders,watchToken)#获取观察者链接矿机列表
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getWorkerListWatch(newHeaders,watchToken)#获取观察者链接矿机列表
    #
    #     with allure.step('step10:deleteWatch'):
    #         self.deleteWatch(newHeaders,watchId)#删除观察者连接
    #
    #     with allure.step('step11:addFavorites'):
    #         self.favorites(newHeaders,0)#新增收藏者
    #
    #     favId = ''
    #     with allure.step('step11:getFavList'):
    #         favId = self.getFavList(newHeaders)#获取收藏连接
    #
    #
    #     with allure.step('step12:deleteFavorites'):
    #         self.favorites(newHeaders,1,favId)#删除收藏



    # '''邀请模块'''
    # @allure.epic("EhashPool")
    # @allure.feature("invitation")
    # def test_invitation(self):
    #
    #     RP_Token = ''
    #     with allure.step('step1:login'):
    #         RP_Token = self.login()  # 登陆
    #
    #     '''将RP_Token加入headers'''
    #     newHeaders = {
    #         'accept': 'application/json',
    #         'Content-Type': 'application/json',
    #         'RP-Token': RP_Token
    #     }
    #
    #     invitationCode = ''
    #     with allure.step('step2:createUserInvitationCode'):
    #         invitationCode = self.createUserInvitationCode(newHeaders)#获取邀请码
    #
    #     with allure.step('step3:getUserInvitationInfo'):
    #         self.getUserInvitationInfo(newHeaders)#获取邀请页面大部分数据的接口
    #
    #     uid = mysqlUtil.getUidWithEmail()
    #     minerName = ''
    #     minerId = ''
    #     with allure.step('step4:getMinerList'):
    #         minerName,minerId = self.getMinerList(newHeaders,uid) #获取子账户列表
    #
    #     with allure.step('step5:updateCommissionMinerId'):
    #         self.updateCommissionMinerId(newHeaders,minerId)#换绑返佣子账号
    #
    #     with allure.step('step6:callInvitationCode'):
    #         self.callInvitationCode(invitationCode)#统计渠道邀请码



    # '''子账号设置模块'''
    # @allure.epic("EhashPool")
    # @allure.feature("minerSetting")
    # def test_minerSetting(self):
    #     RP_Token = ''
    #     with allure.step('step1:login'):
    #         RP_Token = self.login()  # 登陆
    #
    #     '''将RP_Token加入headers'''
    #     newHeaders = {
    #         'accept': 'application/json',
    #         'Content-Type': 'application/json',
    #         'RP-Token': RP_Token
    #     }
    #
    #     uid = mysqlUtil.getUidWithEmail()
    #     minerName = ''
    #     minerId = ''
    #     with allure.step('step2:getMinerList'):
    #         minerName, minerId = self.getMinerList(newHeaders, uid)  # 获取子账户列表
    #
    #
    #     with allure.step('step3:getMinerSetting'):
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getMinerSetting(newHeaders,minerId)#获取子账号设置
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getMinerSetting(newHeaders,minerId)#获取子账号设置
    #
    #     with allure.step('step4:getPayAddressCode'):
    #         newHeaders['Miner-Id'] = str(minerId)
    #         self.getPayAddressCode(newHeaders,minerId)#二次验证发送邮箱验证码
    #
    #
    #     code = redisUtil.getSettingMinerEmailCode(minerId)#二次验证码
    #
    #     with allure.step('step5:minerSettingETH'):
    #         self.minerSetting(newHeaders,minerId,'ETH',code)#配置子账号设置
    #
    #     '''防止60秒重复发送'''
    #     time.sleep(120)
    #     with allure.step('step6:getPayAddressCode'):
    #         newHeaders['Miner-Id'] = str(minerId)
    #         self.getPayAddressCode(newHeaders, minerId)  # 二次验证发送邮箱验证码
    #
    #     code = redisUtil.getSettingMinerEmailCode(minerId)  # 二次验证码
    #     with allure.step('step7:minerSettingETC'):
    #         self.minerSetting(newHeaders, minerId, 'ETC', code)  # 配置子账号设置
    #
    #
    #     with allure.step('step8:getMinerNotifySettingList'):
    #         newHeaders['Coin-Type']='ETH'
    #         self.getMinerNotifySettingList(newHeaders,uid)#获取子账号通知配置列表
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getMinerNotifySettingList(newHeaders, uid)  # 获取子账号通知配置列表
    #
    #
    #     with allure.step('step9:getMinerNotifySetting'):
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.getMinerNotifySetting(newHeaders,minerId)#获取子账号通知配置
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.getMinerNotifySetting(newHeaders, minerId)  # 获取子账号通知配置
    #
    #
    #     with allure.step('step10:editMinerNotifySetting'):
    #         newHeaders['Coin-Type'] = 'ETH'
    #         self.editMinerNotifySetting(newHeaders,minerId,'ETH')
    #         newHeaders['Coin-Type'] = 'ETC'
    #         self.editMinerNotifySetting(newHeaders,minerId,'ETC')
    #
    #
    #     with allure.step('step11:enabledMinerNotifySetting'):
    #         self.enabledMinerNotifySetting(newHeaders,'ETH',minerId,1)#设置子账户通知
    #         self.enabledMinerNotifySetting(newHeaders, 'ETC', minerId, 1)  # 设置子账户通知
    #
    #     with allure.step('step11:deletedMiner'):
    #         self.deletedMiner(newHeaders,minerId,uid)#删除子账号


































