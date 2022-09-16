'''ehash矿池地址'''
NEW_EHASHPOOL_ADDRESS = 'http://ehashapi.test.poolx.io:81'
OLD_EHASHPOOL_ADDRESS = 'http://ehashapi.test.poolx.io'

'''ehash数据库配置'''
EHASH_MYSQL_HOST = '122.10.161.35'
EHASH_MYSQL_PORT = 3306
EHASH_MYSQL_USER = 'readonly'
EHASH_MYSQL_PASSWORD = 'rawpoolreadonly2018'


'''ehash Redis配置'''
EHASH_REDIS_HOST = '152.32.135.234'
EHASH_REDIS_PORT = 6379
EHASH_REDIS_DB = 0
EHASH_REDIS_PASSWORD = 'z2cyyxgu1qdgflKXfvr'



'''通知邮箱'''
GMAIL_HOST ='smtp.qq.com'
GMAIL_USER = '1035717636@qq.com'
# GMAIL_PASSWORD='fengxiaohui123'
AUTH_KEY = 'hxcmjkvxannwbgag'


'''ehash常用数据'''
EMAIL = '1035717636@qq.com'
ACCOUNT_PASSWORD = 'a1234567'


'''EHASh接口url新'''
HOME = '/pool//v1/miner/Home' #首页数据接口
GET_STAT_SUMMARY = '/pool/v1/miner/GetStatSummary'#获取子账号汇总数据
GET_HASHRATE = '/pool/v1/miner/GetHashRate' #获取子账号算力图表
EXPORT_HASHRATE = '/pool/v1/miner/ExportHashrate' #导出子账号算力图表
GET_WORKER_LIST = '/pool/v1/miner/GetWorkerList' #获取矿机列表
FORGOT = '/ethGateWay/v1/eth/users/forgot' #修改用户密码
GET_MINER_EARN_SUMMARY = '/pool/v1/earn/GetMinerEarnSummary' #获取用户子账号天收益图表数据
GET_MINER_EARNLIST = '/pool/v1/earn/GetMinerEarnList' #获取用户子账号收益列表
GET_PAYMENT_RECORDLIST = '/pool/v1/earn/GetPaymentRecordList' #获取用户付款记录列表
GET_STAT_SUMMARY_WATCH = '/observe/GetStatSummary'#获取观察者链接权限
GET_HASHRATE_WATCH = '/observe/GetHashrate'#获取观察者链接算力统计
GET_MINER_EARN_SUMMARY_WATCH = '/observe/GetMinerEarnSummary'#获取观察者链接收益算力统计
GET_MINER_EARNLIST_WATCH = '/observe/GetMinerEarnList' #获取观察者链接收益列表
GET_WORKER_LIST_WATCH = '/observe/GetWorkerList'#获取观察者链接矿机列表
GET_MINER_SETTING = '/pool/v1/miner/GetMinerSetting'#获取子账号设置
MINER_SETTING = '/pool/v1/miner/MinerSetting'#配置子账号设置
GET_MINER_NOTIFYSETTING_LIST = '/pool/v1/notify/GetMinerNotifySettingList'#获取子账号通知配置列表
GET_MINER_NOTIFYSETTING = '/pool/v1/notify/GetMinerNotifySetting'#获取子账号通知配置
EDIT_MINER_NOTIFYSETTING = '/pool/v1/notify/EditMinerNotifySetting'#设置子账号通知配置
ENABLED_MINER_NOTIFYSETTING = '/pool/v1/notify/EnabledMinerNotifySetting'#打开或关闭账号通知





'''EHASH接口url旧'''
SEND_EMAIL_CODE = '/ethGateWay/v1/eth/users/sendEmailCode' #ETH用户发送邮箱验证码/
CHECK_USER_SIGNIN = '/ethGateWay/v1/eth/users/checkUserSignIn' #ETH用户注册校验'
ADD_ETH_USER = '/ethGateWay/v1/eth/users/addETHUser' #添加用户
LOGIN = '/ethGateWay/v1/eth/users/login' #登陆
CREATE_MINER = '/ethGateWay/v1/ethpoolhub/miner/CreateMiner' #创建子账户
GET_MINER_LIST = '/ethGateWay/v1/ethpoolhub/miner/GetMinerList'
CHECK_MINER_NAME = '/ethGateWay/v1/ethpoolhub/miner/CheckMinerName' #检查子账号
CHECK_USER_EMAIL = '/ethGateWay/v1/eth/users/checkUserEmail' #重置密码邮箱校验
LOGIN_HISTORY = '/ethGateWay/v1/eth/users/loginHistory' #登陆历史
INFO = '/ethGateWay/v1/eth/users/info' #获取用户信息
UPDATE_ETH_USER = '/ethGateWay/v1/eth/users/updateETHUser' #修改用户信息
UPDATE_SECOND_AUTH = '/ethGateWay/v1/eth/users/UpdateSecondAuth' #是否开启二次验证
CREATE_OBSERVE_LINK = '/ethGateWay/v1/eth/observe/createObserveLink' #新增观察者链接
WATCH = '/ethGateWay/v1/eth/observe/watch' #获取观察者列表
DELETE_WATCH = '/ethGateWay/v1/eth/observe/delete'#删除观察者
FAVORITES = '/ethGateWay/v1/eth/observe/favorites'#修改收藏（新增删除）
GET_FAVLIST = '/ethGateWay/v1/eth/observe/getFavList'#获取收藏者列表
CREATE_USER_INVITATION_CODE = '/ethGateWay/v1/eth/users/createUserInvitationCode'#获取邀请码
GET_USER_INVITATION_INFO = '/ethGateWay/v1/eth/users/getUserInvitationInfo'#获取邀请页面大部分数据的接口
UPDATE_COMMISSION_MINERID = '/ethGateWay/v1/eth/users/updateCommissionMinerId' #换绑返佣子账号
CALL_INVITATION_CODE = '/ethGateWay/v1/eth/users/callInvitationCode' #统计渠道邀请码
GET_PAYADDRESS_CODE = '/ethGateWay/v1/ethpoolhub/miner/GetPayAddressCode'#二次验证发送邮箱验证码
CREATE_SECRET = '/ethGateWay/v1/eth/users/CreateSecret'#google密钥获取
CONFIRM_GOOGLE = '/ethGateWay/v1/eth/users/ConfirmGoogle'#google验证绑定
DELETE_DMINER = '/ethGateWay/v1/ethpoolhub/miner/DeletedMiner'#删除子账号
GET_MINER = '/observe/GetMiner'#获取观察者链接子账号信息










'''枚举'''
EMALIL_CODE_SINGUP = 0  #注册
EMALIL_CODE_SECOND_AUTH_LOGIN = 1  #二次验证登陆
EMALIL_CODE_SECOND_AUTH_ON = 3  #二次验证开启
EMALIL_CODE_SECOND_AUTH_OFF = 4  #二次验证关闭
EMALIL_CODE_FORGOT_PASSWORD =5 #忘记密码
EMALIL_CODE_UPDATE_PASSWORD = 6 #修改密码
EMALIL_CODE_UPDATE_MINEF = 7 #修改子账号配置
EMALIL_CODE_UPDATE_PAYMENT_ADDRESS = 8 #修改付款地址































# HOST = 'https://open.rawpool.com'
# HOST = 'http://openbtc.test.r-cluster.com'