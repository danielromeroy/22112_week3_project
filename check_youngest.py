from wedlock import *
years = []
for person in persons:
    years.append(reformat_birthday(person).year)
print(f"Oldest:{min(years)}\nYoungest: {max(years)}")
