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
If you experience trouble downloading Basemab using pip, try setting up an anaconda environment
```
conda create --name myvenv
conda activate myvenv
```
Then naviagate to the virtual environment (the path should be printed during reation of the venv) and install Basemap
```
conda install -c anaconda basemap
```

We also reccomend installing Gdal using Homwbrew by following these steps. First install Homebrew:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Then install the header files of Gdal, to avoid extra issues:
```
brew install gdal --HEAD
```
Then install Gdal:
```
brew install gdal
```
If you installed Gdal outside your environment you can simply create a python binding by running the following command inside your venv:
```
pip3 install gdal==X.X.X
```
Please replace X.X.X with your installed version of Gdal. You can find the version by running:
```
gdal-config --version 
```
## Built With

* [Django](https://www.djangoproject.com/) - The web framework used

## Data used
* [NASA - CYGNSS](https://podaac.jpl.nasa.gov/CYGNSS) - Reflectometry data

## Author

* **Andreas G. Strand** - [Strand94](https://github.com/Strand94)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
