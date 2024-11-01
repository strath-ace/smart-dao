# Crop Yield in EU by NUTS 2 regions (Area and Yield)


### About

This dataset is from the public dataset on [Eurostat for Crop production in EU standard humidity by NUTS 2 regions](https://ec.europa.eu/eurostat/databrowser/view/apro_cpshr/default/table?lang=en&category=agr.apro.apro_crop.apro_cp.apro_cpsh). All given NUTS 2 regions are listed with their respective countries. 


### Units

- All areas are measured in 1000 ha (hectares)
- All crop yields are measured in 1000 t (metric tonnes)


### Time Window

- Each area and yield are given for the years 2000-2024. Therefore each cell contains 25 datapoints.
- Null/NaN values are given when no information was given in the previous dataset.


### To use

```python
from datasets import load_dataset

dataset = load_dataset("0x365/crop-yield-eu", split="train")
```


### Licensing

The dataset is available under the [Creative Commons License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). The original dataset used to produce this one can be found at [Eurostat for Crop production in EU standard humidity by NUTS 2 regions](https://ec.europa.eu/eurostat/databrowser/view/apro_cpshr/default/table?lang=en&category=agr.apro.apro_crop.apro_cp.apro_cpsh). The changes made are the combination of all datapoints into a single dataset as well as all colons (:) being converted to NaN values and only NUTS 2 regions are displayed in this dataset.


### List of all columns

Crop types are sorted by least amount of missing values (NaN values).

| Column  | Crop Type  |
|-----------|------------|
| | 0 | Province (NUTS 2 Region) |
| | 1 | Country |
| 2 | Harv_Sunflower_seed |
| 3 | Area_Sunflower_seed |
| 4 | Area_Durum_wheat |
| 5 | Harv_Durum_wheat |
| 6 | Harv_Barley |
| 7 | Harv_Common_wheat_and_spelt |
| 8 | Harv_Rice |
| 9 | Area_Cereals_for_the_production_of_grain_including_seed |
| 10 | Area_Barley |
| 11 | Area_Common_wheat_and_spelt |
| 12 | Harv_Sugar_beet_excluding_seed |
| 13 | Area_Rice |
| 14 | Area_Soya |
| 15 | Harv_Tobacco |
| 16 | Harv_Cereals_for_the_production_of_grain_including_seed |
| 17 | Harv_Soya |
| 18 | Area_Dry_pulses_and_protein_crops_for_the_production_of_grain_including_seed_and_mixtures_of_cereals_and_pulses |
| 19 | Area_Sugar_beet_excluding_seed |
| 20 | Area_Rape_and_turnip_rape_seeds |
| 21 | Area_Tobacco |
| 22 | Harv_Rape_and_turnip_rape_seeds |
| 23 | Area_Linseed_oilflax |
| 24 | Harv_Potatoes_including_seed_potatoes |
| 25 | Area_Potatoes_including_seed_potatoes |
| 26 | Area_Green_maize |
| 27 | Harv_Green_maize |
| 28 | Area_Cotton_fibre |
| 29 | Harv_Grain_maize_and_corn-cob-mix |
| 30 | Harv_Fibre_flax |
| 31 | Area_Sorghum |
| 32 | Harv_Cotton_fibre |
| 33 | Harv_Dry_pulses_and_protein_crops_for_the_production_of_grain_including_seed_and_mixtures_of_cereals_and_pulses |
| 34 | Harv_Sorghum |
| 35 | Area_Fibre_flax |
| 36 | Harv_Cotton_seed |
| 37 | Harv_Linseed_oilflax |
| 38 | Area_Grain_maize_and_corn-cob-mix |
| 39 | Harv_Sweet_lupins |
| 40 | Area_Sweet_lupins |
| 41 | Area_Rye_and_winter_cereal_mixtures_maslin |
| 42 | Harv_Rye_and_winter_cereal_mixtures_maslin |
| 43 | Area_Other_fibre_crops_nec |
| 44 | Harv_Other_fibre_crops_nec |
| 45 | Area_Other_cereals_harvested_green_excluding_green_maize |
| 46 | Area_Energy_crops_nec |
| 47 | Harv_Other_permanent_crops_for_human_consumption_nec |
| 48 | Harv_Energy_crops_nec |
| 49 | Harv_Other_cereals_harvested_green_excluding_green_maize |
| 50 | Area_Other_permanent_crops_for_human_consumption_nec |
| 51 | Area_Plants_harvested_green_from_arable_land |
| 52 | Area_Winter_cereal_mixtures_maslin |
| 53 | Area_Oats |
| 54 | Harv_Winter_cereal_mixtures_maslin |
| 55 | Harv_Broad_and_field_beans |
| 56 | Harv_Oats |
| 57 | Harv_Winter_rape_and_turnip_rape_seeds |
| 58 | Harv_Triticale |
| 59 | Area_Winter_rape_and_turnip_rape_seeds |
| 60 | Area_Broad_and_field_beans |
| 61 | Area_Triticale |
| 62 | Area_Industrial_crops |
| 63 | Harv_Hemp |
| 64 | Area_Winter_barley |
| 65 | Area_Common_winter_wheat_and_spelt |
| 66 | Harv_Winter_barley |
| 67 | Harv_Rape_turnip_rape_sunflower_seeds_and_soya |
| 68 | Area_Leguminous_plants_harvested_green |
| 69 | Harv_Common_winter_wheat_and_spelt |
| 70 | Area_Aromatic_medicinal_and_culinary_plants |
| 71 | Area_Rape_turnip_rape_sunflower_seeds_and_soya |
| 72 | Area_Rice_Indica |
| 73 | Harv_Field_peas |
| 74 | Area_Field_peas |
| 75 | Harv_Rice_Indica |
| 76 | Area_Rice_Japonica |
| 77 | Area_Spring_cereal_mixtures_mixed_grain_other_than_maslin |
| 78 | Harv_Cereals_excluding_rice_for_the_production_of_grain_including_seed |
| 79 | Harv_Spring_cereal_mixtures_mixed_grain_other_than_maslin |
| 80 | Area_Cereals_excluding_rice_for_the_production_of_grain_including_seed |
| 81 | Harv_Aromatic_medicinal_and_culinary_plants |
| 82 | Harv_Leguminous_plants_harvested_green |
| 83 | Harv_Rice_Japonica |
| 84 | Area_Temporary_grasses_and_grazings |
| 85 | Area_Hemp |
| 86 | Area_Citrus_fruits |
| 87 | Harv_Citrus_fruits |
| 88 | Area_Other_industrial_crops_nec |
| 89 | Area_Olives |
| 90 | Harv_Olives |
| 91 | Harv_Hops |
| 92 | Harv_Plants_harvested_green_from_arable_land |
| 93 | Area_Other_dry_pulses_and_protein_crops_nec |
| 94 | Harv_Other_cereals_nec_buckwheat_millet_canary_seed_etc |
| 95 | Area_Hops |
| 96 | Area_Other_cereals_nec_buckwheat_millet_canary_seed_etc |
| 97 | Harv_Fibre_crops |
| 98 | Harv_Temporary_grasses_and_grazings |
| 99 | Harv_Other_dry_pulses_and_protein_crops_nec |
| 100 | Area_Spring_rape_and_turnip_rape_seeds |
| 101 | Area_Cotton_seed |
| 102 | Area_Other_root_crops_nec |
| 103 | Area_Fibre_crops |
| 104 | Harv_Spring_rape_and_turnip_rape_seeds |
| 105 | Harv_Other_root_crops_nec |
| 106 | Harv_Common_spring_wheat_and_spelt |
| 107 | Harv_Other_oilseed_crops_nec |
| 108 | Area_Common_spring_wheat_and_spelt |
| 109 | Area_Other_leguminous_plants_harvested_green_nec |
| 110 | Harv_Other_industrial_crops_nec |
| 111 | Harv_Other_leguminous_plants_harvested_green_nec |
| 112 | Area_Spring_barley |
| 113 | Area_Other_oilseed_crops_nec |
| 114 | Area_Root_crops |
| 115 | Harv_Industrial_crops |
| 116 | Area_Lucerne |
| 117 | Harv_Lucerne |
| 118 | Harv_Spring_barley |
| 119 | Harv_Root_crops |
| 120 | Harv_Grapes |
| 121 | Area_Grapes |
| 122 | Harv_Other_plants_harvested_green_from_arable_land_nec |
| 123 | Area_Other_plants_harvested_green_from_arable_land_nec |
| 124 | Area_Clover_and_mixtures |
| 125 | Area_Rye |
| 126 | Harv_Clover_and_mixtures |
| 127 | Harv_Rye |
| 128 | Area_Fresh_vegetables_including_melons_and_strawberries |
| 129 | Area_Fruits_berries_and_nuts_excluding_citrus_fruits_grapes_and_strawberries |
| 130 | Harv_Fresh_vegetables_including_melons_and_strawberries |
| 131 | Area_Oilseeds |
| 132 | Harv_Oilseeds |
| 133 | Area_Oats_and_spring_cereal_mixtures_mixed_grain_other_than_maslin |
| 134 | Harv_Oats_and_spring_cereal_mixtures_mixed_grain_other_than_maslin |
| 135 | Harv_Fruits_berries_and_nuts_excluding_citrus_fruits_grapes_and_strawberries |
| 136 | Harv_Wheat_and_spelt |
| 137 | Area_Wheat_and_spelt |
| 138 | Harv_Arable_land |
| 139 | Area_Utilised_agricultural_area |
| 140 | Harv_Utilised_agricultural_area |
| 141 | Area_Flowers_and_ornamental_plants_excluding_nurseries |
| 142 | Area_Seeds_and_seedlings |
| 143 | Area_Kitchen_gardens |
| 144 | Harv_Kitchen_gardens |
| 145 | Area_Nurseries |
| 146 | Harv_Nurseries |
| 147 | Area_Other_arable_land_crops_nec |
| 148 | Harv_Other_arable_land_crops_nec |
| 149 | Area_Other_permanent_crops |
| 150 | Harv_Other_permanent_crops |
| 151 | Area_Permanent_crops |
| 152 | Harv_Permanent_crops |
| 153 | Area_Permanent_grassland |
| 154 | Harv_Permanent_grassland |
| 155 | Harv_Flowers_and_ornamental_plants_excluding_nurseries |
| 156 | Harv_Fallow_land |
| 157 | Area_Fallow_land |
| 158 | Harv_Seeds_and_seedlings |
| 159 | Area_Arable_land |
