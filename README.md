# OS_Dash_INT



#### Dash APP structure influenced by: https://www.purfe.com/dash-project-structure-multi-tab-app-with-callbacks-in-different-files/

## OverpassAPI

### Limitations
Every service has its limitations, and so does Overpass API:

- Downloading big data

As the size of an Overpass API query result is only known when the download is complete, it is impossible to give an ETA while downloading. And the dynamically generated files from Overpass API typically take longer to generate and download than downloading existing static extracts of the same region. As a result, when you want to extract country-sized regions with all (or nearly all) data in it, it's better to use planet.osm mirrors for that. Overpass API is most useful when the amount of data needed is only a selection of the data available in the region.

Source: https://wiki.openstreetmap.org/wiki/Overpass_API#Limitations 

