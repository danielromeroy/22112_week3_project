import wedlock
for person in wedlock.persons:
    if (person[5] == "" and person[6] != "") or (person[5] != "" and person[6] == ""):
        print(person)

