# county-visit-2016
This is just a little project I worked on to familiarize myself with Cartopy.
Inspired by [this Tweet](https://twitter.com/thejacobjoss/status/1231732898463510528?s=21),
I plotted all U.S. counties and highlighted the ones I had visited by shading
them according to the 2016 presidential general election result in each county.

## Notes
* You'll need matplotlib, Cartopy, and possibly Fiona (to resolve a text
    encoding issue with the state shapefile from Natural Earth Data) to run the
    **map.py** script.
* This repo *should* be self-contained — that is, all the code and data you
    should need in order to duplicate my result should be here.
* Don't know your counties' FIPS codes? Look [here](https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697)
    for them.

## Included data
* **countypres_2016.csv** — county-level 2016 presidential election results by
    county, obtained from [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ)
* **us_counties_20m** — shapefile for U.S. counties, obtained from [MetPy](https://unidata.github.io/MetPy/latest/examples/plots/US_Counties.html)

## License
The **map.py** script is licensed under [the Unlicense](https://choosealicense.com/licenses/unlicense/).
I have not found any definitive licensing information for the data included in
this repo, other than that redistribution appears to be allowed, but I 
recommend erring on the side of caution and crediting MetPy and the MIT Election
Data and Science Lab for the data.
