# Overview
Knock-Knock is a serverless app service powered by Flask framework and sqlite.
## User Input
- Destination city: A city area the user would like to move to
- "Like" city: The city the user would like the place to be similar to
-  Radius: How far from the destination city will results appear

## Endpoints
"/send_city"
"/detail"
"/retrive_recommendations" - `SELECT * FROM cities WHERE preferences`

## List of Features
The similarity score between two zipcodes is determined by the following factors:
- **Cost of Living Index:** How affordable is the area
- **Walkability:** How car-dependent a zipcode is 
- **Public School Ranking:** How well a public school system ranks in comparison to other districts 
- **Arts and Culture:** How well the arts and culture scene ranks in comparison to other zipcodes
- **Average Temprature (F):** The annual average temperature for a given zipcode
- **Noise Pollution (dB):** The average "noise" measured in decibels of a zipcode
- **Crime Rate:** The annual number of crimes per 100,000 residents
- **Precipitation (in):** The annual precipitation in inches of a zipcode
- **Air Quality (AQI):** The air quality index of a zipcode
- **Housing Price ($):** The average housing price of a given zipcode
- **Age:** The average age of all the residents in a zipcode

- **Zipcode (key):** The data identifier
- **Name:** The name of the zipcode

## Compare to a City

We have all the data in our database already. For instance, to search for Chicago cities, just `SELECT * WHERE seat=chicago;` then calculate similarity score

## Returning

List ordered by similarity score -> detail returns entry so we can compare.

Similarity is the average absolute difference of two entries passed to a sigmoid function.
