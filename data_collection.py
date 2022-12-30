"""
This python script can be called to download required project data from kaggle API
Usage: python data_collection.py
"""

# -- Print start message
print("\t -- START DATA COLLECTION PROCESS --")

# -- Import main python modules
import os
from functools import reduce
import pandas as pd
import argparse


# ---- Set command line arguments
descr = 'Perform project data collection'
h = '[-api] or [--kaggle-API] to use the Kaggle API to dowload and unzip project dataset.'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-api', '--kaggle-API', action='store_true', default=argparse.SUPPRESS, help=h)

# -- Collect arguments
api = [v for _, v in parser.parse_args()._get_kwargs()][0]

# -- Cleanup data folder
print("==> Cleaning up `data/` folder ...")
for f in os.listdir('data'):
    if not 'archive.zip' in f:
        os.remove(os.path.join('data', f))

# -- Download `.csv` data tables
if api:
    #  Use Kaggle API to download and unzip data
    print("==> Downloading data from Kaggle API ...")
    os.system("kaggle datasets download -d ahmedlahlou/accidents-in-france-from-2005-to-2016 -p data --unzip")
else:
    # Unzip Kaggle `archive.zip` file
    print("==> Extract data from data/archive.zip ...")
    from zipfile import ZipFile
    with ZipFile(os.path.join('data', 'archive.zip'), 'r') as z:
        z.extractall('data')


# -- Read tables
print("==> Read all datasets ...")
tables = []
for f in  os.listdir('data'):
    if ('holidays' not in f) & (f.endswith('.csv')):
        # -- Build correct path to file
        path = os.path.join('data', f)
        # Read csv with avoiding encoding issues
        try:
            table = pd.read_csv(path, low_memory=False)
        except:
            table = pd.read_csv(path, low_memory=False, encoding='latin-1')
        # Add data in main table list
        tables.append(table)

# -- Merge tables
print("==> Merge all datasets ...")
df = reduce(lambda left, right: pd.merge(left, right, on="Num_Acc"), tables)

# -- Save main dataset as parquet format
print("==> Saving as parquet format ...")
df.to_parquet(os.path.join('data', 'french_accidents.parquet'))

# -- Print end message
print("\t -- END DATA COLLECTION PROCESS --")
