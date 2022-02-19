# wedlock.py

# Script to check if there are kids born from wedlock in the database. The code is built upon a few assumptions which
# I explain before the code.

# The code is built upon the assumption that there is no one whose parents have married, divorced, and then remarried to
# the same person, which can be checked by running the following script:
# import wedlock
# for person in wedlock.persons:
#     parent_marriages = []
#     for marr in wedlock.marriage:
#         if person[6] == marr[0] and person[5] == marr[1]:
#             parent_marriages.append(marr)
#     if len(parent_marriages) > 1:
#         print(f"Found parent remarriage:\n{parent_marriages}")

# Also, no one is born in the 1800s. Everyone with 2-digit birth year over 30 has both parents properly recorded, and
# as the exercise description states: "all children's parents are in the database until we go so far back that records
# did not exists".
# import wedlock
# for person in wedlock.persons:
#     cpr = person[0]
#     birthday = cpr[0:6]
#     year_2digits = int(birthday[-2:])
#     if year_2digits > 30 and "" in (person[5], person[6]):
#         print(person)


import mysql.connector
import datetime as dt

# Section for defining functions. Skip to the main program logic if reading the code for the first time.


# Function to reformat the birthdays from the CPR numbers.
# Because the data is from 2016 and there is no one from the 1800s, we can safely assume that anyone with a 2-digit
# birth year bigger than 16 is from the 20th century. When it's bigger than 16, to decide whether a person is from
# the 21st or 20th century, we check if the parents are recorded in the database (again, as the exercise description
# states: "all children's parents are in the database until we go so far back that records did not exists").
def reformat_birthday(person):
    cpr = person[0]
    birthday = cpr[0:6]
    year_2digits = int(birthday[-2:])
    if year_2digits > 16:
        year_4digits = f"19{year_2digits}"
    else:
        year_2digits = f"0{year_2digits}" if year_2digits < 10 else str(year_2digits)  # Add leading zero when necessary
        if "" not in (person[5], person[6]):
            year_4digits = f"20{year_2digits}"
        else:
            year_4digits = f"19{year_2digits}"

    year_4digits = int(year_4digits)
    day = int(birthday[0:2])
    month = int(birthday[2:4])
    birthday = dt.date(day=day, month=month, year=year_4digits)

    return birthday


# Function to reformat the marriage dates into datetime class objects.
def reformat_marriage_dates(marriage):
    start_date = marriage[2]
    start_day = int(start_date[0:2])
    start_month = int(start_date[2:4])
    start_year = int(start_date[-4:])
    start_date = dt.date(day=start_day, month=start_month, year=start_year)

    # If there is no marriage end date, set end date to 2017, which is after the latest recorded person (data is from
    # 2016).
    if marriage[3] == "":
        end_date = dt.date(day=1, month=1, year=2017)
    else:
        end_date = marriage[3]
        end_day = int(end_date[0:2])
        end_month = int(end_date[2:4])
        end_year = int(end_date[-4:])
        end_date = dt.date(day=end_day, month=end_month, year=end_year)

    return start_date, end_date


# Function that searches the database for the parents marriage and returns the marriage if it finds it, and returns
# None if it doesn't.
def get_parents_marriage(person):
    global marriage
    output_marriage = None
    for loop_marriage in marriage:
        if person[6] == loop_marriage[0] and person[5] == loop_marriage[1]:
            output_marriage = loop_marriage
    return output_marriage


# Function that evaluates whether a person is born from wedlock.
def born_from_wedlock(person):
    # If any of the parents isn't recorded, we assume the person is not born from wedlock.
    if "" in (person[5], person[6]):
        return False
    # Get parents marriage. If there is no registered marriage, the kid is born from wedlock. Else, check if the
    # birthday is inside the marriage duration and decide from that whether the kid is born from wedlock or not.
    parents_marriage = get_parents_marriage(person)
    if parents_marriage is None:
        return True
    else:
        birthday = reformat_birthday(person)
        marriage_dates = reformat_marriage_dates(parents_marriage)
        if not (marriage_dates[0] < birthday < marriage_dates[1]):
            return True
        else:
            return False


# Load the data from the database
cnx = mysql.connector.connect(user='sXXXXXX', passwd='XXXXXXXX', db='sXXXXXX', host='localhost')
cur = cnx.cursor()

cur.execute('''SELECT * FROM persons''')
persons = cur.fetchall()

cur.execute('''SELECT * FROM marriage''')
marriage = cur.fetchall()

# Main program logic. Create a list and add every person who is born from wedlock, then print the list.
if __name__ == '__main__':
    wedlock_list = []
    for person in persons:
        if born_from_wedlock(person):
            wedlock_list.append(person)

    print(*wedlock_list, sep="\n")
    print(f"{len(wedlock_list)} kids born from wedlock.")

# Closing the database connection.
cur.close()
cnx.close()

# Output:
# ('010194-4579', 'Odin', 'Friis', 202, 77, '181067-7700', '071069-9649')
# ('010207-7058', 'Eva', 'Kristoffersen', 165, 96, '031278-2640', '280981-2587')
# ('010320-8650', 'Susanne', 'Hjorth', 174, 68, '211205-5370', '090801-9561')
# ('010670-8375', 'Simon', 'Petersen', 161, 98, '080651-3982', '020436-7157')
# ('010822-2961', 'Herluf', 'Laursen', 165, 97, '210406-3862', '040701-0179')
# ... (+ 246 lines not shown here)
# 251 kids born from wedlock.
