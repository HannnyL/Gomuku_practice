# server.py

import socket
from game import Gomoku

HOST = '0.0.0.0'
PORT = 65432

def recv_move(conn):
    data = conn.recv(1024).decode()
    x, y = map(int, data.split(','))
    return x, y

def send_move(conn, x, y):
    conn.sendall(f"{x},{y}".encode())

def main():
    game = Gomoku()
    player_symbol = 'X'
    opponent_symbol = 'O'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"等待客户端连接，端口 {PORT}...")
        conn, addr = s.accept()
        with conn:
            print(f"已连接：{addr}")
            game.print_board()

            while True:
                # 自己走
                while True:
                    try:
                        move = input("你的回合（格式 x y）：")
                        x, y = map(int, move.strip().split())
                        if game.place_stone(x, y, player_symbol):
                            send_move(conn, x, y)
                            break
                        else:
                            print("无效落子，请重试")
                    except:
                        print("输入错误，请输入两个整数坐标")

                game.print_board()
                if game.check_win(x, y, player_symbol):
                    print("你赢了！")
                    break

                # 等待对手走
                print("等待对方落子...")
                x, y = recv_move(conn)
                game.place_stone(x, y, opponent_symbol)
                game.print_board()

                if game.check_win(x, y, opponent_symbol):
                    print("你输了。")
                    break

if __name__ == '__main__':
    main()
