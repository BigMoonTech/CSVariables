# CSai

#### Video Demo:  <URL HERE>

#### Description:  An A.I. powered Computer Science tutor. Built with Flask, SqlAlchemy, Python, HTML, CSS, Bootstrap 5, JavaScript, and Jquery.

## Table of Contents

- [License](#license)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Discussion](#discussion)
- [Credits](#credits)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)
- [Project Status](#project-status)
- [Project Team](#project-team)

## License
- NO LICENSE

## Installation

1. Create an empty directory for the project.

```
mkdir CSai
```

2. CD into the directory.

```
cd CSai
```

3. Create a virtual environment in the directory (don't forget to activate the VE).

```
python3 -m venv venv
```

4. Clone the project repo

```
git clone https://github.com/BigMoonTech/CSai.git
```

5. Install the requirements

```
pip install -r requirements-dev.txt
```

## Setup

1. You will need to rename config-sample.py to config.py and add your own Openai API key.
2. In the same config.py file, you will need to add your own mail server/gmail credentials.
    1. If you are using gmail, it used to be that you had to enable less secure apps. This has been discontinued.
       Instead, you will have to enable 2-factor authentication and generate an app password. You can find more
       information here: https://support.google.com/accounts/answer/185833?hl=en

## Usage

1. Run the app (port 5000)
```
flask --app src --debug run
```
2. Optionally, you can run the app like so (port 5006):
```
python3 app.py
```
3. Open the app in your browser by pasting this (if port 5000):
```
http://127.0.0.1:5000
```
Note: If you are running the app on port 5006, you will need to change the port number in the URL. Also, you should see something like `* Running on http://127.0.0.1:5000` inside the record.log file that will be generated in your main project directory.

## Discussion
#### This section notes some design, architecture, and implementation decisions that were made.
- This project was built as a final project for CS50, Harvard's Introduction to Computer Science course. It is a full-featured application that allows users to create an account, verify their account through email, login, update their personal information, and interact with the application. 
- CSai utilizes Openai's API to generate responses to user input. The user can ask questions about computer science and the application will respond with a response generated by a GPT-3 model that is fine tuned to act like a computer science tutor.
- The project was written mostly in Python, and built using the Flask framework. It uses SqlAlchemy to interact with a database that stores user information, and information about OpenAi completions.
- The project uses Bootstrap 5 and custom CSS for styling, and Jquery and Javascript for some of the front-end functionality.

#### Architecture:
- CSai (or whatever name is given to the main project folder which holds everything)
  - src (source code folder)
    - db
      - database file
    - db_models
      - database models and db_session file. db_session is used to interact with the database and uses sqlalchemy to create the database, tables, and rows.
    - helpers
      - helper functions
    - infrastructure
      - cookie_auth
        - cookie authentication
      - request_dict
        - A module that allows you to access request.form, request.args, request.headers, and route args as a dictionary
      - tokenizer.py
        - Serializes and deserializes data to send url safe strings to verify accounts
      - view_modifier.py
        - Defines a decorator that is used to modify the view function. Instead of rendering templates everywhere in view methods, I return a dictionary with the request variables etc. to the Jinja2 templates. I use this pattern throughout the project. Basically, when decorated with @response, the view method returns a dictionary, the decorator takes that dictionary, and creates a response with the template specified, and the dictionary values. That is what is rendered from a view method.  
    - services
      - user_service.py
        - Handles user logic. This includes creating a user, verifying a user, and updating user info, such as, how many free calls they have left. It also handles, password hashing, and password verification.
      - completion_service.py
        - Handles OpenAi completions. Searching, creating, adding completions to the db etc.
    - static
      - all the static files
    - templates
      - all the HTML templates
    - view_models
      - The view models are defined here. The view models are used to pass data to the templates in a more organized way, and used within a view method. After a view method's logic plays out, I turn all the model's attributes into a dictionary and return the model from the view method, which then goes to the @response decorator, as stated above.
    - views
      - The views are where logic is controlled. Inside a view method, I create an instance of one of the view_models, perform some logic depending on whether it is a post or get request, and then return the view model's attributes as a dict.
  - init.py
    - Where the app is configured.
  - config.py
    - This is where the environment variables and other configurations are defined
  - app.py
    - Used to run the application with Python3
  - tests 
    - all the tests for testing the app are here
    - conftest.py is used in pytest to share a pytest fixture accross the tests.
    - test_client.py is used to define a pytest fixture, in this case a fixture primarily used to config the app for testing

## Credits
1. training.talkpython.fm
2. realpython.com
3. stackoverflow.com
4. openai.com
5. flask.palletsprojects.com
6. getbootstrap.com
7. jquery.com
8. colorhunt.co
9. google fonts
10. sqlalchmey.org
11. python.org

## Contact
- Email:  moonynotsunny@gmail.com
- Github: BigMoonTech
- LinkedIn: https://www.linkedin.com/in/joshua-aguilar-8677b532/

## Acknowledgements
- training.talkpython.fm was a very useful resource for learning how to use and write some of the infrastructure that the app is centered on. Particullary the request_dict, cookie_auth, and view_modifier modules.
- realpython.com was a great resource for learning how to implement email verification in a flask app.

## Project Status
- [x] In Development
- [ ] In Production
- [ ] In Maintenance

## Project Team
- Joshua Aguilar