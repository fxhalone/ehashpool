from auto.util.config import *
from auto.util.RedisUtil import *
import time
import json
import random
import requests
redisUtil= RedisUtil()

# data = {
#     'username': "test"+str(random.randint(1,100000)),
#     'email': "1035717636@qq.com",
#     'password': "a1234567",
#     'verification_code': redisUtil.getEmailCode()
# }
# dataJson = json.JSONEncoder().encode(data)
# response = requests.post(url=OLD_EHASHPOOL_ADDRESS + ADD_ETH_USER, headers=headers, data=dataJson)
#
#
# assert int(response.json()['code']) == 200
# print(response.json())
#
#
# print('DeletedMiner'.upper())

#
# print(971.68-97.16)
# print(874.51*0.8)