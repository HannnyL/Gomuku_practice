from oop_connect import Connect
import time
from public_ip_request import get_public_ip
from oop_message import Message

class config:
    SERVER = '1'
    CLIENT = '2'
    LOCAL_HOST = 'localhost'
    LOCAL_PORT = 4567
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 4567
    SEND = '1'
    RECEIVE = '2'



def get_config():

    #选择运行模式(服务/客户端)
    while True:
        mode = input("请选择运行模式\n1 - 服务器模式\n2 - 客户端模式\n输入对应编号即可：").strip()
        match mode:
            case config.SERVER:
                is_server = True
                break
            case config.CLIENT:
                is_server = False
                break
            case _:
                print("\n输入错误，请重新输入\n")

    #选择连接模式(本地/网络)
    while True:
        mode = input("\n请选择连接模式\n1 - 本地连接\n2 - 网络连接\n输入对应编号即可：")
        match mode:
            case '1':
                localmodel = True
                break
            case '2':
                localmodel = False
                break
            case _:
                print("\n输入错误，请重新输入")

    #设置HOST和PORTS
    if localmodel == True:
        #本地连接使用默认参数
        HOST = config.LOCAL_HOST
        PORTS = config.LOCAL_PORT
        #return is_server,HOST,PORTS
        return is_server,HOST,PORTS
    else:
        #网络连接时，服务器使用默认参数
        if is_server == True:
            #服务器模式使用0.0.0.0
            HOST = config.SERVER_HOST
            PORTS = config.SERVER_PORT
            #获取并显示公网IP
            print(f"\n您的公网ip为:{get_public_ip()}")
        else: 
            #客户端模式获取用户输入               
            while True:
                try:
                    HOST = input("\n请输入主机地址(例:127.0.0.1)：")
                    if HOST == '':
                        print("\n地址不能为空，请重新输入")
                        continue
                    for i in range(4):
                        if 0 <= int(HOST.split('.')[i]) <= 255:
                            continue
                        else:
                            raise ValueError("\n地址每项应为0-255，请重新输入")
                    if len(HOST) < 7 or len(HOST) > 15:
                        print("\n地址长度错误，请重新输入")
                        continue
                    else:
                        break
                except ValueError as v:
                    print(v)
                    continue
                except:
                    print("\n主机地址应为数字，请重新输入")
                    continue
        #设置端口号
        #端口号范围为0-65535，且不能为0
        while True:
            PORTS = input("\n请输入端口号(例:4567)：") or 4567
            # if PORTS == '':
            #     print("\n端口号不能为空，请重新输入")
            #     continue
            if PORTS == 0:
                print("\n端口号不能为0，请重新输入")
                continue
            elif PORTS < 0:
                print("\n端口号不能为负数，请重新输入")
                continue
            elif PORTS > 65535:
                print("\n端口号不能超过65535，请重新输入")
                continue
            elif PORTS < 1024:
                print("\n端口号不能低于1024，此区段为系统预留，请重新输入")
                continue           
            else:
                break
        return is_server,HOST,PORTS


#测试开始
def main():
    connect = Connect(*get_config())

    status = input("\n请输入连接状态\n1 - 发送数据\n2 - 接收数据\n输入对应编号即可：").strip()

    match status:
        case config.SEND:
            msg = Message.move(20,6)
            connect.send_message(msg)
            input("\n按任意键继续...")
            msg = Message.flag(True)
            connect.send_message(msg)
            input("\n按任意键继续...")
            msg = Message.chat("你有收到我的消息吗")
            connect.send_message(msg)
            input("\n按任意键继续...")
        case config.RECEIVE:
            for i in range(3):
                typ,msg = connect.recv_message()
                print(f"\n接收到{typ}类消息,内容为：{msg}\n")


    input("\n按任意键继续...")

    for i in range(1,6):
        print(f"{6-i}s后断开连接")
        time.sleep(1)

    connect.close()


if __name__ == "__main__":
    main()


