import socket
import self_g as game
from self_score import pointscounter
import time
from enum import Enum

splayer = "O"
cplayer = "X"


HOST = '127.0.0.1'
PORTS = 4567

class Status(Enum):
    DRAW = True
    LOSE = True



def recv_move(s):
    data = s.recv(1024).decode()
    match data:
        case 'd&d':#平
            return 999,999
        case 'g&g':#对方认输
            return 888,888
        case _:
            x,y = map(int,data.split('&')) #split中的内容是用来去除的，这句的意思是把这个字符串按照&为分隔符，分割成单独的字符
    return x,y


def send_move(s, x, y):
    s.sendall(f"{x}&{y}".encode())
    return


def result_first_player(s, first_player):
    first_player = s.recv(1024).decode()

    match first_player:
        case "server":
            print("\n\n本局对方先手")
            print("等候对方决定棋盘大小...")
            size = int(s.recv(1024).decode())
        case "client":
            print("\n\n本局我方先手")
            while True:
                tempsize = input("请决定棋盘大小(至少为10)")
                try:
                    size = int(tempsize)
                    if size :
                        s.sendall(f"{size}".encode())                    
                        break
                    else:
                        print("数字过小，请重新输入")
                except:
                    print("您的输入应为数字")


    
    return first_player,size


def is_my_turn(s,newgame,gamepoint):
    while True:

        try:
            move = input("请输入落子坐标,格式为:x y,[输入'giveup'认输]")
            if move == "giveup":
                gamepoint.increse_point('s')                
                print("\n你已认输，本轮落败\n")
                send_move(s,'g','g')
                return Status.LOSE
            else:
                cx,cy = map(int,move.strip().split())
            if newgame.update_board(cx,cy,cplayer):
                if newgame.is_leftstep_available():    
                    send_move(s,cx,cy)
                    break
                else:
                    print("\n已无可用步数，此局平局\n")
                    send_move(s,'d','d')
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

    newgame.print_board(cplayer)
    
    if newgame.win_check(cx,cy,cplayer):
        gamepoint.increse_point('c')
        print("\nCongratulation！你赢啦\n")
        return True
    
def opponent_turn(s,newgame,gamepoint):

    print("对手思考中..")
    sx,sy = recv_move(s)
    match sx:
        case 999:#平局
            print("\n已无可用步数，此局平局\n")
            return True
        case 888:#对方认输
            print("\n对方已投降，本轮获胜\n")
            gamepoint.increse_point('c')
            return True
        case _:
            newgame.update_board(sx,sy,splayer)
            newgame.print_board(cplayer)

    
    if newgame.win_check(sx,sy,splayer):
        gamepoint.increse_point('s')      
        print("\nSchade！你输啦\n")
        return True
    else:
        return False


def main():

    first_player = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORTS))
        s.sendall("已连接".encode('utf=8'))
        data = s.recv(1024)
        print("来自服务端：",data.decode('utf-8'))   
        
        gamepoint = pointscounter()
        
        while True:

            if first_player != None:
                for i in range(1, 11):
                    print(f"{11-i}s后开启新游戏...")
                    time.sleep(1)

            first_player,size = result_first_player(s,first_player)
            newgame = game.Gomuku(size)
            newgame.print_board(cplayer)

            print(f"\n新游戏已开始,棋盘大小:【{size}x{size}】,目前比分|你:对方 = {gamepoint.cpoints}:{gamepoint.spoints}\n")

            while True:
                if first_player == 'client':
                    if is_my_turn(s,newgame,gamepoint):
                        break
                    if opponent_turn(s,newgame,gamepoint):
                        break
                else:
                    if opponent_turn(s,newgame,gamepoint):
                        break
                    if is_my_turn(s,newgame,gamepoint):
                        break


if __name__ == '__main__':
    main()
