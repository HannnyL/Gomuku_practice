
import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))           # 连接服务器
    s.sendall("地方军阀".encode('utf-8'))           # 发送消息
    data = s.recv(1024)               # 接收消息
    print("服务器说：", data.decode('utf-8'))
