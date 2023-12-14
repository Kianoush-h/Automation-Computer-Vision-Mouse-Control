import cv2
import numpy as np
import pyautogui
import time

def mouse_movement(center_x, center_y):
    # Move the mouse to the specified coordinates
    pyautogui.moveTo(center_x, center_y)

def read_order_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            order_data = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in lines}
            return order_data
    except FileNotFoundError:
        print(f'File not found: {file_path}')
        return None

def find_objects_on_live_screen(template_paths, padding=10, order_file_path='order.txt', bets_section_path='screen/bets.png'):
    # Load the template images
    templates_rgb = [cv2.imread(template_path) for template_path in template_paths]
    bets_section_rgb = cv2.imread(bets_section_path)

    # Get the dimensions of the templates
    template_shapes = [template.shape[:2] for template in templates_rgb]
    bets_section_shape = bets_section_rgb.shape[:2]

    # Initialize a variable to alternate between bottom-left and bottom-right sections
    alternate_click = False

    while True:
        # Read the order file
        order_data = read_order_file(order_file_path)

        if order_data is not None:
            # Take a screenshot of the entire screen as a NumPy array
            screenshot_np = np.array(pyautogui.screenshot())

            found_regions = []

            # Loop through each template
            for i, template_rgb in enumerate(templates_rgb):
                # Match the template using template matching
                result = cv2.matchTemplate(screenshot_np, template_rgb, cv2.TM_CCOEFF_NORMED)

                # Find the location of the best match
                _, _, _, max_loc = cv2.minMaxLoc(result)

                # Get the dimensions of the template
                h, w = template_shapes[i]

                # Define the region of interest (ROI) with padding
                top_left = (max_loc[0] - padding, max_loc[1] - padding)
                bottom_right = (max_loc[0] + w + padding, max_loc[1] + h + padding)

                # Crop the region of interest
                roi = screenshot_np[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

                found_regions.append((top_left, bottom_right, roi))

            # Find the "bets section"
            bets_result = cv2.matchTemplate(screenshot_np, bets_section_rgb, cv2.TM_CCOEFF_NORMED)
            _, _, _, bets_max_loc = cv2.minMaxLoc(bets_result)

            # Get the dimensions of the "bets section"
            bets_h, bets_w = bets_section_shape

            # Define the region of interest (ROI) for the "bets section"
            bets_top_left = (bets_max_loc[0], bets_max_loc[1])
            bets_bottom_right = (bets_max_loc[0] + bets_w, bets_max_loc[1] + bets_h)

            # Crop the "bets section"
            bets_roi = screenshot_np[bets_top_left[1]:bets_bottom_right[1], bets_top_left[0]:bets_bottom_right[0]]

            found_regions.append((bets_top_left, bets_bottom_right, bets_roi))

            # Click on the specified number in the "bets section" if the color is black
            # if order_data['color'] == 'red':
            # Calculate the number based on the "bet" value in the order file
            bet_number = int(order_data.get('bet', 1))
            bets_section_width = bets_bottom_right[0] - bets_top_left[0]
            bet_width = bets_section_width // 6
            target_x = bets_top_left[0] + (bet_number - 1) * bet_width + bet_width // 2
            target_y = (bets_top_left[1] + bets_bottom_right[1]) // 2
            mouse_movement(target_x, target_y)
            # Display the live results
            time.sleep(2)
            for i, (top_left, bottom_right, region) in enumerate(found_regions):
                # Move the mouse to the center of the "control panel" part
                if i == 1:  # Assuming "control panel" is the second template
                    center_x = (top_left[0] + bottom_right[0]) // 2
                    center_y = (top_left[1] + bottom_right[1]) // 2

                    # Divide the "control panel" part into four sections
                    quarter_width = (bottom_right[0] - top_left[0]) // 2
                    quarter_height = (bottom_right[1] - top_left[1]) // 2

                    # Check the color specified in the order file and move the mouse accordingly
                    if order_data['color'] == 'red':
                        mouse_movement(center_x - quarter_width // 2, center_y + quarter_height // 2)
                    elif order_data['color'] == 'black':
                        mouse_movement(center_x + quarter_width // 2, center_y + quarter_height // 2)

                    # Toggle the variable to alternate between bottom-left and bottom-right sections
                    alternate_click = not alternate_click


            # Wait for a shorter time between frames (adjust as needed)
            time.sleep(2)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the display windows
    cv2.destroyAllWindows()

# Specify the paths to your template images
template_paths = ['screen/past.png', 'screen/colors.png']

# Call the function to find both objects on the live screen and show the live results
find_objects_on_live_screen(template_paths)
