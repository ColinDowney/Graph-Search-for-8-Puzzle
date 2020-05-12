import PySimpleGUI as sg
import numpy as np
import algorithm as ag
import threading
import sys


def bfs_search(digits):
    win1.FindElement('tips').Update("正在bfs搜索，请稍后")
    g = ag.BFSSearch(digits)
    result = g.search()  # expand, generate, final
    if not result:
        win1.FindElement('b_ec').Update("没找到")
        win1.FindElement('b_gc').Update("没找到")
    else:
        win1.FindElement('b_ec').Update(result[0].__str__())
        win1.FindElement('b_gc').Update(result[1].__str__())
    win1.FindElement('tips').Update("bfs搜索完成")


def dfs_search(digits):
    win1.FindElement('tips').Update("正在dfs搜索，请稍后")
    g = ag.DFSSearch(digits)
    result = g.search()  # expand, generate, final
    if not result:
        win1.FindElement('d_ec').Update("没找到")
        win1.FindElement('d_gc').Update("没找到")
    else:
        win1.FindElement('d_ec').Update(result[0].__str__())
        win1.FindElement('d_gc').Update(result[1].__str__())
    win1.FindElement('tips').Update("dfs搜索完成")


def astar_w_search(digits):
    win1.FindElement('tips').Update("正在f(n)=g(n)+w(n)搜索，请稍后")
    g = ag.AStarSearchW(digits)
    result = g.search()  # expand, generate, final
    if not result:
        win1.FindElement('w_ec').Update("没找到")
        win1.FindElement('w_gc').Update("没找到")
    else:
        win1.FindElement('w_ec').Update(result[0].__str__())
        win1.FindElement('w_gc').Update(result[1].__str__())
    win1.FindElement('tips').Update("f(n)=g(n)+w(n)搜索完成")


def astar_p_search(digits):
    win1.FindElement('tips').Update("正在f(n)=g(n)+p(n)搜索，请稍后")
    g = ag.AStarSearchP(digits)
    result = g.search()  # expand, generate, final
    if not result:
        win1.FindElement('p_ec').Update("没找到")
        win1.FindElement('p_gc').Update("没找到")
    else:
        win1.FindElement('p_ec').Update(result[0].__str__())
        win1.FindElement('p_gc').Update(result[1].__str__())
    win1.FindElement('tips').Update("f(n)=g(n)+p(n)搜索完成")


def astar_s_search(digits):
    win1.FindElement('tips').Update("正在f(n)=g(n)+p(n)+3s(n)搜索，请稍后")
    g = ag.AStarSearchS(digits)
    result = g.search()  # expand, generate, final
    if not result:
        win1.FindElement('s_ec').Update("没找到")
        win1.FindElement('s_gc').Update("没找到")
    else:
        win1.FindElement('s_ec').Update(result[0].__str__())
        win1.FindElement('s_gc').Update(result[1].__str__())
    win1.FindElement('tips').Update("f(n)=g(n)+p(n)+3s(n)搜索完成")
# Design pattern 2 - First window remains active

class GraphSearchThread (threading.Thread):   #继承父类threading.Thread

    def __init__(self, threadID, name, digits):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.digits = digits

    def run(self):
        # p(n) + 3s(n)
        astar_s_search(self.digits)

        # p(n)
        astar_p_search(self.digits)

        # w(n)
        astar_w_search(self.digits)

        # bfs
        bfs_search(self.digits)

        # dfs
        dfs_search(self.digits)

        win1.FindElement('tips').Update("搜索完成!")

class BFSSearchThread (threading.Thread):   #继承父类threading.Thread

    def __init__(self, threadID, name, digits):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.digits = digits

    def run(self):
        # bfs
        bfs_search(self.digits)


class DFSSearchThread (threading.Thread):   #继承父类threading.Thread

    def __init__(self, threadID, name, digits):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.digits = digits

    def run(self):
        # dfs
        dfs_search(self.digits)


class AStarSearchWThread (threading.Thread):   #继承父类threading.Thread

    def __init__(self, threadID, name, digits):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.digits = digits

    def run(self):
        # w(n)
        astar_w_search(self.digits)


