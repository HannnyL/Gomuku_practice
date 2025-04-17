import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 不需要真的连接这个地址，只是触发底层分配本地地址
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'  # 获取失败时返回回环地址
    finally:
        s.close()
    return ip

print("您的本地局域网 IP:", get_local_ip())
