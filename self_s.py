import socket
import self_g as game
import random 
import time

splayer = "O"
cplayer = "X"

HOST = '0.0.0.0'
PORTS = 4567



def recv_move(conn):
    data = conn.recv(1024).decode()
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

    match last_first:
        case "server":
            print("本局我方先手")
        case "client":
            print("本局对方先手")

    conn.sendall(f'{last_first}'.encode())

    return last_first


def is_my_turn(conn,newgame):
    while True:

        #服务器先手
        try:
            move = input("请输入落子坐标(格式为:x y)")
            sx,sy = map(int,move.strip().split()) #strip用于去除收尾的空白字符，split按括号中字符分割字符串

            if newgame.update_board(sx,sy,splayer):
                send_move(conn,sx,sy)
                break
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
        print("Congratulation！你赢啦")
        return True
    
def opponent_turn(conn,newgame):

    print("对手思考中..")
    cx,cy = recv_move(conn)
    newgame.update_board(cx,cy,cplayer)
    newgame.print_board(splayer)

    if newgame.win_check(cx,cy,cplayer):
        print("Schade！你输啦")
        return True


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

            while True:
                
                if last_first != None:
                    for i in range(1,11):
                        print(f"{11-i}s后开启新游戏...")
                        time.sleep(1)

                newgame = game.Gomuku(10)
                newgame.print_board(splayer)
                last_first = choose_first_player(conn,last_first)

                print("新游戏已开始")

                while True:
                        
                    """""
                    while True:

                        #服务器先手
                        try:
                            move = input("请输入落子坐标(格式为:x y)")
                            sx,sy = map(int,move.strip().split()) #strip用于去除收尾的空白字符，split按括号中字符分割字符串

                            if newgame.update_board(sx,sy,splayer):
                                send_move(conn,sx,sy)
                                break
                            else:
                                print("非法落子坐标，请重新输入(格式为:x y)")
                        except:
                            print("对方已断开连接/落子无效")
                    

                    newgame.print_board()

                    if newgame.win_check(sx,sy,splayer):
                        print("Congratulation！你赢啦")
                        break
                    """""



                    """""
                    print("对手思考中..")
                    cx,cy = recv_move(conn)
                    newgame.update_board(cx,cy,cplayer)
                    newgame.print_board()

                    if newgame.win_check(cx,cy,cplayer):
                        print("Schade！你输啦")
                        break
                    """""

                    if last_first == 'server':
                        if is_my_turn(conn,newgame):
                            break
                        if opponent_turn(conn,newgame):
                            break
                    else:
                        if opponent_turn(conn,newgame):
                            break
                        if is_my_turn(conn,newgame):
                            break



if __name__ == '__main__':
    main()
