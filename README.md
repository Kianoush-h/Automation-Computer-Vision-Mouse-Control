# Screen Automation Script

## Overview

This Python script utilizes computer vision techniques to automate interactions with a live screen. It identifies predefined regions using template matching, reads configuration data from "order.txt," and performs mouse movements and clicks based on the specified conditions. The script is designed for scenarios where manual interactions with specific screen elements are repetitive and can be automated.

## Key Features

- **Template Matching:** Utilizes OpenCV for template matching to identify specific regions on the screen.
- **Configuration File:** Reads input parameters from the "order.txt" configuration file for dynamic control.
- **Mouse Automation:** Performs mouse movements and clicks based on the identified regions and configuration.

## Usage

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/screen-automation-script.git
    cd screen-automation-script
    ```

2. **Install Dependencies:**
    Ensure that you have the necessary dependencies installed.
    ```bash
    pip install opencv-python pyautogui
    ```

3. **Customize Configuration:**
    - Replace template images in the `screen` directory.
    - Adjust parameters in the "order.txt" file according to your requirements.

4. **Run the Script:**
    ```bash
    python main_script.py
    ```

## Contributions

Contributions and improvements are welcome! If you have ideas for additional features, optimizations, or bug fixes, feel free to submit a pull request.

## Dependencies

- [OpenCV](https://pypi.org/project/opencv-python/)
- [PyAutoGUI](https://pypi.org/project/PyAutoGUI/)

## License

This project is licensed under the [MIT License](LICENSE).
