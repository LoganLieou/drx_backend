create table cities (
	zip text primary key not null,
	name text,
	cost_of_living real,
	walkability real,
	public_school_ranking integer,
	arts_and_culture_ranking integer,
	temperature real,
	crime_rate real,
	precipitation real,
	air_quality real,
	housing_price real,
	age integer
);

insert into cities values(
	"777777",
	"Neighborhood A",
	13422.22,
	0.42,
	341,
	20,
	81,
	14.4,
	22.2,
	18.6,
	334600.99,
	32
);

insert into cities values(
	"777776",
	"Neighborhood B",
	13411.22,
	0.41,
	342,
	20,
	81,
	14.4,
	22.2,
	18.6,
	334600.99,
	32
);

insert into cities values(
	"778776",
	"Neighborhood X",
	13411.22,
	0.41,
	342,
	20,
	81,
	14.4,
	22.2,
	18.6,
	334600.99,
	32
);
