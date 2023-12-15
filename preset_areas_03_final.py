"""
@author: Kianoush 

GitHUb: https://github.com/Kianoush-h
YouTube: https://www.youtube.com/channel/UCvf9_53f6n3YjNEA4NxAkJA
LinkedIn: https://www.linkedin.com/in/kianoush-haratiannejadi/

Email: haratiank2@gmail.com

"""
import time
import pyautogui
# import pytesseract
import easyocr

from PIL import Image

# Set the path to the Tesseract-OCR executable
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Dictionary to store the coordinates of selected points
points_coordinates = {}

def get_mouse_click_coordinates(option):
    print(f"Please move the mouse to the target area for --{option}-- within the next 4 seconds.")
    time.sleep(4)  # Wait for 4 seconds
    print(f"Now, click on the desktop to set the coordinates for {option}")
    coordinates = pyautogui.position()
    print(f"Coordinates for {option}: {coordinates}")
    points_coordinates[option] = coordinates

def save_coordinates():
    print("\nSaved coordinates:")
    for option, coordinates in points_coordinates.items():
        print(f"{option}: {coordinates}")

def test_areas():
    print("\nTesting saved areas:")
    for option, coordinates in points_coordinates.items():
        print(f"Moving to {option} area: {coordinates}")
        pyautogui.moveTo(coordinates[0], coordinates[1], duration=1)
        time.sleep(1)  # Wait for 1 second at each area

def take_screenshot_and_detect_number():
    spin_number_coordinates = points_coordinates.get("spin number")

    if spin_number_coordinates:
        # Add a small padding to the screenshot area
        x, y = spin_number_coordinates
        width, height = 10, 25
        screenshot = pyautogui.screenshot(region=(x - 15, y - 15, width + 10, height + 10))
        screenshot.save("spin_number.png")

        # # Use pytesseract to perform OCR and extract the number
        # number_text = pytesseract.image_to_string(screenshot, config='--psm 8')
        # print(f"Detected number in 'spin number' area: {number_text.strip()}")
        # Open the image file
        image_path = "spin_number.png"
        original_image = Image.open(image_path)
        
        # Get the original size
        original_width, original_height = original_image.size
        
        # Set the new size (300% of the original size)
        new_width = int(original_width * 3)
        new_height = int(original_height * 3)
        
        # Resize the image
        resized_image = original_image.resize((new_width, new_height))
        
        # Save the resized image
        resized_image_path = "spin_number_resized.png"
        resized_image.save(resized_image_path)
        
        # Close the image files
        original_image.close()
        resized_image.close()

        
        results = reader.readtext(resized_image_path)
        
        if results:
            number_text = results[0][-2]
            # print(f"Detected number in 'spin number' area: {number_text}")
            color = 'w'
            if int(number_text) in red_numbers:
                color = 'red'
                # print("spin results is red")
            else:
                color = 'black'
                # print("spin results is black")
            print("**\n")

            return color,int(number_text)
        
def roulette_bot(spin_result,bet,bet_color):
    global current_color
    global consecutive_spins
    global bet_amount
    global balance
    
    if bet:
        if bet_color == spin_result:
            print("Bet won!")
            # balance += bet_amount
            bet = False
            # bet_amount = 50
        else:
            print("Bet lost. Repeating bet... 2X ")
            # balance -= bet_amount
            # bet_amount *= 2
            # print(f"new bet amount: {bet_amount}")
            coordinates = points_coordinates[bet_strategy_color[current_color] + ' zone']
            print(f"2X: Moving to {bet_strategy_color[current_color] + ' zone'} area: {coordinates}")
            pyautogui.moveTo(coordinates[0], coordinates[1], duration=1)
            pyautogui.moveTo(coordinates[0], coordinates[1], duration=1)
            
    
        
    else:
    
        if current_color == spin_result:
            consecutive_spins += 1
        else:
            consecutive_spins = 1
            current_color = spin_result
    
    
        print(f"Consecutive Spins: {consecutive_spins}")
        print("*"*10)


        if consecutive_spins == 4:
            consecutive_spins = 0
            print("$"*10)
            print(f"Starting: Placing bet on opposite color... bet on {bet_strategy_color[current_color]} ")
            coordinates = points_coordinates[bet_strategy_color[current_color] + ' zone']
            
            print(f"Moving to {bet_strategy_color[current_color] + ' zone'} area: {coordinates}")
            pyautogui.moveTo(coordinates[0], coordinates[1], duration=1)
            bet_color = bet_strategy_color[current_color]
            bet = True


    return bet,bet_color

def main():
    global current_color
    global consecutive_spins
    global bet_amount
    global balance
    global bet
    global bet_color
    
    options = ["bet 1", "red zone", "black zone", "spin number"]

    user_input = "start"
    while user_input != "end":
        text_guide ='''
        1)Enter 'start' to start recording buttons\n
        2)Enter 'test' to test saved areas\n 
        3)Enter 'algo' to start the algorithm\n 
        4)Enter 'end' to exit the program\n
        enter here:
        '''
        # Test saved areas if user inputs "test"
        user_input = input(text_guide)
        
        if user_input.lower() == 'test':
            test_areas()
        elif user_input.lower() == 'start':
            # Get coordinates for each option
            for option in options:
                get_mouse_click_coordinates(option)
        
            # Display and save all coordinates
            save_coordinates()
            
        elif user_input.lower() == 'algo':
            # Continuously take screenshots and detect numbers in the "spin number" area
            number_old = -1
            number_new = -1
            while True:
                color,number_new = take_screenshot_and_detect_number()
                try:
                    if color != 'w' and number_old != number_new:
                        number_old = number_new
                        print(f"spin number is {number_new} and color is {color}")
                        bet,bet_color = roulette_bot(color,bet,bet_color)
                    time.sleep(20)  # Wait for 3 seconds between each screenshot
                except:
                    # print('error')
                    pass
                        

if __name__ == "__main__":
    reader = easyocr.Reader(['en'])
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    consecutive_spins = 0
    current_color = None
    bet_strategy_color = {'red':'black', 'black':'red'}
    bet = False
    bet_color = None
    
    main()

























