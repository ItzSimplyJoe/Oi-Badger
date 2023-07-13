import sqlite3
import hashlib

class Signup:
    def __init__(self):
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS user (
            userid INTEGER PRIMARY KEY AUTOINCREMENT, 
            email TEXT, 
            username TEXT,
            password TEXT,
            pin TEXT)''')
        self.conn.commit()
        self.conn.close()

    def add_user(self, email, username, password, pin):
        password = hashlib.sha256(password.encode()).hexdigest()
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('INSERT INTO user (email, username, password, pin) VALUES (?, ?, ?, ?)', (email, username, password, pin))
        self.conn.commit()
        self.conn.close()
    
    def check_username(self,username):
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user WHERE username = ?', (username,))
        user = self.c.fetchone()
        self.conn.close()
        if user is None:
            return False
        else:
            return True
    
    def check_email(self,email):
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user WHERE email = ?', (email,))
        user = self.c.fetchone()
        self.conn.close()
        if user is None:
            return False
        else:
            return True
    
    def check_pin(self,email):
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT pin FROM user WHERE email = ?', (email,))
        pin = self.c.fetchone()
        self.conn.close()
        if pin[0] is None:
            return False
        else:
            return True
    
    def change_username(self, email, username):
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('UPDATE user SET username = ? WHERE email = ?', (username, email))
        self.conn.commit()
        self.conn.close()

    def change_password(self, email, password):
        password = hashlib.sha256(password.encode()).hexdigest()
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('UPDATE user SET password = ? WHERE email = ?', (password, email))
        self.conn.commit()
        self.conn.close()
    
    def change_email(self, username, email):
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('UPDATE user SET email = ? WHERE username = ?', (email, username))
        self.conn.commit()
        self.conn.close()
    
    def change_pin(self, email, pin):
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('UPDATE user SET pin = ? WHERE email = ?', (pin, email))
        self.conn.commit()
        self.conn.close()
    
    def delete_account(self, email):
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('DELETE FROM user WHERE email = ?', (email,))
        self.conn.commit()
        self.conn.close()

signup = Signup()