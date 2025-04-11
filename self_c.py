import socket
import self_g as game

splayer = "O"
cplayer = "X"

HOST = '127.0.0.1'
PORTS = 4567



def recv_move(s):
    data = s.recv(1024).decode()
    x,y = map(int,data.split('&')) #split中的内容是用来去除的，这句的意思是把这个字符串按照&为分隔符，分割成单独的字符
    return x,y

def send_move(s,x,y):
    s.sendall(f"{x}&{y}".encode())
    return

def main():
        
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST,PORTS))
        s.sendall("已连接".encode('utf=8'))
        data = s.recv(1024)
        print("来自服务端：",data.decode('utf-8'))   
        

        while True:

            newgame = game.Gomuku(10)
            newgame.print_board()

            print("新游戏已开始")

            while True:

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


if __name__ == '__main__':
    main()