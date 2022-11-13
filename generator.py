from faker import Faker
from random import sample
from sqlite3 import connect
from zipcodes import matching, is_real


def generate_tuples(amount: int) -> list:
    """
    Generate tables from Logupogu's idea; FYI, only TX zipcodes will be generated

    :param amount: (int) The amount of tuples to generate
    :return: a list of tuples
    """

    # Predetermined variables
    visited_zips = set()
    tuples = []
    rank = [i for i in range(1, amount + 1)]
    art_rank = [i for i in range(1, amount + 1)]
    faker = Faker()

    for _ in range(amount):
        zipcode = faker.zipcode_in_state('TX')

        # Keep generating valid, unvisited TX zipcodes
        while not is_real(zipcode) or zipcode in visited_zips:
            zipcode = faker.zipcode_in_state('TX')

        # Add zipcode to visited set
        visited_zips.add(zipcode)

        # Crime rate: number of crimes per 100K residents
        data_tuple = (
            zipcode,
            matching(zipcode)[0]["city"],
            faker.pyfloat(min_value=30, max_value=200),
            faker.pyint(min_value=0, max_value=100),
            sample(rank, 1)[0],
            sample(art_rank, 1)[0],
            faker.pyint(min_value=30, max_value=110),
            faker.pyint(min_value=1000, max_value=7000),
            faker.pyfloat(min_value=5, max_value=200),
            faker.pyint(min_value=3, max_value=495),
            faker.pyfloat(right_digits=2, min_value=100000, max_value=1200000),
            faker.pyint(min_value=24, max_value=60)
        )

        print(data_tuple)
        tuples.append(data_tuple)

    return tuples


def insert_into_db(amount: int):
    """
    Given amount of tuples to generate, generate and place in DB

    :param amount: (int) The amount of tuples to generate
    """

    tuples = generate_tuples(amount)

    con = connect("test.db")
    cur = con.cursor()

    try:
        cur.executemany("""INSERT INTO cities VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", tuples)
        con.commit()
    except Exception as e:
        print("ERROR: " + str(e))


if __name__ == "__main__":
    result = insert_into_db(1930)
