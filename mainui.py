import PySimpleGUI as sg
import random
import threading
from AccountSystem.GUIS import gui
from Speech.voiceoutput import voiceoutput
from Speech.voiceinput import voiceinput
from main import assistant

class MainUI:
    def __init__(self):
        sg.theme('DarkAmber')
        self.column1 = [
            [sg.Text('OiBadger', font=('Helvetica', 25))],
            [sg.Text(random.choice(["Check you calendar", "Set a Timer", "Add something to your shopping list", "Ask for a joke", "Ask for the weather", "Ask for the time", "Ask for a fact", "Ask for a quote", "Ask for a math problem", "Ask for a riddle", "Ask for a song", "Ask for a poem", "Ask for a story", "Ask for a tongue twister", "Ask for a news headline", "Ask for a news article"]))],
            [sg.Text(random.choice(["Check you calendar", "Set a Timer", "Add something to your shopping list", "Ask for a joke", "Ask for the weather", "Ask for the time", "Ask for a fact", "Ask for a quote", "Ask for a math problem", "Ask for a riddle", "Ask for a song", "Ask for a poem", "Ask for a story", "Ask for a tongue twister", "Ask for a news headline", "Ask for a news article"]))],
            [sg.Text(random.choice(["Check you calendar", "Set a Timer", "Add something to your shopping list", "Ask for a joke", "Ask for the weather", "Ask for the time", "Ask for a fact", "Ask for a quote", "Ask for a math problem", "Ask for a riddle", "Ask for a song", "Ask for a poem", "Ask for a story", "Ask for a tongue twister", "Ask for a news headline", "Ask for a news article"]))],
        ]
        self.column2 = [
            [sg.Output(size=(60, 10))],
            [sg.Text('Enter something'), sg.InputText(key='input')],
            [sg.Button('OK')]
        ]
        self.layout = [
            [sg.Column(self.column1), sg.VSeperator(), sg.Column(self.column2)]
        ]
        self.window = sg.Window('MainUI', self.layout, finalize=True, return_keyboard_events=True)

    def run(self, email):
        while True:
            event, values = self.window.read()
            if event == 'OK' or event == '\r':
                output = threading.Thread(target=self.answer, args=(values['input'],)).start()
                print("You:")
                print(values['input'])
                print("Badger: ")
                if output is not None:
                    print(output)
                    threading.Thread(target=voiceoutput.speak, args=(output,)).start()
                else:
                    print("Okay")
            if event == sg.WIN_CLOSED:
                break
        self.window.close()
    def input(self,email):
        voiceinput.initialize_voice()
        text = threading.Thread(target=voiceinput.process_voice_input, args=(email,)).start()
        print("You:")
        print(text)
        output = threading.Thread(target=self.answer, args=(text,)).start()
        print("Badger: ")
        if output is not None:
            print(output)
            threading.Thread(target=voiceoutput.speak, args=(output,)).start()
        else:
            print("Okay")

    def answer(self,test):
        text = assistant.reply(test)
        return text
    
    def start(self):
        email = gui.remembermecheck()
        while True:
            if email is None:
                email = gui.remembermecheck()
            else:
                break                
        self.run(email)



if __name__ == '__main__':
    mainui = MainUI()
    mainui.start()