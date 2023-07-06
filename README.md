# Module-10-Sqlalchemy-Challenge
---
1. Analyze Climate Data:

I started with importing the necessary dependencies, and then moved on to begin reflecting tables into the SQLAlchemy ORM by creating an engine and connecting to the SQLite database, which allowed me to view all the classes present. From here I started the precipitation analysis: by finding the most recent date in the provided data set, we're able to calculate back one year and perform a specified query for the data within that year. Then, by loading the query results into a pandas dataframe, we're able to plot and visualize these results. For the station dataset, we can determine which station was the most active and query the last year of temperature data for that station.

2. Climate App:

For designing the climate app, setup is much the same: creating an engine, connecting to the SQLite database, and creating a session for future queries. By using Flask, we're able to design the http static routes for a homepage, the precipitation analysis from previous queries, a complete station list, data for the most active station, and variable routes for finding the minimum, maximum, and average temperatures for a specified start or start-end range. I collaborated a lot with both my classmates Taylor Ward and Ethan Musa on the dynamic routes of this app, and I thank them for helping me try to understand the concept better!