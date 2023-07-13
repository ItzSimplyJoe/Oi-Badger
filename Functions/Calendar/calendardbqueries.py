from Functions.Calendar.calendarnlp import calendarnlp
from Functions.Calendar.calendar import CalendarApp
from ML.detemine_most_similar import determine_most_similar_phrase
import sqlite3
class CalendarQueries:
    def main(self, sentence):
        samples = {
            'calendar 15th november 3pm meeting with bob' : {'func' : self.add_to_calendar},
            'open my calendar' : {'func' : self.open_calendar},
            'show me my calendar' : {'func' : self.open_calendar},
        }
        
        most_similar = determine_most_similar_phrase(sentence, samples)
        func = samples[most_similar]['func']
        func(sentence)

    def open_calendar(self,sentence):
        app = CalendarApp()
        app.run()

    def add_to_calendar(self,sentence):
        date,time,reason = calendarnlp.extractionprocess(sentence)
        conn = sqlite3.connect("Functions/Calendar/calendar.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                reason TEXT,
                colour TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO events (date, time, reason, colour)
            VALUES (?, ?, ?, ?)
        """, (date, time, reason, "cyan"))
        conn.commit()
        conn.close()

calendarqueries = CalendarQueries()

