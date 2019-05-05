# -*-coding:utf_8-*-
import re
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
"""接收邮件"""


class MailInfo(object):
    """
    用于临时保存邮件信息的类
    """
    def __init__(self):
        self.index = 0
        self.size = 0
        self.status = ""
        self.data = ""


def get_msg(user_account, password, debuglevel=1, limits=1):
    n = 0
    str = r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$'
    if re.match(str, user_account):
        while n < limits:
            pop3_server = 'pop.' + user_account.split('@')[-1]      # 解析邮箱账号得到邮件服务器地址
            server = poplib.POP3(pop3_server)                       # 连接到服务器
            # server.set_debuglevel(debuglevel)                       # 可选：1为打开，验证连接到邮件服务器
            # print(server.getwelcome().decode('utf8'))             # 打印POP3服务器的欢迎文字，验证连接邮件服务器
            server.user(user_account)                               # 身份验证
            server.pass_(password)
            resp, mails, octets = server.list()                     # 使用list()返回所有邮件的编号
            index = len(mails)
            if index < 1:
                return None
            resp, lines, octets = server.retr(index-n)
            msg_content = b'\r\n'.join(lines).decode('utf-8')  # 可以获得整个邮件的原始文本:
            msg = Parser().parsestr(msg_content)  # 解析出邮件:
            server.close()
            print('****************** 第%d封邮件 *****************' % (n + 1))
            print_info(msg)
            n += 1
    else:
        print('------错误！请检查邮箱账号！------')


# 转码
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


# indent用于缩进显示:
def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'Subject']:    # 获取发件人、发件箱、主题,获取收件人在列表加 'To'
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)    # 读取发件人、发件箱
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if msg.is_multipart():             # 判断内容是否有用
        parts = msg.get_payload()      # 解码并且打印到控制台。循环有两次，第一次是单纯字符串，第二次循环打印的是像HTML的格式
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)      # 解码
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))


user_accounts = input('账号：')
passwords = input('授权码：')
limit = int(input('查看最近邮件数：'))
get_msg(user_accounts, passwords, limit)
