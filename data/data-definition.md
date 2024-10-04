### Data Source
There are 9 data files.  One for each `region`.  

The source data for each file can be found at the url: https://tropical.atmos.colostate.edu/Realtime/index.php?arch&loc= `region`

The source data is stored locally in `<region>.json`.

The 9 `region`s:
1. global
2. northatlantic
3. northeastpacific
4. northernhemisphere
5. northindian
6. northwestpacific
7. southernhemisphere
8. southindian
9. southpacific


### Columns
Each of the 9 databases have the same layout. (F yeah!)

From left to right, the columns are:
* calendar year of the data
* \# of named storms
* \# of named storm days
* \# of hurricanes/typhoons
* \# of hurricane/typhoon days
* \# of Cat 3+ hurricanes
* \# of Cat 3+ hurricane days
* accumulated cyclone energy

The column names are deduced from the table at [the source url for the data](https://tropical.atmos.colostate.edu/Realtime/index.php?arch&loc=northatlantic).

The use of "typhoon" instead of "hurricane" in `northwestpacific.json` surely must be an oversight.

