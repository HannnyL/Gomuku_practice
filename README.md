个人用于练习socket所写的小程序

包括：

1.面向过程思路的实现代码：以self_x,py命名的文件

2.Chatgpt老师的参考代码：game/server/client.py

3.面向对象思路的实现代码：以oop_xxx.py命名的文件

运行方式：

1.self_x.py类文件，主机运行self_s.py，副机修改self_c.py中的'HOST'变量为主机局域网地址后，运行该文件

2.oop_xxx.py类文件，主副机都运行oop_game.py文件，根据提示输入相应参数来设置主/副机和host,ports


已实现功能：
先后手
先手决定棋盘大小
棋盘下满后平局
玩家昵称
投降
玩家自选是否开启新游戏
断线重连(未完全)

待实现：
对局中互发消息



