import socket
import self_g as game
from self_score import pointscounter
import random 
import time
from enum import Enum


splayer = "O"
cplayer = "X"


HOST = '0.0.0.0'
PORTS = 4567

class Status(Enum):
    DRAW = True
    LOSE = True


def recv_move(conn):
    data = conn.recv(1024).decode()
    match data:
        case 'd&d':#平
            return 999,999
        case 'g&g':#对方认输
            return 888,888
        case _:
            x,y = map(int,data.split('&')) #split中的内容是用来去除的，这句的意思是把这个字符串按照&为分隔符，分割成单独的字符
    return x,y

def send_move(conn,x,y):
    conn.sendall(f"{x}&{y}".encode())
    return

def choose_first_player(conn,last_first):

    if last_first == None:
        last_first = random.choice(["server","client"])
    else:
        last_first = "client" if last_first == "server" else "server"


    conn.sendall(f'{last_first}'.encode())    
    
    match last_first:
        case "server":
            print("\n\n本局我方先手")
            while True:
                tempsize = input("请决定棋盘大小(至少为10)")
                try:
                    size = int(tempsize)                
                    if size :
                        conn.sendall(f"{size}".encode())    
                        break
                    else:
                        print("数字过小，请重新输入")
                except:
                    print("您的输入应为数字")                
        case "client":
            print("\n\n本局对方先手")
            print("等候对方决定棋盘大小...")
            size = int(conn.recv(1024).decode())

    return last_first,size


def is_my_turn(conn,newgame,gamepoint):

    while True:

        try:
            move = input("请输入落子坐标,格式为:→x ↓y,[输入'giveup'认输]")
            if move == "giveup":
                gamepoint.increse_point('c')
                print("\n你已认输，本轮落败\n")
                send_move(conn,'g','g')
                return Status.LOSE
            else:
                sx,sy = map(int,move.strip().split()) #strip用于去除收尾的空白字符，split按括号中字符分割字符串
            if newgame.update_board(sx,sy,splayer):
                if newgame.is_leftstep_available():
                    send_move(conn,sx,sy)
                    break
                else:
                    print("\n已无可用步数，此局平局\n")
                    send_move(conn,'d','d')
                    return Status.DRAW
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
            
    newgame.print_board(splayer)

    if newgame.win_check(sx,sy,splayer):
        gamepoint.increse_point('s') 
        print("\nCongratulation！你赢啦\n")
        return True
    
def opponent_turn(conn,newgame,gamepoint):

    print("对手思考中..")
    cx,cy = recv_move(conn)
    match cx:
        case 999:#平局
            print("\n已无可用步数，此局平局\n")
            return True
        case 888:#对方认输
            print("\n对方已投降，本轮获胜\n")
            gamepoint.increse_point('s') 
            return True
        case _:
            newgame.update_board(cx,cy,cplayer)
            newgame.print_board(splayer)
            
    if newgame.win_check(cx,cy,cplayer):
        gamepoint.increse_point('c')
        print("\nSchade！你输啦\n")
        return True
    else:
        return False


def main():

    last_first = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORTS))
        s.listen()

        print("等待连接中...")
        
        conn,addr = s.accept()

        with conn:
            print("连接来自玩家：",addr)
            data = conn.recv(1024)        
            print("来自客户端：",data.decode('utf-8'))
            conn.sendall("已就绪".encode('utf-8'))

            gamepoint = pointscounter()

            while True:
                
                if last_first != None:
                    for i in range(1,11):
                        print(f"{11-i}s后开启新游戏...")
                        time.sleep(1)


                last_first,size = choose_first_player(conn,last_first)
                newgame = game.Gomuku(size)
                newgame.print_board(splayer)

                print(f"\n新游戏已开始,棋盘大小为{size}x{size},目前比分|你:对方={gamepoint.spoints}:{gamepoint.cpoints}")

                while True:
                    if last_first == 'server':
                        if is_my_turn(conn,newgame,gamepoint):
                            break
                        if opponent_turn(conn,newgame,gamepoint):
                            break
                    else:
                        if opponent_turn(conn,newgame,gamepoint):
                            break
                        if is_my_turn(conn,newgame,gamepoint):
                            break



if __name__ == '__main__':
    main()
