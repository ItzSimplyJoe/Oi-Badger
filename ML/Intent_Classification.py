import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC

class IntentClassifier: ### Makes use of naive bayes classifier algorithm ###
    def __init__(self):
        self.data = pd.read_csv('ML/data.csv')
        self.train()

    def train(self):
        X_train, y_train = self.data['Text'], self.data['Intent']
        self.count_vect = CountVectorizer()
        X_train_counts = self.count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        self.svm = LinearSVC().fit(X_train_tfidf, y_train)
    
    def predict(self, text):
        self.addtofile(text,self.svm.predict(self.count_vect.transform([text]))[0])
        return self.svm.predict(self.count_vect.transform([text]))[0]


    def addtofile(self, text, intent):
        self.data.loc[len(self.data.index)] = [text, intent]
        self.data.to_csv('ML/data.csv', index=False)



intent_classifier = IntentClassifier()