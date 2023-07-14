# Oi Badger
The Intelligent Assistant project is a Python-based application that combines various functionalities such as facial recognition, natural language processing, intent classification, calendar management, and timers. It aims to provide a comprehensive solution for tasks related to user interaction, scheduling, and time management.

## Features
The Intelligent Assistant project includes the following features:

### Facial Recognition: 
The application includes facial recognition capabilities to authenticate users based on their facial features. It uses OpenCV and the face_recognition library to detect and compare faces in real-time.

### Natural Language Processing (NLP): 
The NLP component enables the assistant to understand and process user input in natural language. It utilizes the scikit-learn library for intent classification, determining the user's intention based on their input.

### Intent Classification: 
The intent classification module uses machine learning techniques to classify user intents. It employs a linear support vector machine (SVM) algorithm with features extracted from the text input.

### Calendar Management: 
The calendar management functionality allows users to schedule and manage events. It provides a graphical user interface (GUI) for visualizing and interacting with a calendar. The data is stored in an SQLite database, and events can be added, edited, and deleted through the interface.

### Timers: 
The application includes a timer feature that allows users to set timers for specified durations. It supports various input formats, such as specific durations (e.g., "15-minute timer," "1-hour timer") or natural language expressions (e.g., "five minutes," "ten hours"). The timer triggers an alarm sound upon completion.

## Installation
To run the Intelligent Assistant project, follow these steps:

#### Clone the repository to your local machine:

`git clone https://github.com/itzsimplyjoe/Oi-badger.git`
Install the required dependencies. You can use pip to install the dependencies listed in the requirements.txt file:

`pip install -r requirements.txt`
Download any additional resources or models required for the specific modules (e.g., facial recognition models, NLP models) and place them in the appropriate directories.

#### Run the mainUI application file:

`python mainUI.py`

## Usage
Simply run the `mainui.py` file and it should all run correctly.
## Contributing
Contributions to the Intelligent Assistant project are welcome! If you would like to contribute, please follow these steps:

### Fork the repository.

Create a new branch for your feature or bug fix:

`git checkout -b feature-name`
Make your changes and commit them with descriptive commit messages:

`git commit -m "Add feature-name"`
Push your changes to your forked repository:

`git push origin feature-name`
Open a pull request on the main repository's master branch.

Please ensure that your contributions adhere to the project's coding conventions and style guidelines.

## License
The Intelligent Assistant project is licensed under the MIT License.

## Acknowledgements
The project incorporates several open-source libraries and resources, including:

- OpenCV
- face_recognition
- scikit-learn
- PySimpleGUI
- pygame
- word2number
- pydub
I would like to thank the developers and contributors of these libraries for their valuable work.
