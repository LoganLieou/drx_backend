from faker import Faker
from random import sample
from zipcodes import matching, is_real


def generate_tuples(amount: int) -> list:
    """
    Generate tables from Logupogu's idea

    :param amount: The amount of tuples to generate
    :return: a list of tuples
    """

    tuples = []
    rank = [i for i in range(1, amount + 1)]
    art_rank = [i for i in range(1, amount + 1)]
    faker = Faker()

    for i in range(amount):
        zipcode = faker.zipcode()
        while not is_real(zipcode):
            zipcode = faker.zipcode()

        name = matching(zipcode)[0]["city"]

        # Crime rate: number of crimes per 100K residents
        data_tuple = {
            "zip": zipcode,
            "name": name,
            "cost_of_living": faker.pyfloat(min_value=30, max_value=200),
            "walkability": faker.pyint(min_value=0, max_value=100),
            "public_school_ranking": sample(rank, 1)[0],
            "arts_and_culture_ranking": sample(art_rank, 1)[0],
            "temperature": faker.pyint(min_value=30, max_value=110),
            "noise": faker.pyint(min_value=20, max_value=55),
            "crime_rate": faker.pyint(min_value=1000, max_value=7000),
            "precipitation": faker.pyfloat(min_value=5, max_value=200),
            "air_quality": faker.pyint(min_value=3, max_value=495),
            "housing_price": faker.pyfloat(right_digits=2, min_value=100000, max_value=1200000),
            "age": faker.pyint(min_value=24, max_value=60)
        }
        print(data_tuple)
        tuples.append(data_tuple)

    return tuples


def insert_into_db(amount: int):
    pass


if __name__ == "__main__":
    generate_tuples(5)