import wedlock
for person in wedlock.persons:
    cpr = person[0]
    birthday = cpr[0:6]
    year_2digits = int(birthday[-2:])
    if year_2digits > 30 and "" in (person[5], person[6]):
        print(person)
