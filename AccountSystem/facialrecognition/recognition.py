import cv2
import face_recognition
import threading
import time


def perform_facial_recognition():

    reference_image = face_recognition.load_image_file('AccountSystem/facialrecognition/captured_image.jpg')
    reference_encoding = face_recognition.face_encodings(reference_image)[0]

    found = False
    cap = cv2.VideoCapture(0)
    
    def check_timeout():
        time.sleep(10)
        if not found:
            cap.release()
            cv2.destroyAllWindows()
            return False

    timeout_thread = threading.Thread(target=check_timeout)
    timeout_thread.start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        match_results = face_recognition.compare_faces(face_encodings, reference_encoding)
        similarity_threshold = 0.6
        for (top, right, bottom, left), match in zip(face_locations, match_results):
            if match:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, 'Match', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                found = True
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, 'No match', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        cv2.imshow('Facial Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if found:
            break

    cap.release()
    cv2.destroyAllWindows()
    return found

if __name__ == '__main__':
    perform_facial_recognition()
