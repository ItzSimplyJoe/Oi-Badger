import cv2
import PySimpleGUI as sg
from PIL import Image, ImageTk

def image():
    def capture_image():
        nonlocal capturing
        capturing = False
        _, frame = video_capture.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image.thumbnail((400, 300))
        photo = ImageTk.PhotoImage(image)
        image_elem.update(data=photo)

        image.save("AccountSystem/facialrecognition/captured_image.jpg")
        print("Image saved as captured_image.jpg")

        window['-CAPTURE-'].update(disabled=True)
        window['-PROCEED-'].update(disabled=False)
        window['-RETAKE-'].update(disabled=False)

    def proceed_image():
        window.close()

    def retake_image():
        nonlocal capturing
        capturing = True
        window['-CAPTURE-'].update(disabled=False)
        window['-PROCEED-'].update(disabled=True)
        window['-RETAKE-'].update(disabled=True)
        update_image()

    def update_image():
        if capturing:
            _, frame = video_capture.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image.thumbnail((400, 300))
            photo = ImageTk.PhotoImage(image)
            image_elem.update(data=photo)

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("No webcam found. Exiting...")
        exit()

    capturing = True

    layout = [
        [sg.Image(filename='', key='-IMAGE-')],
        [sg.Button('Capture', key='-CAPTURE-', disabled=False), sg.Button('Proceed', key='-PROCEED-', disabled=True), sg.Button('Retake', key='-RETAKE-', disabled=True)]
    ]

    window = sg.Window('Webcam Capture', layout, background_color='black', element_justification='center', no_titlebar=False, finalize=True, icon = 'AccountSystem/badger.ico', resizable=False, return_keyboard_events=True, use_default_focus=True, titlebar_icon='AccountSystem/badger.ico')
    image_elem = window['-IMAGE-']

    while True:
        event, values = window.read(timeout=10)
        if event == sg.WINDOW_CLOSED:
            break

        if event == '-CAPTURE-':
            capture_image()

        if event == '-PROCEED-':
            proceed_image()

        if event == '-RETAKE-':
            retake_image()

        update_image()

    window.close()
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    image()
