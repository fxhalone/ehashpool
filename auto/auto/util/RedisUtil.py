import redis
from  util.config import *

class RedisUtil:

    '''获取emailCode验证码'''
    def getEmailCode(self,codeTYpe):
        r = redis.Redis(host=EHASH_REDIS_HOST, port=EHASH_REDIS_PORT, db=EHASH_REDIS_DB,password=EHASH_REDIS_PASSWORD)
        code = ''
        if codeTYpe == EMALIL_CODE_SINGUP:
            code = r.get('EmailCode'+EMAIL+'_Ehashpool')  # 获取注册验证码
        elif codeTYpe == EMALIL_CODE_SECOND_AUTH_LOGIN:
            code = r.get('EmailSecondCode' + EMAIL + '_Ehashpool')  # 获取二次验证登陆验证码
        elif codeTYpe == EMALIL_CODE_SECOND_AUTH_ON:
            code = r.get('SecondOnCode' + EMAIL + '_Ehashpool')  # 获取开启二次验证验证码
        elif codeTYpe == EMALIL_CODE_SECOND_AUTH_OFF:
            code = r.get('SecondOffCode' + EMAIL + '_Ehashpool')  # 获取关闭二次验证验证码
        elif codeTYpe == EMALIL_CODE_FORGOT_PASSWORD:
            code = r.get('ForgetCode' + EMAIL + '_Ehashpool')  # 获取忘记密码验证码
        elif codeTYpe == EMALIL_CODE_UPDATE_PASSWORD:
            code = r.get('ModifyPasswordCode' + EMAIL + '_Ehashpool')  # 获取修改密码验证码
        r.close()
        return code.decode('utf-8')


    '''获取修改子账户二次验证验证码'''
    def getSettingMinerEmailCode(self,minerId):
        r = redis.Redis(host=EHASH_REDIS_HOST, port=EHASH_REDIS_PORT, db=EHASH_REDIS_DB,password=EHASH_REDIS_PASSWORD)
        code = r.get('PayAddressEmailCode_'+str(minerId))  # 获取修改密码验证码
        r.close()
        return code.decode('utf-8')


if __name__ == '__main__':
    a = RedisUtil()
    print(a.getSettingMinerEmailCode(687))
    print(a.getEmailCode(4))

