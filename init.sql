create table cities (
	zip text primary key not null,
	name text,
	cost_of_living real,
	walkability integer,
	public_school_ranking integer,
	arts_and_culture_ranking integer,
	temperature integer,
	crime_rate integer,
	precipitation float,
	air_quality integer,
	housing_price real,
	age integer
);
