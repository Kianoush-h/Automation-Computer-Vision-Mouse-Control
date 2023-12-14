import cv2
import numpy as np
import pyautogui

def find_objects_on_live_screen(template_paths, padding=10):
    # Load the template images
    templates_rgb = [cv2.cvtColor(cv2.imread(template_path), cv2.COLOR_BGR2RGB) for template_path in template_paths]

    while True:
        # Take a screenshot of the entire screen
        screenshot = pyautogui.screenshot()

        # Convert the screenshot to a numpy array
        screenshot_np = np.array(screenshot)

        # Convert the color from BGR to RGB
        screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

        found_regions = []

        # Loop through each template
        for template_rgb in templates_rgb:
            # Match the template using template matching
            result = cv2.matchTemplate(screenshot_rgb, template_rgb, cv2.TM_CCOEFF_NORMED)

            # Find the location of the best match
            _, _, _, max_loc = cv2.minMaxLoc(result)

            # Get the dimensions of the template
            h, w, _ = template_rgb.shape

            # Define the region of interest (ROI) with padding
            top_left = (max_loc[0] - padding, max_loc[1] - padding)
            bottom_right = (max_loc[0] + w + padding, max_loc[1] + h + padding)

            # Crop the region of interest
            roi = screenshot_rgb[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

            found_regions.append(roi)

        # Display the live results
        for i, region in enumerate(found_regions):
            cv2.imshow(f'Live Result {i + 1}', region)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the display windows
    cv2.destroyAllWindows()

# Specify the paths to your template images
template_paths = ['screen/past.png', 'screen/colors.png']

# Call the function to find both objects on the live screen and show the live results
find_objects_on_live_screen(template_paths)
