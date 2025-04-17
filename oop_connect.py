import socket
import json
from oop_message import Message
import sys

class Connect:

    def __init__(self,is_server,HOST,PORTS):

        self.s = None
        self.conn = None
        self.addr_server = (HOST,PORTS)
        self.addr = (HOST,PORTS)
        self.is_server = is_server

        if is_server:
            self.initial_server()
        else:
            self.initial_client()


    #初始化服务器
    def initial_server(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind(self.addr_server)
        self.s.listen()
        print("等待连接中...")
        self.conn,self.addr = self.s.accept()
        print(f"\n已连接客户端：{self.addr}")

    #初始化客户端
    def initial_client(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #设置连接超时为10s
        #self.s.settimeout(10)
        retry = 10 #设置重试次数
        while True:
            #超出重试次数
            if retry == 0:
                print("\n连接失败，请检查服务器是否开启")
                self.close_socket()
                sys.exit("程序将关闭，请稍后重启重试")
            #尝试连接
            try:
                self.s.connect(self.addr)
                break
            except ConnectionRefusedError:
                retry -= 1
                print(f"服务器未响应，正在尝试重新连接至服务器：{self.addr}")
                continue
            except TimeoutError:
                retry -= 5
                print(f"连接超时，正在尝试重新连接至服务器：{self.addr}")
                continue
        print(f"\n已连接至服务器：{self.addr}")

    #todo: 发送成功后等待对方的接收成功标志
    def send_message(self,msg):
            try:
                #发送消息
                if self.is_server:
                    self.conn.sendall(msg)
                else:
                    self.s.sendall(msg)
            except (ConnectionResetError, BrokenPipeError,OSError):
                self.reconnect()
                self.send_message(msg)
            except Exception as e:
                print(f"发送失败：{e}")

    #todo:接收成功后发送接收成功标志
    def recv_message(self):
        try:
            #接收消息
            if self.is_server:
                data = self.conn.recv(1024)
            else:
                data = self.s.recv(1024)
            msg = json.loads(data.decode('utf-8'))
            return msg['type'], msg['payload']
        except (ConnectionResetError, BrokenPipeError,OSError):
            self.reconnect()
            self.recv_message()     
        except Exception as e:
            print(f"发送失败：{e}")

    def reconnect(self):
        print("\n连接已断开，正在尝试重新连接...")
        if self.is_server:
            self.conn.close()
            self.conn,self.addr = self.s.accept()
            print(f"\n已重新连接至：{self.addr}")
        else:
            self.s.close()
            self.initial_client()


    def close_socket(self):
        if self.conn:
            self.conn.close()
            print(f"已断开来自{self.addr}的连接")
        if self.s:
            self.s.close()
            print(f"已断开与服务器的连接")