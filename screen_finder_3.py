import cv2
import numpy as np
import pyautogui

def find_objects_on_live_screen(template_paths, padding=10):
    # Load the template images
    templates_rgb = [cv2.imread(template_path) for template_path in template_paths]

    # Get the dimensions of the templates
    template_shapes = [template.shape[:2] for template in templates_rgb]

    while True:
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

            found_regions.append(roi)

        # Display the live results
        for i, region in enumerate(found_regions):
            cv2.imshow(f'Live Result {i + 1}', region)

        # Wait for a shorter time between frames (adjust as needed)
        cv2.waitKey(50)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the display windows
    cv2.destroyAllWindows()

# Specify the paths to your template images
template_paths = ['screen/past.png', 'screen/colors.png']

# Call the function to find both objects on the live screen and show the live results
find_objects_on_live_screen(template_paths)
