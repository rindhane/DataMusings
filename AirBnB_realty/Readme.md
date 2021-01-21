# Airbnb listing's analysis of Boston City.

> **Introduction** : Following code helps to create quick linear model and conduct exploratory analysis of price & demand aspect of airbnb listing within a city. 

### Table of Contents
1. [Getting Started](#gettingStarted)
    * [Prerequisities](#Prerequisites)
    * [Quick Start Guide](#quickguide)
2. [Project Motivation](#motivation)
3. [Results](#results)
4. [File Descriptions](#files)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Getting Started <a name="gettingStarted"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

#### Prerequisites

Following softwares are required to be installed in order to build and run this application/files: 
1. `Python 3` : Follow the guidelines from this [link](https://realpython.com/installing-python/) to install python.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Optional : Install virtual environment for clean setup. Use the [link](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for installation guidelines.

2. `Git` : Follow this [guidelines](https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html) to install & get started with git command line.


#### Quick Start Guide <a name="quickguide"></a>
- Clone the directory into your desired path
```bash
git clone https://github.com/rindhane/DataMusings.git demo
```
- Using terminal go to to inside the dowloaded repository folder
 ```bash
  cd demo/
 ```
- Using terminal initate the python virtual environment and install dependencies
 ```bash
python -m venv pyenv

source pyenv/bin/activate

pip install -r requirements.txt
```
- Run the following command to start and run the files and it will generate the results:
```bash

python main.py
```
## Project Motivation<a name="motivation"></a>

This project dwelves into publicly available data of Airbnb listings within the Boston city. We are interested to find the monetary benefits of listing from the perspectives of home owners. Thus in this project we are interested to understand: 

1. What is the typical earning potential for a general listing within a given city?
2. Is this earning pertains to certain month of the year or is it consistent through out the year ?
3. What are the top factors which influence this earnings and what inferences can help owners to maximise their earnings?

Note: Even though the analysis presently have been done for the Boston City, but python script is generally functional for various city and time periods. One have to modify inputs in the script to do the analysis for other city as well. 

## Results<a name="results"></a>

The main findings of the code can be found at the post available [here](https://rindhane.github.io/entries/Entry1.html)

## File Descriptions <a name="files"></a>
Repository's organization is as follows 

```
Project [Root Folder]/
├── EDA/
│   └── Exploratory_Data_Analysis.ipynb
├── results/   
├── temp/
│
├──main.py
├──downloader.py
├──clean_data.py
├──functions.py
├──model_functions.py
├──requirements.txt
├──structure.py
├── LICENSE
├── README.md 
└── .gitignore
```

**Details:**

+ *EDA:* Contains the jupyter notebooks which will give fair idea about the details and background working of data analysis and its exploration.
+ *results:* It is the folder where by default all the plot results are created when main.py script is run. It could be changed by changing the configuration in main.py
+ *temp:* An optional folder for some temporary scripts were kept for other model testing. 
+ *main.py:* Primary file for initiating the project. When run through the python intrepreter it starts the project from downloading the data till creating the final plots. All confinguration to set the desired city or required time period can be changed through changing the inputs to the variables.
+ *downloader.py:* Holds the functions that are called by main.py to download the *data*.csv.gz file and load them into a dataframe.
+ *clean_data:* This files contains the functions which are called by main.py to clean & preprocess the download to make it suitable for analysis.
+ *functions:* Collection of helper functions used by other files to avoid repeating the code. 
+ *model_functions.py:* This files contains the functions to create and train the machine learning model.
+ *requirements.py:* file required by pip to download the dependencies.
+ *structure.py:* Shows the segregation of columns of raw data , done during the exploratory analysis.


## Licensing, Authors, Acknowledgements<a name="licensing"></a>

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/rindhane/DataMusings/blob/master/LICENSE.md) file for details

### Credits : 
* **Murray Cox** -[Reach out](http://insideairbnb.com/about.html)
    - For creating the *Inside Airbnb* site to access the data of listings 
* [**Udacity**](Udacity) for guiding about Data Science.   
* @Adopted some style from [source](https://github.com/jjrunner/stackoverflow) by [@jjrunner](https://github.com/jjrunner)


------------------------------------
***End***
