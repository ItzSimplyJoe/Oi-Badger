import re
from dateutil import parser
import PySimpleGUI as sg
class CalendarNLP:
    def get_time(self, sentence):
        words = sentence.lower().split()

        time = None

        for index, word in enumerate(words):
            if re.match(r"\d+(am|pm)", word):
                try:
                    time = parser.parse(word, fuzzy=True).time()
                except ValueError:
                    pass
            elif ":" in word:
                try:
                    time = parser.parse(word).time()
                except ValueError:
                    pass

        time_str = time.strftime("%H:%M") if time else None

        if time_str is None:
            time_str = self.user_input("Enter time: ")
            time = self.get_time(time_str)

        return time_str


    def extract_dates(self, text):
        date_pattern = r"(?<!\d)(?:(?:0?[1-9]|1[0-9]|2[0-9]|3[01])(?:(?:st|nd|rd|th)?(?:\s)?(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:\s*(?:\d{2,4}))?|\s\d{1,2}(?:/\d{1,2}){1,2}(?:/\d{2,4})?))(?!\d)"
        dates = re.findall(date_pattern, text, re.IGNORECASE)
        while len(dates) == 0:
            text = self.user_input("Enter date: ")
            dates = re.findall(date_pattern, text, re.IGNORECASE)
        return str(dates)

    def format_date(self, date_str):
        try:
            date_obj = parser.parse(date_str, fuzzy=True)
            formatted_date = date_obj.strftime("%d-%m-%Y")
            return formatted_date
        except ValueError:
            return "Invalid date format!"
        
    def get_reason(self, text):
        text = text.lower()
        if re.search(r"\d+(am|pm)", text):
            text = re.sub(r"\d+(am|pm)", "", text)
        if re.search(r"(?<!\d)(?:(?:0?[1-9]|1[0-9]|2[0-9]|3[01])(?:(?:st|nd|rd|th)?(?:\s)?(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:\s*(?:\d{2,4}))?|\s\d{1,2}(?:/\d{1,2}){1,2}(?:/\d{2,4})?))(?!\d)", text, re.IGNORECASE):
            text = re.sub(r"(?<!\d)(?:(?:0?[1-9]|1[0-9]|2[0-9]|3[01])(?:(?:st|nd|rd|th)?(?:\s)?(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:\s*(?:\d{2,4}))?|\s\d{1,2}(?:/\d{1,2}){1,2}(?:/\d{2,4})?))(?!\d)", "", text)
        if re.search(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", text, re.IGNORECASE):
            text = re.sub(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", "", text, flags=re.IGNORECASE)
        for word in text.lower().split():
            if word in ["at", "on", "for", "to", "the", "a", "an", "calendar"]:
                text = text.replace(word, "")
        text = " ".join(text.split())
        if text == "":
            self.user_input("Please enter a reason for the event")
        return text

    def user_input(self,text):
        sg.theme('DarkAmber')
        layout = [
            [sg.Text(text)],
            [sg.InputText(key='input'), sg.Button('Ok')]
            ]
        window = sg.Window('Popup', layout, element_justification='c', finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Ok' or event == '\r':
                text = values['input']
                window.close()
                return text

            window.close()
                  
    def extractionprocess(self, sentence):
        date = self.extract_dates(sentence)
        times = self.get_time(sentence)
        reason = self.get_reason(sentence)
        formatted_date = self.format_date(date)
        return formatted_date, times, reason

calendarnlp = CalendarNLP()