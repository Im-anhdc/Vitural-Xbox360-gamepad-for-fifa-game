import vgamepad as vg
from pynput import keyboard

# Initialize the virtual gamepad
gamepad = vg.VX360Gamepad()

# Keep track of currently pressed keys
pressed_keys = set()

# Maximum values for joystick movements
MAX_VALUE = 32767

# Track the current stick state
current_left_state = (0, 0)
current_right_state = (0, 0)

# Define the mapping from keyboard keys to gamepad buttons
keyboard_to_gamepad = {
    'w': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,  # Map 'w' to 'Y' button
    'a': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,  # Map 'a' to 'X' button
    'd': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,  # Map 'd' to 'B' button
    's': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,  # Map 's' to 'A' button
    'shift': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,  # Map left shift to LB button
    'z': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,  # Map 'z' to RB button
    '[': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,  # Map '[' to D-pad left
    ']': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT  # Map ']' to D-pad right
}

# Function to check and handle key combos
def check_key_combos():
    if 'shift' in pressed_keys and 'w' in pressed_keys and 'a' in pressed_keys:
        print("Shift + w + a combo detected!")
        # Example action: Press a gamepad button or combo
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        gamepad.update()

    elif 'shift' in pressed_keys and 'w' in pressed_keys and 'd' in pressed_keys:
        print("Shift + w + d combo detected!")
        # Example action: Press a different combo of buttons
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()

    # You can add more combos like this based on your needs

# Function to update the left stick movement based on the pressed keys
def update_left_stick():
    global current_left_state
    x_value = 0
    y_value = 0

    if 'ctrl_l' not in pressed_keys:  # Disable left stick if ctrl_l is pressed
        if 'up' in pressed_keys:
            y_value = MAX_VALUE  # Move up
        if 'down' in pressed_keys:
            y_value = -MAX_VALUE  # Move down
        if 'left' in pressed_keys:
            x_value = -MAX_VALUE  # Move left
        if 'right' in pressed_keys:
            x_value = MAX_VALUE  # Move right

    if (x_value, y_value) != current_left_state:
        current_left_state = (x_value, y_value)
        gamepad.left_joystick(x_value=x_value, y_value=y_value)
        gamepad.update()

# Function to update the right stick movement based on the pressed keys (ctrl_l + arrow keys)
def update_right_stick():
    global current_right_state
    x_value = 0
    y_value = 0

    if 'ctrl_l' in pressed_keys:  # Only move the right stick if ctrl_l is pressed
        if 'up' in pressed_keys:
            y_value = MAX_VALUE  # Move up
        if 'down' in pressed_keys:
            y_value = -MAX_VALUE  # Move down
        if 'left' in pressed_keys:
            x_value = -MAX_VALUE  # Move left
        if 'right' in pressed_keys:
            x_value = MAX_VALUE  # Move right

    if (x_value, y_value) != current_right_state:
        current_right_state = (x_value, y_value)
        gamepad.right_joystick(x_value=x_value, y_value=y_value)
        gamepad.update()

# Function to handle key presses
def on_press(key):
    try:
        # Handle arrow keys for left and right stick
        if key == keyboard.Key.up:
            pressed_keys.add('up')
            update_left_stick()
            update_right_stick()
        elif key == keyboard.Key.down:
            pressed_keys.add('down')
            update_left_stick()
            update_right_stick()
        elif key == keyboard.Key.left:
            pressed_keys.add('left')
            update_left_stick()
            update_right_stick()
        elif key == keyboard.Key.right:
            pressed_keys.add('right')
            update_left_stick()
            update_right_stick()
        elif key == keyboard.Key.ctrl_l:
            pressed_keys.add('ctrl_l')
            update_right_stick()
        elif key == keyboard.Key.shift:
            pressed_keys.add('shift')
            gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            gamepad.update()

        # Handle letter keys for gamepad buttons, making it case insensitive
        if hasattr(key, 'char') and key.char:
            char = key.char.lower()  # Convert to lowercase to handle shift+letter case
            pressed_keys.add(char)  # Add the lowercase version of the key to pressed_keys
            if char in keyboard_to_gamepad:
                gamepad_button = keyboard_to_gamepad[char]
                gamepad.press_button(button=gamepad_button)
                gamepad.update()

        # Special handling for shift+e and shift+c
        if hasattr(key, 'char') and key.char.lower() in ['e', 'c']:
            if key.char.lower() == 'c':  # LT trigger
                gamepad.left_trigger(value=255)
                gamepad.update()
            elif key.char.lower() == 'e':  # RT trigger
                gamepad.right_trigger(value=255)
                gamepad.update()

        # Check for key combos after key press
        check_key_combos()

    except AttributeError as e:
        print(f"Error handling key press: {e}")

# Function to handle key releases
def on_release(key):
    try:
        if key == keyboard.Key.up:
            pressed_keys.discard('up')
            update_left_stick()
            update_right_stick()
        elif key == keyboard.Key.down:
            pressed_keys.discard('down')
            update_left_stick()
            update_right_stick()
        elif key == keyboard.Key.left:
            pressed_keys.discard('left')
            update_left_stick()
            update_right_stick()
        elif key == keyboard.Key.right:
            pressed_keys.discard('right')
            update_left_stick()
            update_right_stick()
        elif key == keyboard.Key.ctrl_l:
            pressed_keys.discard('ctrl_l')
            update_right_stick()
        elif key == keyboard.Key.shift:
            pressed_keys.discard('shift')
            gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            gamepad.update()

        # Handle letter keys for gamepad buttons
        if hasattr(key, 'char') and key.char:
            char = key.char.lower()  # Convert to lowercase to handle shift+letter case
            pressed_keys.discard(char)  # Remove the lowercase version from pressed_keys
            if char in keyboard_to_gamepad:
                gamepad_button = keyboard_to_gamepad[char]
                gamepad.release_button(button=gamepad_button)
                gamepad.update()

        # Special handling for shift+e and shift+c
        if hasattr(key, 'char') and key.char.lower() in ['e', 'c']:
            if key.char.lower() == 'c':  # LT trigger
                gamepad.left_trigger(value=0)
                gamepad.update()
            elif key.char.lower() == 'e':  # RT trigger
                gamepad.right_trigger(value=0)
                gamepad.update()

    except AttributeError as e:
        print(f"Error handling key release: {e}")

# Setup the keyboard listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Keep the script running
listener.join()
