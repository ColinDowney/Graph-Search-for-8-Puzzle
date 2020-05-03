import PySimpleGUI as sg

if __name__ == '__main__':
    sg.theme('Dark Blue 3')  # please make your creations colorful

    layout = [  [sg.Text('8-Puzzle')],
        [sg.Input(size=(3, 1)), sg.Input(size=(3, 1)), sg.Input(size=(3, 1))],
        [sg.Input(size=(3, 1)), sg.Input(size=(3, 1)), sg.Input(size=(3, 1))],
        [sg.Input(size=(3, 1)), sg.Input(size=(3, 1)), sg.Input(size=(3, 1))],
        [sg.OK(), sg.Cancel(), sg.Button('Random')],
        [sg.Text('Search Algorithm'), sg.Text('Expanded Count'), sg.Text('Generated Count')],
        [sg.Text('BFS'), sg.Text('Count'), sg.Text('Count')],
        ]

    window = sg.Window('8-Puzzle-Demo', layout)

    event, values = window.Read()
    window.close()