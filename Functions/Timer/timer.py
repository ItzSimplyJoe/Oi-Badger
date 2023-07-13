import threading
import re
import time
from word2number import w2n
from pydub import AudioSegment
import random
import pygame
class Timer:
    def timer(self, duration):
        print(f"Timer set for {duration} seconds.")
        time.sleep(duration)
        pygame.mixer.init()
        pygame.mixer.music.load('Functions/Timer/alarm.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def extract_duration(self, sentence):
        duration = None
        
        keywords = {
            '15 minute timer': 15 * 60,
            '30 minute timer': 30 * 60,
            '60 minute timer': 60 * 60,
            '5 hour timer': 5 * 60 * 60,
            '10 hour timer': 10 * 60 * 60,
            '30 second timer': 30,
            '1 minute timer': 60,
            '45 minute timer': 45 * 60,
        }

        for keyword, dur in keywords.items():
            if keyword in sentence:
                duration = dur
                break
        
        if duration is None:
            match = re.search(r'(\d+)\s*second', sentence)
            if match:
                duration = int(match.group(1))
        
        if duration is None:
            try:
                duration_words = re.search(r'(\w+) (second|minute|hour)s?', sentence)
                if duration_words:
                    duration_num = w2n.word_to_num(duration_words.group(1))
                    duration_unit = duration_words.group(2)
                    
                    if duration_unit == 'second':
                        duration = duration_num
                    elif duration_unit == 'minute':
                        duration = duration_num * 60
                    elif duration_unit == 'hour':
                        duration = duration_num * 60 * 60
            except ValueError:
                pass
        
        return duration

    def handle_sentence(self,sentence):
        duration = self.extract_duration(sentence)
        
        if duration:
            threading.Thread(target=self.timer, args=(duration,)).start()
            return duration
        else:
            print("No valid timer length found.")
            return("No valid timer length found.")

    def main(self,sentence):
        self.handle_sentence(sentence)
        return
    

timer = Timer()