# Walkability_Index_Analysis
Data Analysis Project looking into the Walkability Index presented by the EPA. Using various machine learning models to predict future walkability of various blocks/cities, and cluster data based on neighbourhoods

## Prerequisites
-Python 3
-pip

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/AndrewPitblado/Walkability_Index_Analysis.git
```

### 2. Create Virtual Enviornment

```bash
python3 -m venv .venv
```

### 3. Activate Virtual Enviornment

***MacOS/Linux***
```bash
source .venv/bin/activate
```

***Windows***
```bash
.venv/Scripts/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
### 5. Get the Data
-Download Data from (https://catalog.data.gov/dataset/walkability-index8)
-Place files in `data/` directory

## Usage
```bash
python main.py
#or
jupyter notebook analysis.ipynb
```

## Deactivating Virtual Enviornment

When finished:
```bash
deactivate
```