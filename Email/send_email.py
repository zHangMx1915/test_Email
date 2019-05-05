import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
"""发送邮件"""


class SendEmail:

    def __init__(self):
        self.send_users = input("输入账号：")
        self.passwords = input("输入授权码：")
        self.user_list = input("收件人：")     # input("Receipt")        # 收件人邮箱

    # 判断附件目录是否为空
    def see_file(self, sub, content):
        work_path = "../Email/annex"
        if not os.listdir(work_path):
            self.send_email(sub, content)
        else:
            for root, dirs, files in os.walk(work_path):
                """
                root: 当前目录路径
                dirs: 当前路径下所有子目录
                files: 当前路径下所有非目录子文件
                """
                for file in files:
                    file_name = root + "/" + file
                    self.file_mail(sub, content, file_name)

    # 发送邮件（纯文本格式）
    def send_email(self, sub, content):
        """
        :param user_list: 收件人邮箱
        :param sub:     主题
        :param content:     内容
        :return:
        """
        email_host = 'smtp.' + self.send_users.split('@')[-1]     # 根据邮箱账号获取不同厂家SMTP服务器地址
        user = 'zhangXin' + '<' + self.send_users + '>'
        message = MIMEText(content, _subtype='plain', _charset='utf-8')
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ';'.join(self.user_list)
        server = smtplib.SMTP()
        server.connect(host=email_host)
        server.login(self.send_users, self.passwords)
        server.sendmail(user, self.user_list, message.as_string())
        server.close()

    # 发送带有附件的邮件
    def file_mail(self, sub, content, file_name):
        # 创建一个带附件的实例
        user = 'zhang' + '<' + self.send_users + '>'
        message = MIMEMultipart()
        message.attach(MIMEText(content, _subtype='plain', _charset='utf-8'))  # 邮件正文内容
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ';'.join(self.user_list)
        # 构造附件
        att1 = MIMEText(open(file_name, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="新建文本文档"'     # 定义附件的名字
        message.attach(att1)
        try:
            # 使用非本地服务器，需要建立ssl连接
            email_host = 'smtp.' + self.send_users.split('@')[-1]
            smtpObj = smtplib.SMTP_SSL(email_host, 465)
            smtpObj.login(self.send_users, self.passwords)
            smtpObj.sendmail(self.send_users, self.user_list, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as se:
            print(f"Error: 无法发送邮件.Case:{se}")


if __name__ == '__main__':
    subs = "测试邮件"
    contents = "全国政协十三届二次会议闭幕习近平李克强栗战书王沪宁赵乐际韩正王岐山出席 汪洋发表讲话新华社北京3月13日电 " \
               "中国人民政治协商会议第十三届全国委员会第二次会议在圆满完成各项议程后，13日上午在人民大会堂闭幕。会议号召，人民政协各级组织、" \
               "各参加单位和广大政协委员，要更加紧密地团结在以习近平同志为核心的中共中央周围，高举中国特色社会主义伟大旗帜，继续奋斗，" \
               "切实把中共中央的决策部署和对人民政协工作的要求落实下去，把海内外中华儿女实现中华民族伟大复兴中国梦的智慧和力量凝聚起来，" \
               "以优异成绩庆祝新中国成立70周年，为决胜全面建成小康社会，为把我国建设成为富强民主文明和谐美丽的社会主义现代化强国作出新的更大贡献。" \
               "会议由中共中央政治局常委、全国政协主席汪洋主持。全国政协副主席张庆黎、刘奇葆、帕巴拉·格列朗杰、董建华、万钢、何厚铧、卢展工、王正伟、" \
               "马飚、陈晓光、梁振英、夏宝龙、杨传堂、李斌、巴特尔、汪永清、何立峰、苏辉、郑建邦、辜胜阻、刘新成、何维、邵鸿、高云龙在主席台前排就座。"
    send_email = SendEmail()
    send_email.see_file(subs, contents)

