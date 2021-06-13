import csv
import sys
import math
import random
import bisect

class Meal:
    def __init__(self):
        self.count = 0
        self.meal_types = ["Breakfast", "Main Meal", "Snack"]
        self.all_foods = { }
        self.index = { }


    # Input format - Name Category Rating
    def getRecents(self, filename = 'recent_items.csv'):
        output = []

        try:
            with open(filename, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    row = "".join(row)
                    output.append(row)
        except:
            pass

        return output


    def loadData(self, inputfile = 'food_option.csv', recentfile = 'recent_items.csv'):
        self.all_foods = {}
        recent = self.getRecents(recentfile)

        with open(inputfile, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:

                if row[0] in recent:
                    continue

                category = row.pop(1)
                if category in self.all_foods:
                    self.all_foods[category].append(row)
                else:
                    self.all_foods[category] = [row]


    def create_index(self, category):
        try:
            val = 0
            for row in self.all_foods[category]:
                val += int(row.pop(1))
                if category not in self.index:
                    self.index[category] = [val]
                else:
                    self.index[category].append(val)
        except:
            print("No options left")
            exit()


    def random_selection(self, category):
        # try:
        #     total_index = self.index[category][-1]
        #     selected_index = math.floor(random.random()*total_index)
        #     selected_index = bisect.bisect(self.index[category], selected_index) - 1
        #     output = self.all_foods[category][selected_index]
        # except:
        #     output = ["No options left"]
        # return output

        try:
            total_index = self.index[category][-1]
            selected_index = round(random.random()*total_index)
            for n, ind in enumerate(self.index[category]):
                if ind > selected_index:
                    break

            n = n -1
            n = 0 if n < 0 else n
            
            nlen = len(self.all_foods[category])
            n = nlen - 1 if n >= nlen else n

            output = self.all_foods[category][n]
        except:
            output = ["No options left"]

        return output




    def foodSelector(self, mtype):
        output = []

        if mtype == "Breakfast":
            self.create_index("Breakfast")
            output = self.random_selection("Breakfast")

        elif mtype == "Snacks":
            self.create_index("Snacks")
            output = self.random_selection("Snacks")

        elif mtype == "Main Meal":
            self.create_index("Curry")
            self.create_index("Dry")

            if __name__ == "__main__":
                try:
                    n = int(input("Select Curry, Dry or Both? Chose 1, 2 or 3 respectively (default 'Both') \n"))
                except ValueError:
                   n = 3

                if n == 1:
                    output = self.random_selection("Curry")
                elif n == 2:
                    output = self.random_selection("Dry")
                elif n == 3:
                    output = self.random_selection("Curry")
                    output.extend(self.random_selection("Dry"))

            else:
                output = [self.random_selection("Curry")[0], self.random_selection("Dry")[0]]

        return output


    def setRecents(self, output):
        recents = []

        try:
            csv_file = open('recent_items.csv', mode='r')
        except:
            csv_file = open('recent_items.csv', mode='w+')
            csv_file.close()

            csv_file = open('recent_items.csv', mode='r')

        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            row = "".join(row)
            recents.append(row)

        if len(recents) > 5:
            del(recents[0])

        for n in output:
            recents.append(n)

        recents = list(set(recents))

        with open('recent_items.csv', mode='w') as csv_file:
            csv_writer = csv.writer(csv_file)
            for row in recents:
                csv_writer.writerow(row)


def main():
    mtype = ""

    if len(sys.argv) < 2:
        print("No meal type specified!")

        n = input("Continue to create a main meal plan? y/n: \n")
        if n != "n" or n != "no":
            mtype = "Main Meal"

        print(f"Meal type - {mtype}")

    else:
        mtype = sys.argv[1]

    # Creat class instance
    meal_obj = Meal()

    if mtype not in meal_obj.meal_types:
        print("Please enter a valid meal!")
        return

    # Load all food options
    print("Loading data...\n")
    meal_obj.loadData()

    # Generate randomized mean plan
    print("Generating meal...\n")
    output = meal_obj.foodSelector(mtype)

    # Save in recents
    meal_obj.setRecents(output)

    print("Final output - ")
    print(output)


if __name__ == "__main__":
    main()
