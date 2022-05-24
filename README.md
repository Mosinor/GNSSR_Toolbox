# GNSSR-Toolbox

The GNSSR-Toolbox is a prototype tool for the collection and processing of Global Navigation Sattelite System Reflectometry data. This website was created in accordance with a master thesis at the Norwegian university NTNU. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

What things you need to install the software and how to install them

Python - The Python programming language: [www.python.org](https://www.python.org/downloads/)

git - Distributed version control system: [git-scm.com/download](https://git-scm.com/downloads)


### Installing

A step by step series of examples that tell you how to get a development env running

First you need to clone the project from Github to a folder of your choice.

```
git clone https://github.com/Strand94/GNSSR-Toolbox.git
```

Create a python virtual enviroment (virtualenv) named venv in the project folder.

Then navigate to the folder in your terminal, activate the enviroment and install the required packages

```
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Finally all you need to do is to run the server locally on your computer while the enviroment is active.

```
python manage.py runserver
```

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used

## Data used
* [NASA - CYGNSS](https://podaac.jpl.nasa.gov/CYGNSS) - Reflectometry data

## Author

* **Andreas G. Strand** - [Strand94](https://github.com/Strand94)
* **Vegard Haneberg** - [vegardhaneberg](https://github.com/vegardhaneberg)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
