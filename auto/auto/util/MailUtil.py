import smtplib
from email.mime.text import MIMEText
from email.header import Header
from util.config import *

class MailUtil:

    def sendMail(self):

        sender = GMAIL_USER
        receivers = ['f1035717636@163.com']
        message  = MIMEText('接口自动化执行完成','plain','utf-8')
        message['From'] = Header('自动化客户端','utf-8')
        message['To'] = Header('自动化测试','utf-8')
        message['Subject'] = Header('接口自动化测试执行完毕通知','utf-8')
        server = smtplib.SMTP_SSL(GMAIL_HOST,465)
        server.login(GMAIL_USER,AUTH_KEY)
        server.sendmail(sender,receivers,message.as_string())
        server.quit()
        print('发送成功')


if __name__ == '__main__':
    a  = MailUtil()
    a.sendMail()