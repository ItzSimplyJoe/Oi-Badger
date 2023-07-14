from login import login
from signup import signup
from facialrecognition.takeimage import image
from facialrecognition.recognition import perform_facial_recognition
from facialrecognition.facerecognitionchecks import *
import PySimpleGUI as sg

class GUIS:
    def __init__(self):
        self.login = login
        self.signup = signup
        sg.theme('DarkAmber')
    
    def starterpage(self):
        layout = [
            [sg.Text('Welcome to OiBadger')],
            [sg.Text('Your personal Virtual Assistant')],
            [sg.Button('Login'), sg.Button('Signup')]
        ]
        window = sg.Window('Account System', layout, size=(300, 100), element_justification='c', finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Login':
                try:
                    window.close()
                    self.loginui()
                except:
                    self.popup('There was an error opening the login page')
            if event == 'Signup':
                try:
                    window.close()
                    self.signupui()
                except:
                    self.popup('There was an error opening the signup page')
        window.close()

    def loginui(self):
        layout = [
            [sg.Text('Email/Username')],
            [sg.InputText(key='emailuser')],
            [sg.Text('Password/Pin')],
            [sg.InputText(key='password', password_char='*')],
            [sg.Checkbox('Remember me', key='rememberme')],
            [sg.Button('Submit'), sg.Button('Not got an account?'), sg.Button('Forgot password?')]
        ]

        window = sg.Window('Login', layout, size=(300, 200), element_justification='c', finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Submit':
                try:
                    user = self.login.login(values['emailuser'], values['password'])
                    if user:
                        if values['rememberme'] == True:
                            self.login.add_remember_me(str(user[1]))
                            self.proceed(user)
                        else:
                            self.proceed(user)
                    else:
                        self.popup("Invalid login")
                except:
                    self.popup('There was an error logging in')
            if event == "Forgot password?":
                try:
                    window.close()
                    self.forgotpasswordui()
                except:
                    self.popup('There was an error opening the forgot password page')
            if event == 'Not got an account?':
                try:
                    window.close()
                    self.signupui()
                except:
                    self.popup('There was an error opening the signup page')
        window.close()

    def signupui(self):
        column1 = [
            [sg.Text('Email', justification='r', size=(15, 1), font=('Helvetica', 12))],
            [sg.Text('Username', justification='r', size=(15, 1), font=('Helvetica', 12))],
            [sg.Text('Password', justification='r', size=(15, 1), font=('Helvetica', 12))],
            [sg.Text('Confirm Password', justification='r', size=(15, 1), font=('Helvetica', 12))],
            [sg.Button('Submit', size=(15, 1))]
        ]
        column2 = [
            [sg.InputText(key='email', justification='r', size=(25,1))],
            [sg.InputText(key='username', justification='r', size=(25,1))],
            [sg.InputText(key='password', password_char='*', justification='r', size=(25,1))],
            [sg.InputText(key='confirmpassword', password_char='*', justification='r', size=(25,1))],
            [sg.Button('Already got an account?',size=(22,1))]
        ]
        layout= [
            [sg.Column(column1), sg.Column(column2)]
        ]
        window = sg.Window('Signup', layout, finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Submit':
                try:
                    if values['password'] != values['confirmpassword']:
                        self.popup('Passwords do not match')
                    elif self.signup.check_email(values['email']):
                        self.popup('Email already in use')
                    elif self.signup.check_username(values['username']):
                        self.popup('Username already in use')
                    elif self.passwordvalidation(values['password']) == False:
                        self.popup('Password must be at least 8 characters long and contain at least 1 number and 1 letter')
                    else:
                        self.signup.add_user(values['email'], values['username'], values['password'], None)
                        self.popup('Account created')
                        window.close()
                        self.loginui()
                except:
                    self.popup('There was an error signing up')
            if event == 'Already got an account?':
                try:
                    window.close()
                    self.loginui()
                except:
                    self.popup('There was an error opening the login page')
        window.close()
    
    def forgotpasswordui(self):
        layout = [
            [sg.Text('Email')],
            [sg.InputText(key='email')],
            [sg.Button('Back'), sg.Button('Send email')]
        ]
        window = sg.Window('Forgot password', layout, element_justification='c', finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Back':
                try:
                    window.close()
                    self.loginui()
                except:
                    self.popup('There was an error opening the login page')
            if event == 'Send email':
                try:
                    if self.signup.check_email(values['email']):
                        try:
                            otp = self.login.forgotten_password(values['email'])
                            self.popup('Email sent')
                        except:
                            self.popup('There was an error sending the email')
                        if otp is not None:
                            window.close()
                            self.otpui(otp, values['email'])
                    else:
                        self.popup('Invalid Email')
                except:
                    self.popup('There was an error with the OTP')
        window.close()

    def otpui(self, otp, email):
        layout = [
            [sg.Text('Enter the otp sent to your email'), sg.InputText(key='otp')],
            [sg.Text('Enter your new password'), sg.InputText(key='password')],
            [sg.Text('Confirm your new password'), sg.InputText(key='confirmpassword')],
            [sg.Button('Submit')]
        ]
        window = sg.Window('OTP', layout, element_justification='c', finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Submit':
                try:
                    if values['password'] != values['confirmpassword']:
                        self.popup('Passwords do not match')
                    else:
                        if values['otp'] == otp:
                            try:
                                if self.passwordvalidation(values['password']) == False:
                                    self.popup('Password must be at least 8 characters long and contain at least 1 number and 1 letter')
                                else:
                                    self.signup.change_password(email, values['password'])
                                    window.close()
                                    self.loginui()
                            except:
                                self.popup('There was an error changing your password')
                        else:
                            self.popup('Invalid OTP')
                except:
                    self.popup('There was an error with the OTP')
        window.close()
    
    def remembermeui(self, user):
        layout = [
            [sg.Text('Welcome back ' + user[2])],
            [sg.Text('Would you like to use facial recognition or pin to login?')],
            [sg.Button('Facial recognition'), sg.Button('Pin'), sg.Button('Logout')]
        ]
        window = sg.Window('Remember me', layout, element_justification='c', finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Facial recognition':
                try:
                    window.close()
                    self.facialrecognitionui(user)
                except:
                    self.popup('There was an error opening the facial recognition page')
            if event == 'Pin':
                try:
                    window.close()
                    self.pinui(user)
                except:
                    self.popup('There was an error opening the pin page')
            if event == "Logout":
                try:
                    window.close()
                    login.logout()
                    self.loginui()
                except:
                    self.popup('There was an error logging out')
        window.close()
    
    def facialrecognitionui(self, user):
        layout = [
            [sg.Text('Since you have never taken a picture before')],
            [sg.Text('Look at the camera')],
            [sg.Text('Press the button below to start')],
            [sg.Text('Press escape to stop')],
            [sg.Text('Press the button at the bottom of the window to take the picture')],
            [sg.Button('Start'), sg.Button('Back')],
        ]
        layout2 = [
            [sg.Text('Welcome back')],
            [sg.Text('Look at the camera')],
            [sg.Text('Press the button below to start')],
            [sg.Text('Press escape to stop')],
            [sg.Button('Start'), sg.Button('Back')],
        ]
        if image_check():
            window = sg.Window('Facial recognition', layout, element_justification='c', finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')
        else:
            window = sg.Window('Facial recognition', layout2, element_justification='c', finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Back':
                try:
                    window.close()
                    self.remembermeui(user)
                except:
                    self.popup('There was an error opening the previous page')
            if event == "Start":
                try:
                    if image_check():
                        try:
                            image()
                            window.close()
                            self.facialrecognitionui(user)
                        except:
                            self.popup('There was an error with facial recognition')
                    else:
                        try:
                            check = perform_facial_recognition()
                            if check:
                                window.close()
                                self.proceed(user)
                            else:
                                window.close()
                                self.popup('Facial recognition failed, please try using a pin instead')
                                self.remembermeui(user)
                        except:
                            self.popup('There was an error with facial recognition')
                except:
                    self.popup('There was an error starting facial recognition')
        window.close()

    def pinui(self, user):
        layout = [
            [sg.Text('Enter your pin')],
            [sg.InputText(key='pin')],
            [sg.Button('1'), sg.Button('2'), sg.Button('3')],
            [sg.Button('4'), sg.Button('5'), sg.Button('6')],
            [sg.Button('7'), sg.Button('8'), sg.Button('9')],
            [sg.Button('Backspace'), sg.Button('0'), sg.Button('Clear')],
            [sg.Button('Back'), sg.Button('Submit')]
        ]
        layout2= [
            [sg.Text('Create your pin')],
            [sg.InputText(key='pin')],
            [sg.Button('1'), sg.Button('2'), sg.Button('3')],
            [sg.Button('4'), sg.Button('5'), sg.Button('6')],
            [sg.Button('7'), sg.Button('8'), sg.Button('9')],
            [sg.Button('Backspace'), sg.Button('0'), sg.Button('Clear')],
            [sg.Button('Back'), sg.Button('Submit')]
        ]
        
        if self.signup.check_pin(user[1]):
            window = sg.Window('Pin', layout, element_justification='c', finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')
        else:
            window = sg.Window('Pin', layout2, element_justification='c', finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Back':
                try:
                    window.close()
                    self.remembermeui(user)
                except:
                    self.popup('There was an error opening the previous page')
            if event == 'Backspace':
                try:
                    window['pin'].update(window['pin'].get()[:-1])
                except:
                    self.popup('There was an error with the pin')
            if event == 'Clear':
                try:
                    window['pin'].update('')
                except:
                    self.popup('There was an error with the pin')
            if event == 'Submit':
                if self.signup.check_pin(user[1]):
                    try:
                        pin = int(values['pin'])
                        if self.login.check_pin(user[1], pin):
                            window.close()
                            self.proceed(user)
                        else:
                            self.popup('Invalid pin')
                    except:
                        self.popup('Invalid pin')
                else:
                    try:
                        pin = int(values['pin'])
                        if len(str(pin)) >= 4 and len(str(pin)) <= 8:
                            if str(pin).isnumeric():
                                self.signup.change_pin(user[1], pin)
                                window.close()
                                self.proceed(user)
                    except:
                        self.popup('Invalid pin')
            if event in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                try:
                    window['pin'].update(window['pin'].get() + event)
                except:
                    self.popup('There was an error with the pin')
        window.close()
    

    def popup(self, text):
        layout = [
            [sg.Text(text)],
            [sg.Button('Ok')]
        ]
        window = sg.Window('Popup', layout, element_justification='c', finalize=True, icon='AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=False, titlebar_icon='AccountSystem/badger.ico')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Ok':
                break
        window.close()


    def remembermecheck(self):
        email = self.login.remember_me_check()
        if email != None:
            user = self.login.return_user_from_email(email[0])
            self.remembermeui(user)
        else:
            self.starterpage()
    
    def proceed(self, user):
        return (user[1])
    
    def passwordvalidation(self, password):
        if len(password) < 7:
            return False
        else:
            return True

gui = GUIS()