class AStarSearchPThread (threading.Thread):   #继承父类threading.Thread

    def __init__(self, threadID, name, digits):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.digits = digits

    def run(self):
        # p(n)
        astar_p_search(self.digits)


class AStarSearchSThread (threading.Thread):   #继承父类threading.Thread

    def __init__(self, threadID, name, digits):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.digits = digits

    def run(self):
        # p(n)+3s(n)
        astar_s_search(self.digits)


if __name__ == '__main__':
    # sg.theme('Dark Blue 3')  # please make your creations colorful
    sg.theme('GreenTan')  # please make your creations colorful  Material1
    sg.SetOptions(text_justification='center')

    layout = [
        [sg.Text('8-Puzzle', size=(10, 1)), sg.Text('', key='tips', size=(35, 1))],
        [sg.Button(button_text='问题', size=(10, 1)), sg.Input(size=(10, 1), key='index0'),
         sg.Input(size=(10, 1), key='index1'),
         sg.Input(size=(10, 1), key='index2'), sg.Button(button_text='Random', size=(10, 1))],
        [sg.Button(button_text='内容', size=(10, 1)), sg.Input(size=(10, 1), key='index3'),
         sg.Input(size=(10, 1), key='index4'),
         sg.Input(size=(10, 1), key='index5'), sg.Button(button_text='Clear', size=(10, 1))],
        [sg.Button(button_text='AllStart', size=(10, 1)), sg.Input(size=(10, 1), key='index6'),
         sg.Input(size=(10, 1), key='index7'),
         sg.Input(size=(10, 1), key='index8'), sg.Button(button_text='Exit', size=(10, 1))],
        [sg.Text('Search Algorithm', size=(15, 1)), sg.Text('Expanded Count', size=(15, 1)),
         sg.Text('Generated Count')],
        [sg.Button(button_text='BFS', size=(15, 1)), sg.Text('', size=(15, 1), key='b_ec'),
         sg.Text('', size=(15, 1), key='b_gc')],
        [sg.Button(button_text='DFS', size=(15, 1)), sg.Text('', size=(15, 1), key='d_ec'),
         sg.Text('', size=(15, 1), key='d_gc')],
        [sg.Button(button_text='W(n)', size=(15, 1)), sg.Text('', size=(15, 1), key='w_ec'),
         sg.Text('', size=(15, 1), key='w_gc')],
        [sg.Button(button_text='P(n)', size=(15, 1)), sg.Text('', size=(15, 1), key='p_ec'),
         sg.Text('', size=(15, 1), key='p_gc')],
        [sg.Button(button_text='P(n)+3S(n)', size=(15, 1)), sg.Text('', size=(15, 1), key='s_ec'),
         sg.Text('', size=(15, 1), key='s_gc')]
    ]

    win1 = sg.Window('8-Puzzle-Demo', layout)
    # 字体
    # window = sg.Window('8-Puzzle-Demo', layout, font='微软雅黑',finalize=True)
    digits = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8}
    while True:
        win2_active = False
        win3_active = False
        event, values = win1.Read()
        input_values = []

        if event == 'Random':
            digits_temp = ag.random_digits_array().flatten()
            index = 0
            for i in digits_temp:
                win1.FindElement("index" + str(index)).Update(str(i))
                index += 1
            win1.FindElement('tips').Update("八数码矩阵随机生成成功")

        elif event == 'Clear':
            index = 0
            for i in range(9):
                win1.FindElement("index" + str(index)).Update("")
                index += 1
            win1.FindElement('tips').Update("")
            key_temp = ['b', 'd', 'w', 'p', 's']
            for i in range(len(key_temp)):
                win1.FindElement(key_temp[i] + '_ec').Update("")
                win1.FindElement(key_temp[i] + '_gc').Update("")

        elif event == 'Exit':
            # TODO:停止后台线程
            win1.close()
            sys.exit()
            quit()
            break

        elif not win2_active and event == '问题':
            win2_active = True
            layout2 = [
                [sg.Text('问题重述 3×3九宫棋盘，放置数码为')],
                [sg.Text('1 -8的8个棋牌，剩下一个空格，只能通过')],
                [sg.Text('棋牌向空格的移动来改变棋盘的布局')],
                [sg.Text('初始状态,如下，0代表空格')],
                [sg.Text('1', size=(5, 1)), sg.Text('2', size=(5, 1)), sg.Text('3', size=(5, 1))],
                [sg.Text('4', size=(5, 1)), sg.Text('0', size=(5, 1)), sg.Text('5', size=(5, 1))],
                [sg.Text('6', size=(5, 1)), sg.Text('7', size=(5, 1)), sg.Text('8', size=(5, 1))],
                [sg.Text('↓', size=(5, 1))],
                [sg.Text('目标状态，唯一的')],
                [sg.Text('1', size=(5, 1)), sg.Text('2', size=(5, 1)), sg.Text('3', size=(5, 1))],
                [sg.Text('8', size=(5, 1)), sg.Text('0', size=(5, 1)), sg.Text('4', size=(5, 1))],
                [sg.Text('7', size=(5, 1)), sg.Text('6', size=(5, 1)), sg.Text('5', size=(5, 1))],
                [sg.Text('要求：根据给定初始布局（即初始状态）和目标布')],
                [sg.Text('局（即目标状态）,如何移动棋牌才能从初始')],
                [sg.Text('布局到达目标布局,找到合法的走步序列')]
            ]
            win2 = sg.Window('八数码问题', layout2)
            if win2_active:
                ev2, vals2 = win2.read(timeout=100)
                if ev2 is None or ev2 == 'Exit':
                    win2_active = False
                    win2.close()

        elif not win3_active and event == '内容':
            win3_active = True
            layout3 = [
                [sg.Text('针对八数码问题，在Windows环境下用')],
                [sg.Text('Python3.x语言实现几种搜索算法(最好是图形界面)：')],
                [sg.Text('深度优先搜索 ')],
                [sg.Text('宽度优先搜索')],
                [sg.Text('启发式搜索算法（h1(n) =W(n) “不在位”的将牌数）')],
                [sg.Text('启发式搜索算法（h2(n) = P(n)将牌“不在位”的距离和）')],
                [sg.Text('启发式搜索算法（h3(n) = h(n)＝P(n)+3S(n)）')],
                [sg.Text('随机产生或手动输入初始状态，对于同一个')],
                [sg.Text('初始状态，分别用上面的5种方法进行求解，并对比结果')]
            ]
            win3 = sg.Window('实验内容和要求', layout3)
            if win3_active:
                ev3, vals3 = win3.read(timeout=100)
                if ev3 is None or ev3 == 'Exit':
                    win3_active = False
                    win3.close()

        else:
            if values is None:
                break
            for i in values:
                if values[i] in digits.keys():
                    input_values.append(digits[values[i]])
                else:
                    input_values.append(0)

            if set(input_values) != set(range(9)):
                win1.FindElement('tips').Update("数据不正确，请检查数据")
                continue

            d = np.array(input_values, dtype=int).reshape(3, 3)

            if event == 'AllStart':
                # 开启线程放后台跑
                all_thread = GraphSearchThread(1, "All-Thread", d)
                all_thread.start()
            elif event == 'BFS':
                # 开启线程放后台跑
                bfs_thread = BFSSearchThread(2, "BFS-Thread", d)
                bfs_thread.start()
            elif event == 'DFS':
                # 开启线程放后台跑
                dfs_thread = DFSSearchThread(3, "DFS-Thread", d)
                dfs_thread.start()
            elif event == 'W(n)':
                # 开启线程放后台跑
                w_thread = AStarSearchWThread(4, "W-Thread", d)
                w_thread.start()
            elif event == 'P(n)':
                # 开启线程放后台跑
                p_thread = AStarSearchPThread(5, "P-Thread", d)
                p_thread.start()
            elif event == 'P(n)+3S(n)':
                # 开启线程放后台跑
                s_thread = AStarSearchSThread(6, "S-Thread", d)
                s_thread.start()