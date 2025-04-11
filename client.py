# client.py

import socket
from game import Gomoku

HOST = '127.0.0.1'  # 例如 '127.0.0.1' 或 '192.168.1.10'
PORT = 65432

def recv_move(s):
    data = s.recv(1024).decode()
    x, y = map(int, data.split(','))
    return x, y

def send_move(s, x, y):
    s.sendall(f"{x},{y}".encode())

def main():
    game = Gomoku()
    player_symbol = 'O'
    opponent_symbol = 'X'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("已连接到服务器。")
        game.print_board()

        while True:
            # 等待对手先走
            print("等待对方落子...")
            x, y = recv_move(s)
            game.place_stone(x, y, opponent_symbol)
            game.print_board()

            if game.check_win(x, y, opponent_symbol):
                print("你输了。")
                break

            # 自己走
            while True:
                try:
                    move = input("你的回合（格式 x y）：")
                    x, y = map(int, move.strip().split())
                    if game.place_stone(x, y, player_symbol):
                        send_move(s, x, y)
                        break
                    else:
                        print("无效落子，请重试")
                except:
                    print("输入错误，请输入两个整数坐标")

            game.print_board()
            if game.check_win(x, y, player_symbol):
                print("你赢了！")
                break

if __name__ == '__main__':
    main()
