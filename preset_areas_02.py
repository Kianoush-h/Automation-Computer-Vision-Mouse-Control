import time
import pyautogui
import pytesseract
import easyocr

from PIL import Image

# Set the path to the Tesseract-OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
            print(f"Detected number in 'spin number' area: {number_text}")
            
            if int(number_text) in red_numbers:
                print("spin results is red")
            else:
                print("spin results is black")
            
            print("**\n")
        

def main():
    
    
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
            while True:
                try:
                    take_screenshot_and_detect_number()
                    time.sleep(5)  # Wait for 3 seconds between each screenshot
                except:
                    print('error')
                        

if __name__ == "__main__":
    reader = easyocr.Reader(['en'])
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    main()
