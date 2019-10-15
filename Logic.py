from socket import  *
import pymssql
import  numpy as np
con_succ="#2"
ready = "#4"
finished = "#6"
map = {
    "前收盘价": "column4",
    '开盘价': "column5",
    '最高价': "column6",
    '最低价': "column7",
    '收盘价': "column8",
    '成交量': "column9",
    '成交金额': "column10",
    '涨跌': "column11",
    '涨跌幅': "column12",
    '均价': "column13",
    '换手率': "column14",
    "市盈率": "column21",
    '市净率': "column22",
    "市销率": "column23",
    '市现率': "column24",
}

class Handle:
    def __init__(self, port_opened):
        self.port = port_opened
        self.ADDR = ('', self.port)
        self.tcpSerSock = socket(AF_INET, SOCK_STREAM)
        self.tcpSerSock.bind(self.ADDR)
        self.tcpSerSock.listen(5)
        self.tcpCliSock, self.addr = self.tcpSerSock.accept()
        self.tcpCliSock.send(con_succ.encode("utf-8"))
        print(1)
        self.column_name = ""
        self.start_time = ""
        self.end_time = ""

    def receive(self):

        data = self.tcpCliSock.recv(2048).decode("utf-8")
        self.handle_msg(data)
        return data

    def connect_database(self, para1, para2, para3):
        server = "127.0.0.1"  # 连接服务器地址
        user = "sa"              # 连接帐号
        password = "123456789"          # 连接密码
        conn = pymssql.connect(server, user, password, "TEST")
        cursor = conn.cursor()
        cursor.execute("exec get_data @start_time='%s',@end_time='%s',@column= '%s'" % (para1, para2，map[para3])) #map(para3)
        self.result = cursor.fetchall()  # 得到结果集
        self.send_inquire(self.result)

    def send_inquire(self, text):
        str_notice_client = "#4 "+"日期 "+self.column_name
        self.tcpCliSock.send(str_notice_client.encode("utf-8"))

        for column in text:
            msg1 = column[0]
            msg2 = ""
            try:
                msg2 = column[1]
            except error:
                msg2 = "0"
            msg = str(msg1)+" "+str(msg2)
            self.tcpCliSock.recv(2048)
            self.tcpCliSock.send(msg.encode("utf-8"))

        self.tcpCliSock.send(finished.encode("utf-8"))

    def handle_msg(self, msg):
        if msg[0:2] == "#1":
            colnames = msg.split(" ")
            self.start_time = colnames[1]
            self.end_time = colnames[2]
            self.column_name = colnames[3]
            print(self.start_time)
            print(self.end_time)
            print(self.column_name)
            self.connect_database(self.start_time, self.end_time, self.column_name)


server = Handle(2433)
while True:
    try:
        server.receive()
    except error:
        exit(1)


