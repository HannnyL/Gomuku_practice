from oop_connect import Connect
import time
from public_ip_request import get_public_ip
from get_local_ip import get_local_ip
from oop_message import Message

class config:
    SERVER = '1'
    CLIENT = '2'
    LOCAL = '1'
    INTERNET = '2'
    LOCAL_HOST = 'localhost'
    LOCAL_PORT = 4567
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 4567
    SEND = '1'
    RECEIVE = '2'


class Player:
    def __init__(self,piece):
        self.name = None
        self.piece = piece
        self.firstplayer = None
        self.currentplayer = None
        self.score = 0

    def set_name(self):
        self.name = input("请输入一个昵称：")

    def get_connect_config():
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
            mode = input("\n请选择连接模式\n1 - 本机连接\n2 - 网络连接\n输入对应编号即可：")
            match mode:
                case config.LOCAL:
                    localmodel = True
                    break
                case config.INTERNET:
                    localmodel = False
                    break
                case _:
                    print("\n输入错误，请重新输入")
        #设置HOST和PORTS
        if localmodel == True:
            #本地连接使用默认参数
            HOST = config.LOCAL_HOST
            PORTS = config.LOCAL_PORT
            return is_server,HOST,PORTS
        else:
            #网络连接时，服务器使用默认参数
            if is_server == True:
                #服务器模式使用0.0.0.0
                HOST = config.SERVER_HOST
                PORTS = config.SERVER_PORT
                #获取并显示本地局域网IP
                print("\n您的本地局域网 IP:", get_local_ip())
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
            #端口号范围为0-65535，且不能为0，不能为负数，不能低于1024
            while True:
                PORTS = input("\n请输入端口号(空输入默认4567)：") or 4567
                # if PORTS == '':
                #     print("\n端口号不能为空，请重新输入")
                #     continue
                PORTS = int(PORTS)
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


    def place_piece(self,board):
        GIVEUP = ('g','g')
        while True:
            try:
                move = input("请输入落子坐标,格式为:x y,[输入'giveup'认输]")
                if move.strip().lower() == 'giveup':
                    return GIVEUP
                else:
                    x,y = map(int,move.strip().split())
                    if board.is_valid_move(x,y):
                        return x,y
                    else:
                        print("该坐标超出棋盘范围或已有棋子，请重试")
            except ValueError:
                print("输入格式有误，请重试")
            except TypeError:
                print("输入格式有误，请重试")
            except (ConnectionResetError, BrokenPipeError):
                print("对方已断开连接")
            except Exception:
                print(f"未知错误，{Exception}")

    def update_score(self):
        self.score += 1

    def ask_continue(self):
        while True:
            game_continue = (input("是否继续游戏？(y/n):")).strip().lower()
            if game_continue == 'y':
                print("您的选择为:继续游戏")
                return True
            elif game_continue == 'n':
                print("您的选择为:结束游戏")
                return False
            else:
                print("输入错误，请重新输入")

    def save_state(self):
        pass

