import pytest
import os
import shutil
import sys
if __name__ == '__main__':

    #清除历史报告文件
    path = sys.path[0]+'/report/testResults/'
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    #执行测试案例
    pytest.main(['-s'])
    #生成allure报告
    os.system('allure generate ./report/testResults/ -o ./report/reportHtml/ --clean')



