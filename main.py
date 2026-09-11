import gspread
import csv
import PIL
from PIL import Image, ImageGrab, ImageDraw
import webbrowser
import random

CARD_WIDTH = 250
CARD_HEIGHT = 350
SHEET_CARD_HEIGHT = 4
SHEET_CARD_WIDTH = 5
SHEET_SIZE = SHEET_CARD_HEIGHT * SHEET_CARD_WIDTH
SHEET_HEIGHT = CARD_HEIGHT * SHEET_CARD_HEIGHT
SHEET_WIDTH = CARD_WIDTH * SHEET_CARD_WIDTH

reader = gspread.api_key("AIzaSyDOsvY1riiBGMfHEN4m0oLA2V4TENxn2OU")
sheet = reader.open_by_key("1RyVuXuTbjReXnPB0BYGq-aMEtmI_Z3HK2iEkngKHFN4")
filename = "card_data.csv"


def generate_card(card_number):
    new_card = PIL.Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), (random.randint(100, 255), random.randint(100, 255), 255))

    

    return new_card

def set_up():

    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(sheet.sheet1.get_all_values())   
        
def generate_sheet():

    card_array = []

    for i in range(SHEET_SIZE):
        card_array.append(generate_card(1))

    new_sheet = Image.new("RGB", (SHEET_WIDTH, SHEET_HEIGHT))

    array_counter = 0

    for i in range(SHEET_CARD_WIDTH):
        for k in range(SHEET_CARD_HEIGHT):

            to_paste = card_array[array_counter]
            new_sheet.paste(to_paste, (CARD_WIDTH * i, CARD_HEIGHT * k))
            array_counter += 1


    new_sheet.save("new_sheet.jpg")

    


def main(): 

    #set_up()

    generate_sheet()
    
    print("Complete.")

if __name__ == '__main__':
    main()
