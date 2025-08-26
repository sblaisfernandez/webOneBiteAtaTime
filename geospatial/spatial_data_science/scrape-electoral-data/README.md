# Scrape electoral data Canadian election 2025

## Depedencies

```bash
# verify brew is installed
blais@Mac webOneBiteAtaTime % brew --version
Homebrew 4.4.21

brew install miniconda

# verify conda is correctly installed
blais@Mac webOneBiteAtaTime % conda --version
conda 25.1.1
conda info
```

### Create ananconda env

```bash

conda create --name geoenv pandas geopandas matplotlib fiona shapely sqlalchemy requests folium

conda activate geoenv

geoenv) blais@Mac webOneBiteAtaTime % conda env list

# conda environments:
#
base                   /opt/homebrew/Caskroom/miniconda/base
geoenv               * /opt/homebrew/Caskroom/miniconda/base/envs/geoenv

(geoenv) blais@Mac webOneBiteAtaTime % python --version
Python 3.13.2
```

Open the common pallet apply the command

Python: Select interpreter

## Data sources

- [List of all candidats](https://www.elections.ca/content2.aspx?section=can&dir=cand&document=index&lang=f)

## References

- [](https://www.youtube.com/watch?v=km0gda7OcDE)
