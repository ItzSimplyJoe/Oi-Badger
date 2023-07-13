import sqlite3,hashlib,random,smtplib
class Login:
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

        self.conn = sqlite3.connect('AccountSystem/rememberme.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS user (email TEXT)''')
        self.conn.commit()
        self.conn.close()

    def login(self, emailuser, password):
        password = hashlib.sha256(password.encode()).hexdigest()
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user WHERE (email = ? OR username = ?) AND password = ? ', (emailuser, emailuser, password))
        user = self.c.fetchone()
        self.conn.close()
        return user
    
    def add_remember_me(self, email):
        self.conn = sqlite3.connect('AccountSystem/rememberme.db')
        self.c = self.conn.cursor()
        self.c.execute('INSERT INTO user (email) VALUES (?)', (email,))
        self.conn.commit()
        self.conn.close()
    
    def logout(self):
        self.conn = sqlite3.connect('AccountSystem/rememberme.db')
        self.c = self.conn.cursor()
        self.c.execute('DELETE FROM user')
        self.conn.commit()
        self.conn.close()
    
    def check_pin(self,email,pin):
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user WHERE email = ? AND pin = ?', (email,pin))
        user = self.c.fetchone()
        self.conn.close()
        if user is None:
            return False
        else:
            return True

    def remember_me_check(self):
        self.conn = sqlite3.connect('AccountSystem/rememberme.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user')
        user = self.c.fetchone()
        self.conn.commit()
        self.conn.close()
        return user
    
    def return_user_from_email(self,email):
        self.conn = sqlite3.connect('AccountSystem/accounts.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user WHERE email = ?', (email,))
        user = self.c.fetchone()
        self.conn.commit()
        self.conn.close()
        return user
        
    def forgotten_password(self, email):
        otp = random.randint(100000,999999)
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login('joesvirtualassistant@gmail.com' ,'kpflqtzddozqgjlj')

            subject = 'One Time Password'
            body = ('Your one time password is '+ str(otp))
            footer = ('This is an incredible virtual assistant created by Joe, the virtual assistant probably doesnt work very well. \n If this email is not for you please just ignore it. \n Thankyou very much,\n Joe')

            msg = f'Subject: {subject}\n\n{body}\n\n{footer}'

            smtp.sendmail('joesvirtualassistant@gmail.com', email, msg)
        return otp

login = Login()