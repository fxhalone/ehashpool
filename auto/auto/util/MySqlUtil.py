import pymysql
from auto.util.config import *


class MySqlUtil:

    '''获取ehash连接'''
    def getEhashMysqlConnect(self):
        connect = pymysql.Connect(
            host=EHASH_MYSQL_HOST,
            port=EHASH_MYSQL_PORT,
            user=EHASH_MYSQL_USER,
            passwd=EHASH_MYSQL_PASSWORD,
            db='ethpool_rpc_poolhub',
            charset='utf8'
        )
        return connect

    '''删除账号，初始化数据'''
    def initEhashAccount(self):
        connect = self.getEhashMysqlConnect()
        cursor = connect.cursor()
        sql = "delete from eth_user where email = '"+ EMAIL +"'"
        cursor.execute(sql)
        sql = 'commit'
        cursor.execute(sql)
        connect.close()

    def getUidWithEmail(self):
        connect = self.getEhashMysqlConnect()
        cursor = connect.cursor()
        sql = "select uid from eth_user where email = '" + EMAIL + "'"
        cursor.execute(sql)
        uid = cursor.fetchall()[0][0]
        connect.close()
        return uid

    def getGoogleSecretByEmail(self):
        connect = self.getEhashMysqlConnect()
        cursor = connect.cursor()
        sql = "select google_secret from eth_user where email =  '" + EMAIL + "'"
        cursor.execute(sql)
        googleSecret = cursor.fetchall()[0][0]
        connect.close()
        return googleSecret


if __name__ == '__main__':
    mysqlUtil = MySqlUtil()
    print(mysqlUtil.getGoogleSecretByEmail())
