import time
import pyautogui

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
        time.sleep(1)  # Wait for 2 seconds at each area

def main():
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    # options = ["bet 1", "bet 2", "bet 3", "red zone", "black zone"]
    options = ["bet 1", "red zone", "black zone", "spin number"]


    user_input = "start"
    while user_input != "end":
        text_guide ='''
        1)Enter 'start' to start recording buttons\n
        2)Enter 'test' to test saved areas\n 
        3)Enter 'end' to exit the program\n
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
            
        

if __name__ == "__main__":
    main()
