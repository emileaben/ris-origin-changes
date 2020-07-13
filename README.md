# ris-origin-changes
Looking at changes in ASNs originating prefixes, are there COVID-19 related changes visible?

# how does this work
The script *doit.py* analyses RIS data between a given start and end date. A single run can do about 7 days worth of files.
In the top of the script there are a start and end time configured, so to create an update
edit the start and end time there.
The data is pulled from an internal database, which can't be accessed from outside RIPE NCC, so this script won't produce
anything useful if you don't have access to this database.
The script produces 2 types of files:
* CSV: have a summary of the number of changes for a given timestamp.
* JSONF: have details on what prefixes and ASNs had what changes.

Both types of files are added to this repository.

CSV files are useful for plotting general trends. This is done in the *plot.py* script that generates graphs
based on these.

The JSONF files can be used to do further research into specific changes on specific dates.
I've tried to map prefixes/ASNs to countries to see country-level specific effects, but there seems to be
too little data to reliably say something there.

