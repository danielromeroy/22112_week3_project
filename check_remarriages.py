import wedlock
for person in wedlock.persons:
    parent_marriages = []
    for marr in wedlock.marriage:
        if person[6] == marr[0] and person[5] == marr[1]:
            parent_marriages.append(marr)
    if len(parent_marriages) > 1:
        print(f"Found parent remarriage:\n{parent_marriages}")
