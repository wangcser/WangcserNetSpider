import time
import os
import smtplib #发送邮件
from email import encoders # 附件编码
from email.mime.base import MIMEBase # 附件标记
from email.mime.multipart import MIMEMultipart # 多类型邮件容器
from email.mime.text import MIMEText # 纯文本类型邮件

def send_email(report_text=' ', file_path='C:/users/superequs/desktop/data.db', send_to_addr='wangcser@qq.com'):
    '''
    name: 发送邮件模块
    func: 调用该模块向指定地址发送邮件，已设定默认正文，默认收件人和默认附件，目前不考虑接受log信息（本地调试）
    send_email(attch_text='', file_path='', send_to_addr='')
    '''

    # email 地址与用户口令
    from_addr = "502612842@qq.com"
    password = "bvbekgpwcrslbgha"
    # 收件人地址
    to_addr = send_to_addr # 默认收件地址,默认抄送一份到该地址

    # 构建一个支持附件的邮件容器
    msg = MIMEMultipart()

    # 构造当前时间戳，添加到邮件的主题中
    t = time.localtime()
    time_stamp = str(t.tm_mon) + "." + str(t.tm_mday) + " " + str(
        t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec)
    subject = '[' + time_stamp + '] ' + 'Crawler Run Report'

    # 填写邮件头信息
    msg["Subject"] = subject # 邮件主题
    msg["From"]    = from_addr
    msg["To"]      = to_addr

    # 填写邮件正文信息
    # 默认正文内容
    header_text = '''
    该邮件由crawler自动生成发送，下方为本次爬取情况：
    '''
    # 希望 attch_text给出：爬虫名，运行时间，爬取数量，
    mime_text = MIMEText(header_text + report_text, 'plain', 'utf-8') # 实例化一个文本邮件对象
    msg.attach(mime_text)

    # 添加邮件附件信息
    with open(file_path,'rb') as f:
        # 设置附件的MIME和文件名
        dir_path = os.path.dirname(file_path)
        file_name = file_path[len(dir_path):] # 获取文件名
        mime = MIMEBase('database', 'db' , filename = file_name)
        # 加上必要的头部信息
        mime.add_header('Content-Disposition', 'attachment', filename=file_name)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 读取附件内容
        mime.set_payload(f.read())
        # 用Base64编码
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart
        msg.attach(mime)
        f.close()

    # 发送邮件
    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # server.set_debuglevel(1) # 输出所有交互信息
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        print("mail send to : " + to_addr)
    except:
        print("mail send falied.")

'''
if __name__  == '__main__':

    send_email()
'''