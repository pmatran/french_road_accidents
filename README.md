
[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/)
[![Awesome Badges](https://img.shields.io/badge/badges-awesome-green.svg)](https://github.com/Naereen/badges)

<br>
<H1 align="center"> 
	<b>French road accidents (2005-2016)</b>
	<br>
	<img height="220" width="220" src="assets/car-crash-icon.png">
</H1>
<br>

Description & Content
-----------------------------------------------
This project is a simple Data Science analysis based on the `Kaggle` dataset : [Accidents in France from 2005 to 2016](https://www.kaggle.com/datasets/ahmedlahlou/accidents-in-france-from-2005-to-2016) provided by [Ahmed Lahlou Mimi](https://www.kaggle.com/ahmedlahlou).

The datset contains several data tables related to recorded accidents in french territory:
- `caracteristics.csv`
- `holidays.csv`
- `places.csv`
- `users.csv`
- `vehicles.csv`

All tables are related by a primary key named `Num_Acc` which corresponds to a unique accident id.
The additional `data_collection.py` script perform a bunch of instructions to :
- Collect required data tables using the `Kaggle API`
- Merge all tables on their primary key
- Write a easy-to-read file for analysis (`data/french_accidents.parquet`)

The `plot_utils.py` script contains visualisation functions to help, minimize and clarify some notebook contents.


Installation
------------------------------------------------
In order to 

```shell
git clone https://github.com/pmatran/french_road_accidents.git (https)
git clone git@github.com:pmatran/french_road_accidents.git (ssh)
cd french_road_accidents
```

Make sure to install all dependencies:

```shell
pip install -r requirements.txt
```

Next, install the main dataset through `Kaggle API` by running the following command:

```shell
python data_collection.py
```


Get started
-----------------------------------------------

**_Start the Exploraroty Data Analysis_**
```shell
jupyter notebook EDA.ipynb
```

**_Start the Machine Learning Analysis_**
```shell
jupyter notebook PCA_Clustering.ipynb
```


Contributing
------------------------------------------------
Bug reports, code contributions, or improvements to the documentation are welcome from the community. 
Feel free to suggest improvements by working with your own fork version of `hdtsa`. Go to the project page and hit the **Fork** button.
You will want to clone your fork to your machine:

```shell
git clone <url_french_road_accident> <french_road_accident-yourname>
cd french_road_accident
```


Ressources
-----------------------------------------------
+ [Pandas documentation](https://pandas.pydata.org/docs/)
+ [Plotly documentation](https://plotly.com/python/)
+ [ADTK  documentation](https://adtk.readthedocs.io/en/stable/)
+ [Scikit-learn documentation](https://scikit-learn.org/stable/)


Disclaimer :no_entry:
-----------------------------------------------
This project was created to evaluate the analytic skills of the owner ([@pmatran](https://github.com/pmatran)) by his professor at M2-IASchool (Bordeaux, FRANCE).


Coffee beaks :coffee:
-----------------------------------------------
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/pmatran)
