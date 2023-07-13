import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
class NaturalLanguageProcessing:
    def predict(self, user_input):
        data = pd.read_csv('ML/nlpdataset.csv')
        sentences = data['Sentence'].tolist()
        keywords = data['Keywords'].tolist()

        sentences_train, sentences_test, keywords_train, keywords_test = train_test_split(sentences, keywords, test_size=0.2, random_state=42)

        vectorizer = CountVectorizer()
        features_train = vectorizer.fit_transform(sentences_train)
        features_test = vectorizer.transform(sentences_test)

        model = MultinomialNB()
        model.fit(features_train, keywords_train)

        accuracy = model.score(features_test, keywords_test)
        print(f"Accuracy: {accuracy:.4f}")
        new_features = vectorizer.transform([user_input])
        new_predictions = model.predict(new_features)
        self.AddDataToCSV(user_input, new_predictions[0])
        return(new_predictions[0])

    def AddDataToCSV(self, sentence, keywords):
        if sentence == "" or keywords == "":
            return
        sentence = sentence.replace(',', '')
        data = pd.read_csv('ML/nlpdataset.csv')
        #check if its already in there to avoid duplicates
        for index, row in data.iterrows():
            if row['Sentence'] == sentence and row['Keywords'] == keywords:
                return
        data.loc[len(data.index)] = [sentence, keywords]
        data.to_csv('ML/nlpdataset.csv', index=False)

nlp = NaturalLanguageProcessing()
