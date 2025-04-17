import requests

def get_public_ip():
    try:
        # 使用多个服务提高可靠性
        services = [
            "https://api.ipify.org",          # 纯文本响应
            "https://ipinfo.io/ip",           # 纯文本响应
            "https://httpbin.org/ip",         # JSON 响应 {"origin": "x.x.x.x"}
            "https://ident.me",               # 纯文本响应
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    # 处理不同响应格式
                    if service == "https://httpbin.org/ip":
                        return response.json()["origin"]
                    else:
                        return response.text.strip()
            except:
                continue  # 如果某个服务失败，尝试下一个
        
        raise Exception("所有 IP 查询服务均不可用")
    except Exception as e:
        print(f"获取公网 IP 失败: {e}")
        
#public_ip = get_public_ip()
#print("您的IP:", public_ip)
