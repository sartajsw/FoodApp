import os
import PySimpleGUIQt as sg
from mealRandomizer import Meal

layout = [
        [sg.Text("Randomized Meal Generator!")], 
        [sg.Combo(['Main Meal', 'Breakfast', 'Snack'], default_value='Main Meal', key='combo'),
        sg.Button("Create")],
        [sg.Text(' Select Input File:'),
        sg.InputText('Enter Location', key='folder'), 
        sg.FileBrowse()],
        [sg.Button("Reset"), sg.Button("Exit")] 
        ]

# Create Meal instance
meal_obj = Meal()

# Create the window
window = sg.Window("Food App", layout)

# Create an event loop
while True:
    event, values = window.read()

    if event == "Create":
        if not os.path.isfile(values['folder']):
            sg.popup("Invalid File Location")
            continue

        if values['combo'] not in meal_obj.meal_types:
            sg.popup("Please enter a valid meal!")
            continue

        meal_obj.loadData()
        output = meal_obj.foodSelector(values['combo'])
        meal_obj.setRecents(output)

        output = " & ".join(output)
        sg.popup(f"Suggested meal - " + output)

        output = []

    if event == "Reset":
        os.remove('recent_items.csv')

    # End program 
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()

