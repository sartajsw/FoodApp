import csv
import sys
import random
import bisect

count = 0
meal_types = ["breakfast", "main", "snacks"]
all_foods = { }
index = { }


# Input format - Name Category Rating
def getRecents():
    output = []
    with open('recent_items.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            output.extend(row)
    return output


def loadData():
    recent = getRecents()

    with open('food_option.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:

            if row[0] in recent:
                continue

            category = row.pop(1)
            if category in all_foods:
                all_foods[category].append(row)
            else:
                all_foods[category] = [row]


def create_index(category):
    val = 0
    for row in all_foods[category]:
        val += int(row.pop(1))
        if category not in index:
            index[category] = [val]
        else:
            index[category].append(val)


def random_selection(category):
    total_index = index[category][-1]

    selected_index = round(random.random()*total_index)
    selected_index = bisect.bisect(index[category], selected_index) - 1
    
    output = all_foods[category][selected_index]
    return output


def foodSelector(mtype):
    global count

    if mtype == "breakfast":
        if count == 0:
            create_index("Breakfast")

        count += 1
        output = random_selection("Breakfast")

    elif mtype == "snacks":

        if count == 0:
            create_index("Snacks")

        count += 1
        output = random_selection("Snacks")

    elif mtype == "main":

        if count == 0:
            create_index("Curry")
            create_index("Dry")

        count += 1  

        try:
            n = int(input("Select Curry, Dry or Both? Chose 1, 2 or 3 respectively (default 'Both') \n"))
        except ValueError:
            n = 3

        if n == 1:
            output = random_selection("Curry")
        elif n == 2:
            output = random_selection("Dry")
        elif n == 3:
            output = random_selection("Curry")
            output.extend(random_selection("Dry"))

    return output


def setRecents(output):
    recents = []
    with open('recent_items.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            recents.append(row)

    if len(recents) > 5:
        del(recents[0])
    recents.append(output)

    with open('recent_items.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in recents:
            csv_writer.writerow(row)


def main():
    mtype = ""

    if len(sys.argv) < 2:
        print("No meal type specified!")

        n = input("Continue to create a main meal plan? y/n: \n")
        if n != "n" or n != "no":
            mtype = "main"

        print(f"Meal type - {mtype}")

    else:
        mtype = sys.argv[1]

    if mtype not in meal_types:
        print("Please enter a valid meal!")
        return

    # Load all food options
    print("Loading data...\n")
    loadData()

    # Generate randomized mean plan
    print("Generating meal...\n")
    output = foodSelector(mtype)

    # Save in recents
    setRecents(output)

    print("Final output - ")
    print(output)


if __name__ == "__main__":
    main()
