from ML.Intent_Classification import intent_classifier
from ML.NLP import nlp
from Functions.webanswers.webanswers import webanswers
from Functions.Calendar.calendardbqueries import calendarqueries
from Functions.Timer.timer import timer

class Assistant:
    def __init__(self, name):
        self.name = name

    def reply(self, text):
        text = nlp.predict(text)
        intent = intent_classifier.predict(text)

        replies = {
            'webanswer': webanswers.get_answer,
            'calendar': calendarqueries.main,
            'timer': timer.main,
        }

        try:
            reply_func = replies[intent]
            if callable(reply_func):
                response = reply_func(text)
                return response
        except KeyError:
            print("Sorry, I didn't understand.")
            pass
        except Exception as e:
            print("There has been an error. Please report this to Joe :D")
            print("Error:", str(e))


assistant = Assistant("Badger")
