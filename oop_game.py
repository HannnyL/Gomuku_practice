from oop_board import Board
from oop_player import Player
from oop_message import Message
from oop_connect import Connect
import random
import time
import sys


class Status:
    WIN = 1
    LOSS = 2
    DRAW = 3

class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.connect = None
        self.board = None
        self.times = 1

    #初始化游戏-首次运行
    def initialize_game(self):
        self.connect = Connect(*Player.get_connect_config())
        #根据主副机确定棋子符号
        if self.connect.is_server == True:
            self.player1 = Player('X')
            self.player2 = Player('O')
        else:
            self.player1 = Player('O')
            self.player2 = Player('X')
        #获取玩家昵称
        self.get_player_name()
        #非首次运行重置内容
        self.reset_game()

    #重置游戏-非首次运行
    def reset_game(self):
        #决定先后手
        self.choose_first_player()
        #先手玩家决定棋盘大小
        self.board = Board(self.get_board_size())
        #打印棋盘及双方信息
        self.print_game_info()
    
    #处理玩家昵称
    def get_player_name(self):
        if self.connect.is_server == True:
            #主机 先定昵称并发送
            self.handle_my_name()
            #主机 再等待接收对方昵称
            self.handle_other_name()
        else:
            #副机 先接收对方昵称
            self.handle_other_name()
            #副机 再定自己昵称并发送 
            self.handle_my_name()
    def handle_my_name(self):
        self.player1.set_name()
        self.connect.send_message(Message.chat(self.player1.name))
        time.sleep(1)
    def handle_other_name(self):
        print("等待对方响应中...")
        msg_type,payload = self.connect.recv_message()
        if msg_type == 'chat':
            self.player2.name = payload

    #决定先后手
    def choose_first_player(self):
        #第一局随机决定先后手
        if self.player1.firstplayer == None:
            if self.connect.is_server == True:
                #主机来计算先后手
                self.player1.firstplayer = self.player1.currentplayer = random.choice([True,False])
                self.player2.firstplayer = self.player2.currentplayer = not self.player1.firstplayer
                #发送对方先后手结果
                self.connect.send_message(Message.flag(self.player2.firstplayer))
            else:
                #接收主机发来的先后手结果
                msg_type,payload = self.connect.recv_message()
                if msg_type == 'flag':
                    self.player1.firstplayer = self.player1.currentplayer = payload
                    self.player2.firstplayer = self.player2.currentplayer = not self.player1.firstplayer
        #如果不是第一局，则交换先后手
        else:
            self.player1.firstplayer = self.player1.currentplayer = not self.player1.firstplayer
            self.player2.firstplayer = self.player2.currentplayer = not self.player2.firstplayer
        print(f"\n【本局我方{'先手' if self.player1.firstplayer == True else '后手'}】\n")

    #主机定棋盘大小 副机接收
    def get_board_size(self):
        if self.player1.firstplayer == True:
            #主机决定棋盘大小
            while True:
                try:
                    size = input("请决定棋盘大小(5-30)：")
                    size = int(size)
                    if size < 2 or size > 30:
                        print("尺寸超限，应为2-30，请重新输入")
                        continue
                    else:
                        self.connect.send_message(Message.flag(size))
                        return size
                except ValueError:
                    print("棋盘尺寸应为整数，请重新输入")
                    continue
        else:
            #接收主机发来的棋盘大小
            print("等待对方决定棋盘大小...")
            msg_type,payload = self.connect.recv_message()
            if msg_type == 'flag':
                return payload

    #打印棋盘及双方信息
    def print_game_info(self):
        #游戏伊始打印局数
        if self.board.size ** 2 == self.board.leftstep:
            print(f"\n---------------第{self.times}局---------------")
        self.board.print_board()
        print(f"\n我方({self.player1.piece}):{self.player1.name}  |  比分 {self.player1.score}:{self.player2.score}\n对方({self.player2.piece}):{self.player2.name}\n")

    #处理但回合
    def next_turn(self):
        #当回合玩家操作
        if self.player1.currentplayer:
            x,y = self.player1.place_piece(self.board)
            #发送坐标
            self.connect.send_message(Message.move(x,y))
            #判断玩家是否投降
            if self.check_giveup(x,y):
                return Status.LOSS
            #未投降则继续游戏
            else:
                return self.handle_game_data(x,y)
        #待机玩家等候对方操作
        else:
            #接收对方坐标
            print("对方思考中...")
            msg_type,payload = self.connect.recv_message()
            if msg_type == 'move':
                x,y = payload['x'],payload['y']
                #判断玩家是否投降
                if self.check_giveup(x,y):
                    return Status.WIN
                #未投降则继续游戏
                else:
                    return self.handle_game_data(x,y)
                
    #处理游戏数据                
    def handle_game_data(self,x,y):
        #判断己方是否为当前玩家
        current_player = self.player1 if self.player1.currentplayer else self.player2
        piece = current_player.piece
        #更新并打印棋盘
        self.board.update_board(x,y,piece)
        self.print_game_info()
        #更新当前玩家
        self.player1.currentplayer = not self.player1.currentplayer
        self.player2.currentplayer = not self.player2.currentplayer
        #判断胜负
        if self.board.win_check(x,y,piece):
            return Status.WIN if current_player == self.player1 else Status.LOSS
        elif self.board.leftstep == 0:
            return Status.DRAW
        else:
            return False

    #投降检测
    def check_giveup(self,x,y):
        if x == 'g' and y == 'g':
            print("\n我方已投降" if self.player1.currentplayer else "\n对方已投降")
            return True
        return False

    #询问是否继续游戏
    def ask_continue(self):
        #询问玩家是否继续游戏
        game_continue = self.player1.ask_continue()
        #双方互发用户结果
        if self.connect.is_server:
            self.connect.send_message(Message.flag(game_continue))
            time.sleep(1)
            print("\n等待对方选择...")
            msg_type,payload = self.connect.recv_message()
        else:
            print("\n等待对方选择...")
            msg_type,payload = self.connect.recv_message()
            time.sleep(1)
            self.connect.send_message(Message.flag(game_continue))
        #判断是否继续游戏
        if msg_type == 'flag':
                if payload and game_continue:
                    print("\n双方均选择继续游戏")
                    #继续游戏
                    return True
                else:
                    if payload and not game_continue:
                        print("\n我方选择结束游戏")
                    elif not payload and game_continue:
                        print("\n对方选择结束游戏")
                    else:
                        print("\n双方均选择结束游戏")
                    #游戏结束
                    return False
                
    #循环执行next_turn并判断胜负结果
    def handle_game_process(self):
        while True:
            result = self.next_turn()
            if result== Status.WIN:
                print("\nCongratulation！我方获胜\n")
                self.player1.update_score()
                break
            elif result == Status.LOSS:
                print("\nSchade！我方落败\n")
                self.player2.update_score()
                break
            elif result == Status.DRAW:
                print("\n已无可用步数，此局平局\n")
                break
        if self.ask_continue() == False:
            print("\n【游戏结束】")
            self.connect.close_socket()
            sys.exit(0)
        else:
            print("\n【继续游戏】")

    
    #执行方法
    def run(self):
        #初始化游戏
        if self.times == 1:
            self.initialize_game()
        else:
            self.reset_game()
        #游戏开始
        self.handle_game_process()
        #游戏结束
        self.times += 1


if __name__ == "__main__":
    game = Game()
    while True:
        game.run()
