import mysql.connector


# Script to track heritable diseases in the database.

# The code builds on the assumptions described in wedlock.py. But also, there is no one who has only 1 registered
# parent, which can be proven by running the following script:
# import heritable_diseases
# for person in heritable_diseases.persons:
#     if (person[5] == "" and person[6] != "") or (person[5] != "" and person[6] == ""):
#         print(person)


# Section for defining functions. Skip to the main program logic when reading the code for the first time.

# Function to get a person given only the CPR number
def fetch_person(cpr):
    global cur
    cur.execute(f'''SELECT * FROM persons WHERE cpr = "{cpr}"''')
    person = cur.fetchall()
    return person[0]


# Function to get all diseases from a given CPR number. It also converts to all lowercase (in case the same diseases are
# recorded with different casing) and converts all types of cancer to simply "cancer".
def fetch_diseases(cpr):
    global cur
    cur.execute(f'''SELECT disease_name FROM disease WHERE cpr = "{cpr}"''')
    person_diseases = cur.fetchall()
    for i in range(len(person_diseases)):
        person_diseases[i] = person_diseases[i][0].lower()
        person_diseases[i] = "cancer" if "cancer" in person_diseases[i] else person_diseases[i]
    return tuple(person_diseases)


# Function to get the CPRs of the grandparents, given the CPRs of the parents. It loops through persons instead of
# using an SQL query, as I timed it to be faster this way (unlike fetch_person and fetch_diseases)
def fetch_grandparents(parents):
    global persons
    grandparents = ["", "", "", ""]
    for person in persons:
        if person[0] == parents[0]:
            grandparents[0], grandparents[1] = person[6], person[5]
        elif person[0] == parents[1]:
            grandparents[2], grandparents[3] = person[6], person[5]
    return grandparents


# Load the data from the database
cnx = mysql.connector.connect(user='sXXXXXX', passwd='XXXXXXXX', db='sXXXXXX', host='localhost')
cur = cnx.cursor()

cur.execute('''SELECT * FROM persons''')
persons = cur.fetchall()

cur.execute('''SELECT * FROM disease''')
diseases = cur.fetchall()

# Main program logic
if __name__ == '__main__':
    # Create a list of tuples, where each one contains the CPRs of a person and their father, mother, parental
    # grandfather, parental grandmother, maternal grandfather and maternal grandmother, always in that exact order.
    # Loop through all the persons in the database, compile all their relevant relatives in a tuple and append it to
    # the list. If there is any lost relative, ignore that person (as the is no one with only one parent recorded, it
    # will be impossible to track a heritable disease.
    peoples_ancestors = []
    for person in persons:
        person_ancestors = []
        if "" in (person[5], person[6]):
            continue
        person_ancestors.extend([person[0], person[6], person[5]])
        person_ancestors.extend(fetch_grandparents(person_ancestors[1:]))
        if "" in person_ancestors:
            continue
        else:
            peoples_ancestors.append(tuple(person_ancestors))

    # List of tuples containing the indexes of the possible direct family lines in the tuples of the peoples_ancestors
    # list.
    family_lines = [(0, 1, 3),
                    (0, 1, 4),
                    (0, 2, 5),
                    (0, 2, 6)]

    # Create a list of tuples, where each one contains the person, the name of the inherited disease, the CPRs of the
    # ancestors who had it and the corresponding family line (as the index of the family_lines list). Loop through
    # the peoples_ancestors list created earlier and get all the diseases each person had. Then loop through the
    # diseases of the person and compare them to the diseases that the parent and grandparent of each family line had
    # (looping through the family lines inside the diseases loop). If both the parent and the grandparent have the
    # disease, add it to the inherited_diseases list.
    inherited_diseases = []
    for person_ancestors in peoples_ancestors:
        ancestors_diseases = [fetch_diseases(ancestor) for ancestor in person_ancestors]
        for disease in ancestors_diseases[0]:
            for i in range(len(family_lines)):
                parent_has = True if disease in ancestors_diseases[family_lines[i][1]] else False
                grandparent_has = True if disease in ancestors_diseases[family_lines[i][2]] else False
                if parent_has and grandparent_has:
                    inherited_diseases.append((person_ancestors[0], disease,
                                               person_ancestors[family_lines[i][1]],
                                               person_ancestors[family_lines[i][2]], i))

    # Relative names in the positions states in the peoples_ancestors and family_lines lists, for printing output
    # properly
    relatives = ("person", "father", "mother",
                 "parental grandfather", "parental grandmother",
                 "maternal grandfather", "maternal grandmother")

    # Loop through the diseases and print out a short phrase describing who has the disease and hteir relative who also
    # had it.
    for disease in inherited_diseases:
        person = fetch_person(disease[0])
        parent = fetch_person(disease[2])
        grandparent = fetch_person(disease[3])
        print(
            f"{person[1]} {person[2]} has had {disease[1]}. Their {relatives[family_lines[disease[4]][1]]} ({parent[1]}"
            f" {parent[2]}) and their {relatives[family_lines[disease[4]][2]]} ({grandparent[1]} {grandparent[2]}) have"
            f" also had it.")

    print(f"Total of {len(inherited_diseases)} diseases tracked.")

# Output:
# Daniel Pedersen has had cancer. Their father (Frank Pedersen) and their parental grandfather (Herman Pedersen) have also had it.
# Betina Ponten has had cancer. Their father (Kurt Kristoffersen) and their parental grandfather (Hasse Kristoffersen) have also had it.
# Sanne Berg has had cancer. Their father (Bent Berg) and their parental grandfather (Danny Vestergaard) have also had it.
# Sanne Berg has had cancer. Their mother (Betty Berg) and their maternal grandfather (Danny Vestergaard) have also had it.
# Inger Thomsen has had hemorrhoids. Their mother (Abelone Thomsen) and their maternal grandfather (Niels Brunak) have also had it.
# ... (+19 lines not shown here)
# Total of 24 diseases tracked.
