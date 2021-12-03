# Zendesk Ticket Viewer
A simple python CLI utility which can be used to view support tickets using the Zendesk API

# Installation

Ensure you have python3 installed on your machine (this works on Python3):

Install all the necessary packages

```bash
pip install -r requirements.txt
```
Packages needed are:

```bash
requests
pytest
coverage
```

Note: you may need to `pip install . --user` if you get a permission error.

# Testing

Before performing tests, please populate the .ini file with the correct credentials. 
Please fill it with the email, subdomain and password for the user. The password is denoted in the psd field under default section in .ini file. 


**Note:** psd should be a base64 encoded string. This is because in the code, the script will deocde the psd into an ascii decoded string.

To run the viewer, go to the src directory and issue the following command:

```bash
python3 main_menu.py
```

This will initiate a menu driven Ticket Viewer with all options.


# Features
- Displays a list of all tickets
- Pages through 25 tickets at a time
- Displays individual tickets


## Initial Menu Screen
<img src="screenshots/initial_menu.png?raw=true">

## Listing the tickets
<img src="screenshots/list_tickets.png?raw=true">

## Navigating through next pages
<img src="screenshots/navigate_tickets.png?raw=true">

## Single Ticket View
<img src="screenshots/single_ticket_view.png?raw=true">




# Code Coverage

To run the tests and to obtain the code coverage report please run the following command under the src directory:

``` bash
python3 -m pytest --cov='.' --cov-report term  tests.py  
```

The output of the coverage will look like this:

<img src="screenshots/coverage_report.png?raw=true">

The final coverage is 81%
