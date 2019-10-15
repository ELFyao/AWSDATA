from socket import *
from tkinter import *
import matplotlib.pyplot as plt
from _datetime import datetime
from tkinter.messagebox import *
from matplotlib import *
"""the first type is axis x and the second type is axis y in matplotlib  picture                           """
"""protocol between client and server                                           """
"""# + odd number-----client send to server  """
"""#1---------------give server the 2 column's name client want to know  """

"""# + even number-------server send to client  """
"""#2-----------------notice client that i had ready (connection success) """
"""#4-----------------notice client i am ready to tell you the results
                      ,ready to receive,also the begin of the whole result set"""
"""#6-----------------the last of message,notice client close the connection ,stop receive"""


class Interaction:
    def __init__(self, address, port):
        self.ADDR = (address, port)
        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)
        self.tcpCliSock.connect(self.ADDR)
        self.tcpCliSock.settimeout(10)
        self.alldata = {}
        self.type1 = "1"
        self.type2 = "2"
        self.last_is_complete = True
        self.window = Tk()
        self.window.minsize(width=400, height=300)
        self.window.maxsize(width=400, height=320)
        self.window.title("数据查询")
        self.UI_wid()
        self.window.mainloop()

    def UI_wid(self):

        self.scrollbar2 = Scrollbar()
        self.listbox2 = Listbox(self.window, selectmode=SINGLE, yscrollcommand=self.scrollbar2.set)

        self.scrollbar2.config(command=self.listbox2.yview)

        for item in ['前收盘价', '开盘价', '最高价', '最低价', '收盘价', '成交量', '成交金额', '涨跌', '涨跌幅', '均价', \
                     '换手率', "市盈率", '市净率', '市销率', '市现率']:
            self.listbox2.insert(END, item)
        self.label_start = Label(self.window, text='Start_date')
        self.Sca_start_Y = Scale(self.window, from_=1999, to=2016, orient=HORIZONTAL)
        self.Sca_start_M = Scale(self.window, from_=1, to=12, orient=HORIZONTAL)
        self.Sca_start_D = Scale(self.window, from_=1, to=30, orient=HORIZONTAL)
        self.label_End = Label(self.window, text='End_date')
        self.Sca_end_Y = Scale(self.window, from_=1999, to=2016, orient=HORIZONTAL)
        self.Sca_end_M = Scale(self.window, from_=1, to=12, orient=HORIZONTAL)
        self.Sca_end_D = Scale(self.window, from_=1, to=30, orient=HORIZONTAL)

        self.label_start.grid(row=0, column=0)
        self.Sca_start_Y.grid(row=1, column=0)
        self.Sca_start_M.grid(row=1, column=1)
        self.Sca_start_D.grid(row=1, column=2)

        self.label_End.grid(row=2, column=0)
        self.Sca_end_Y.grid(row=3, column=0)
        self.Sca_end_M.grid(row=3, column=1)
        self.Sca_end_D.grid(row=3, column=2)

        self.scrollbar2.grid(row=4, column=1, ipady=65)
        self.listbox2.grid(row=4, column=0)

        button_get_data = Button(self.window, width=5, height=1, text="登录", activebackground="red", command= self.get_all)
        button_get_data.grid(row=4, column=2, sticky=SE)
    def recive1(self):
            try:
                self.data = self.tcpCliSock.recv(2048).decode("utf-8")  # seems error

                self.handle_data(self.data)
                return self.data
            except TclError:
                pass
    def handle_data(self,text):
        print(text)
        if text == "#2":
            pass
        elif text[0:2] == "#4":
            print("4 complete")
            self.last_is_complete = False
            datas = text.split(" ")                                 #format "#4 type1 type2"
            self.alldata[datas[1]] = []                             #asume that the type1 at the first place
            self.alldata[datas[2]] = []
            self.type1 = datas[1]
            self.type2 = datas[2]
            self.tcpCliSock.send("1".encode("utf-8"))
        elif text == "#6":
            self.last_is_complete = True
            self.draw()
        else:
            self.tcpCliSock.send("1".encode("utf-8"))
            datas = text.split(" ")
            self.alldata[self.type1].append(datas[0])
            self.alldata[self.type2].append(datas[1])
    def draw(self):
            xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in self.alldata[self.type1]]
            xs2 = [float(x) for x in self.alldata[self.type2]]
            plt.plot(xs, xs2, linewidth=2)
            plt.xlabel("time")
            plt.ylabel(self.type2)
            plt.show()
    def get_all(self):
        if self.last_is_complete:
            self.alldata.clear()
            start_Y = self.Sca_start_Y.get()
            start_M = self.Sca_start_M.get()
            start_D = self.Sca_start_D.get()
            start_time = datetime(start_Y, start_M, start_D)
            Least_time = datetime(1999, 11, 10)

            end_Y = self.Sca_end_Y.get()
            end_M = self.Sca_end_M.get()
            end_D = self.Sca_end_D.get()
            end_time = datetime(end_Y, end_M, end_D)
            Max_time = datetime(2016, 6, 8)

            if start_time > end_time or start_time < Least_time or end_time > Max_time:
                showinfo(message="time_error")
            try:
                str_data_type = self.listbox2.get(self.listbox2.curselection())
            except TclError as e:
                showinfo(message="No choice! default value is the first")
                str_data_type = self.listbox2.get((1,))
            x = str(start_time).split(" ")
            y = str(end_time).split(" ")
            str_notice_msg = "#1 "+x[0]+" "+y[0]+" "+str_data_type
            self.tcpCliSock.send(str_notice_msg.encode("utf-8"))
            while True:
                str_res = self.recive1()
                if str_res[0:2] == "#6":
                    break
        else:
            showinfo(message="wait! last mission didn't complete")


user = Interaction("localhost", 2433)
