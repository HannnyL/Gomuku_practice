import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))      # 绑定地址和端口
    s.listen()                # 监听
    print("等待连接中...")
    conn, addr = s.accept()   # 接受连接
    with conn:
        print("连接来自：", addr)
        data = conn.recv(1024)         # 接收消息（最多1024字节）
        print("收到消息：", data.decode('utf-8'))
        conn.sendall("你好客户端".encode('utf-8'))     # 发送消息

