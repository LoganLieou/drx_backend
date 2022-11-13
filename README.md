## User Input

Get City Center moving too important preferences, return filtered list of locations.

Serverless app service using flask / django fuck cloud functions I'm so lazy rn using sqlite and flask.
later gonna use ocaml and cockroachdb.

"/send_city"
"/detail"
"/retrive_recommendations" - `SELECT * FROM cities WHERE preferences`

## List of Features

- Cost of Living Index (Publicly Avalible)
- Walkability (Fake Score) (How much area is covered by green space and )
- Public School Ranking (Publicly avalible rankings)
- Arts and Culture (Publicly avalible rankings)
- Average Temprature (Weather Information is openly avalible)
- Noise Pollution (noise codes in some city)
- Crime (Rate)
- Percepitation (Some cities may vary low perssure high pressure areas)
- Air Quality (I wanna breathe) (AQI)
- Housing Price (Probably the government somewhere)
- Age (Similar Stages of Life)

- Zipcode (Identifier)
	- Scrape from wikipedia description and image

## Compare to a City

We have all the data in our database already just `SELECT * WHERE seat=chicago;` then calculate similarity score

## Returning

List ordered by similarity score -> detail returns entry so we can compare.

similarity is cosnie similarity dot prod of two entries and take sigmoid of output.
