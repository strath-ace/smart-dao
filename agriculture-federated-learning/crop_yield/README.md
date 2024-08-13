# Crop Yield Modelling


## Data

Crop Yield data comes from [LINK](https://ec.europa.eu/eurostat/databrowser/view/apro_cpshr__custom_11014442/default/table?lang=en`).

The georeferenced areas come from [LINK](https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts)

## Data Clean

- Download all georeferenced areas and save crop yield data for all years for the crop type desired. Save this sheet for crop yield seperately from all other sheets and name `dataset.xlsx`.

- Run `generate_combined_data.py`

- `clean_data.xlsx` is the dataset with all estimates removed and only data that has a geographic polygon asigned to it.

- `geo_out.geojson` is a geojson file with the polygon shapes ready for use within GIS software.