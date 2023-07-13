import sqlite3
import datetime

'''
Add to database check time and date
when loadup check if time and date is greater than database time and date
if it is then send a reminder
'''

class reminder():
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS reminder (date text, time text, reminder text)")
        self.conn.commit()

    def addReminder(self, date, time, reminder):
        self.c.execute("INSERT INTO reminder VALUES (?, ?, ?)", (date, time, reminder))
        self.conn.commit()

    def getReminder(self):
        self.c.execute("SELECT * FROM reminder")
        return self.c.fetchall()

    def deleteReminder(self, date, time, reminder):
        self.c.execute("DELETE FROM reminder WHERE date=? AND time=? AND reminder=?", (date, time, reminder))
        self.conn.commit()

    def checkReminder(self):
        self.c.execute("SELECT * FROM reminder")
        data = self.c.fetchall()
        for row in data:
            date = row[0]
            time = row[1]
            reminder = row[2]
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            time = datetime.datetime.strptime(time, '%H:%M')
            if date.date() == datetime.datetime.now().date():
                if time.time() == datetime.datetime.now().time():
                    return reminder
        return None
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    r = reminder()
    r.addReminder("2020-05-10", "12:00", "Test")
    print(r.checkReminder())
    r.close()