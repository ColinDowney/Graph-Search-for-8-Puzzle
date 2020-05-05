import PySimpleGUI as sg
import numpy as np
import algorithm as ag

def bfs_search(digits):
    g = ag.BFSSearch(digits)
    result = g.search()  # expand, generate, final
    if not result:
        window.FindElement('b_ec').Update("没找到")
        window.FindElement('b_gc').Update("没找到")
    else:
        window.FindElement('b_ec').Update(result[0].__str__())
        window.FindElement('b_gc').Update(result[1].__str__())

def dfs_search(digits):
    g = ag.DFSSearch(digits)
    result = g.search()  # expand, generate, final
    if not result:
        window.FindElement('d_ec').Update("没找到")
        window.FindElement('d_gc').Update("没找到")
    else:
        window.FindElement('d_ec').Update(result[0].__str__())
        window.FindElement('d_gc').Update(result[1].__str__())

def astar_w_search(digits):
    g = ag.AStarSearchW(digits)
    result = g.search()  # expand, generate, final
    if not result:
        window.FindElement('w_ec').Update("没找到")
        window.FindElement('w_gc').Update("没找到")
    else:
        window.FindElement('w_ec').Update(result[0].__str__())
        window.FindElement('w_gc').Update(result[1].__str__())

def astar_p_search(digits):
    g = ag.AStarSearchP(digits)
    result = g.search()  # expand, generate, final
    if not result:
        window.FindElement('p_ec').Update("没找到")
        window.FindElement('p_gc').Update("没找到")
    else:
        window.FindElement('p_ec').Update(result[0].__str__())
        window.FindElement('p_gc').Update(result[1].__str__())

def astar_s_search(digits):
    g = ag.AStarSearchS(digits)
    result = g.search()  # expand, generate, final
    if not result:
        window.FindElement('s_ec').Update("没找到")
        window.FindElement('s_gc').Update("没找到")
    else:
        window.FindElement('s_ec').Update(result[0].__str__())
        window.FindElement('s_gc').Update(result[1].__str__())

if __name__ == '__main__':

    sg.theme('Dark Blue 3')  # please make your creations colorful

    layout = [
        [sg.Text('8-Puzzle'), sg.Text('', key='tips', size=(20, 1))],
        [sg.Input(size=(10, 1), key='index0'), sg.Input(size=(10, 1), key='index1'),
         sg.Input(size=(10, 1), key='index2'), sg.Button(button_text='Random', size=(15, 1))],
        [sg.Input(size=(10, 1), key='index3'), sg.Input(size=(10, 1), key='index4'),
         sg.Input(size=(10, 1), key='index5'), sg.Button(button_text='Clear', size=(15, 1))],
        [sg.Input(size=(10, 1), key='index6'), sg.Input(size=(10, 1), key='index7'),
         sg.Input(size=(10, 1), key='index8'), sg.Button(button_text='Exit', size=(15, 1))],
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

    window = sg.Window('8-Puzzle-Demo', layout)

    digits = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8}
    while True:
        event, values = window.Read()
        input_values = []

        if event == 'Random':
            digits_temp = ag.random_digits_array().flatten()
            index = 0
            for i in digits_temp:
                window.FindElement("index" + str(index)).Update(str(i))
                index += 1
            window.FindElement('tips').Update("八数码矩阵随机生成成功")

        elif event == 'Clear':
            index = 0
            for i in range(9):
                window.FindElement("index" + str(index)).Update("")
                index += 1
            window.FindElement('tips').Update("")
            key_temp = ['b', 'd', 'w', 'p', 's']
            for i in range(len(x)):
                window.FindElement(key_temp[i] + '_ec').Update("")
                window.FindElement(key_temp[i] + '_gc').Update("")

        elif event == 'Exit':
            window.close()

        else:
            for i in values:
                if values[i] in digits.keys():
                    input_values.append(digits[values[i]])
                else:
                    input_values.append(0)

            if set(input_values) != set(range(9)):
                window.FindElement('tips').Update("数据不正确，请检查数据")
                continue

            d = np.array(input_values, dtype=int).reshape(3, 3)

            # 这提示显示不出来
            # window.FindElement('tips').Update("正在运行中，请稍后")

            if event == 'BFS':
                bfs_search(d)

            elif event == 'DFS':
                dfs_search(d)

            elif event == 'W(n)':
                astar_w_search(d)

            elif event == 'P(n)':
                astar_p_search(d)

            elif event == 'P(n)+3S(n)':
                astar_s_search(d)

            window.FindElement('tips').Update("")