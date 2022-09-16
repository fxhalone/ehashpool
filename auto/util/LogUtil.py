import logging
import os.path
import time

class LogUtil:



    '''获取logger'''
    @staticmethod
    def initLogger():

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  # Log等级总开关
        #创建一个handler，用于写入日志文件
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))
        log_path = os.path.dirname(os.getcwd()) + '/auto/log/rqtasklog.txt'
        # logfile = log_path + rq + '.log'
        fh = logging.FileHandler(log_path, mode='a')#累加
        fh.setLevel(logging.INFO)
        #定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        #将logger添加到handler里面
        logger.addHandler(fh)
        return logger



if __name__ == '__main__':
    hear = {
        "RP-Token":'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjE5NDc4NTUsImlhdCI6MTY2MTk0NDI1NSwidWlkIjoxMDMxNSwidXNlcm5hbWUiOiIiLCJwaWQiOjB9.trQVfn1TZ6txHBvBFbDguddDubMq8eFGf1NuTq3uAKI'

    }
    import  requests
    response = requests.get(url='http://ehashapi.test.poolx.io/ethGateWay/v1/ethpoolhub/miner/ExportHashrate?minerId=407&startTime=1661940671792&endTime=1661944271792&span=10m',headers=hear)
    print(response.status_code)

    with open('./doctor.xlsx', 'wb') as fd:
        for chunk in response.iter_content():
            fd.write(chunk)