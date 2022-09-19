import sys
sys.path.append('..')
from  auto.util.MailUtil import *

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果'''

    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get("passed", []))
    # failed = len(terminalreporter.stats.get("failed", []))
    # error = len(terminalreporter.stats.get("error", []))
    # skipped = len(terminalreporter.stats.get("skipped", []))
    # deselected = len(terminalreporter.stats.get("deselected", []))  # 过滤的用例数
    content = "执行全部数量:"+str(total)+"\n执行通过数量；"+str(passed)


   #发送邮件
    util = MailUtil()
    util.sendMail(content)