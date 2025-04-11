import socket
import self_g as game
import time

splayer = "O"
cplayer = "X"

HOST = '192.168.124.7'
PORTS = 4567


def recv_move(s):
    data = s.recv(1024).decode()
    x, y = map(int, data.split('&'))  # split中的内容是用来去除的，这句的意思是把这个字符串按照&为分隔符，分割成单独的字符
    return x, y


def send_move(s, x, y):
    s.sendall(f"{x}&{y}".encode())
    return


def result_first_player(s, first_player):
    first_player = s.recv(1024).decode()

    match first_player:
        case "server":
            print("本局对方先手")
        case "client":
            print("本局我方先手")

    return first_player


def is_my_turn(s, newgame):
    while True:

        try:
            move = input("请输入落子坐标(格式为:x y)")
            cx, cy = map(int, move.strip().split())

            if newgame.update_board(cx, cy, cplayer):
                send_move(s, cx, cy)
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

    newgame.print_board(cplayer)

    if newgame.win_check(cx, cy, cplayer):
        print("Congratulation！你赢啦")
        return True


def opponent_turn(s, newgame):

    print("对手思考中..")
    sx, sy = recv_move(s)
    newgame.update_board(sx, sy, splayer)
    newgame.print_board(cplayer)

    if newgame.win_check(sx, sy, splayer):
        print("Schade！你输啦")
        return True


def main():

    first_player = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORTS))
        s.sendall("已连接".encode('utf=8'))
        data = s.recv(1024)
        print("来自服务端：", data.decode('utf-8'))

        while True:

            if first_player != None:
                for i in range(1, 11):
                    print(f"{11-i}s后开启新游戏...")
                    time.sleep(1)

            newgame = game.Gomuku(10)
            newgame.print_board(cplayer)
            first_player = result_first_player(s, first_player)

            print("新游戏已开始")

            while True:

                """""
                print("对手思考中..")
                sx,sy = recv_move(s)
                newgame.update_board(sx,sy,splayer)
                newgame.print_board()


                if newgame.win_check(sx,sy,splayer):
                    print("Schade！你输啦")
                    break

                while True:

                    try:
                        move = input("请输入落子坐标(格式为:x y)")
                        cx,cy = map(int,move.strip().split())

                        if newgame.update_board(cx,cy,cplayer):
                            send_move(s,cx,cy)
                            break
                        else:
                            print("非法落子坐标，请重新输入(格式为:x y)")
                    except:
                        print("对方已断开连接/落子无效")


                newgame.print_board()

                if newgame.win_check(cx,cy,cplayer):
                    print("Congratulation！你赢啦")
                    break

                """""

                if first_player == 'client':
                    if is_my_turn(s, newgame):
                        break
                    if opponent_turn(s, newgame):
                        break
                else:
                    if opponent_turn(s, newgame):
                        break
                    if is_my_turn(s, newgame):
                        break


if __name__ == '__main__':
    main()
