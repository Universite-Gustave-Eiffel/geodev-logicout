# Logicout GeoDev project

This project aims to analyze the deliveries made by agricultural producers 
and to determine which ones can be mutualized among producers in order to 
reduce economic and societal costs.

# Note on data

Data is extracted from the [Logicout platform](https://www.logicout.fr/couts/) for research purposes only. 
They are not open for confidentiality reasons but you can contact the [SPLOTT laboratory](https://splott.univ-gustave-eiffel.fr/contacter-le-labo) about them.

5 files are expected in the `data/raw` folder:

- point_arret.csv : departures and delivery points
- simulation.csv : unique simulations entered in the platform
- trajet.csv : trips between two stops
- usage.csv : metadata on the platform usage (for data quality control)
- utilisateur 0603_Etudiants ENSG_nettoyé.xls: filtered user database for the purpose of this study

To use the API present in the code, you will need:

- A logicout API key
- A Google Maps or Mapbox API key

You will need to put these keys in a `.env` file at the root of the repo, formatted as follows :

``` env
LOGICOUT_KEY='my_key'
GMAPS_KEY='my_key'
```
or
``` env
LOGICOUT_KEY='my_key'
MAPBOX_KEY='my_key'
```

# Instructions
## Preparation of the environement
The dependencies used for the project are listed on the file `environment.yml`. 
You can import it as follows :
``` python
conda env create -f environment.yml
```
## Prepare the data
Run once the file 'prep_data.py' to create two CSVs containing all the data necessary to run the algorithm to find the mutualisations (those files will be stored in the  `data/raw` folder).

This script will take as input the files .csv from logicout's database and make spatial and attributaires joins between tables to filter the data by entry, user and localization. 
This process will create the files `data/raw/simulations_gdf.csv` and `data/raw/simulations_reel_gdf.csv`

For the purpose of this study we will only use the file `simulations_reel_gdf.csv` , that contains the selected data of 1097 simulations made in the Logicout application.

Once you have this file, you have to create the file 'ranked_mutualisations.csv'. In this file you will find all the indexes for each tour, sorted in ascending order according to the general index.
To obtain this file, you have to run the script named 'list_mutualisation_index.py'.

## Evaluating the mutualizations

The script 'mutualisation.py' contains a function, "comparison", that takes two routes and make a request to Logicout to calucl the costs of an optimized mutualized itinerary
The informations are then stored in the file "gains.csv"

The 'main.py' script loop through the file "ranked_simulation.csv" and run the function "comparison" for all the lines of the file 'ranked_mutualisations.csv', having as parameter an itinerary and its better mutualization. Note it comes commented by default to avoid an unintended execution, since it will make thousand request for the API and will possibly incur costs in terms of quota.


To run the code, run this command from the root of this project:

```python
python scripts/main.py 
```

Change the `block_size` parameter in [`main.py`](https://github.com/Universite-Gustave-Eiffel/geodev-logicout/blob/2d8285dd33bffa4298774c5eaeac7d1933d5f43c/scripts/main.py#L22) 
to the fix the number of evaluations you want to make by run (default is 20).

## Notebooks

During the development of the project we use jupyter notebooks to show preliminary results and discuss technical issues. They are contained in the notebooks directory and are self-explanatory.

# Licence 

This work is licensed under an 
<a rel="license" href="https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12">
European Union Public Licence (EUPL) version 1.2</a>.

# Contributors

- Nicolas Roelandt - Univ. Eiffel/AME
- Clovis Bergeret - ENSG
- Gautier Tabordet - ENSG
- Claire Girardin - ENSG
- Thiago Rabacal - ENSG
