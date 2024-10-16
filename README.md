# Vitural Xbox360 gamepad for FIFA game
Here is a mapping code for anyone who uses a keyboard for FIFA game. This will create a virtual  game pad and map button to your keyboard key

### 1\. **Initial Setup**

-   The script initializes a virtual gamepad using the `vgamepad` library with `vg.VX360Gamepad()`.
-   Install module `vgamepad`: `pip install vgamepad`
-   A set `pressed_keys` is maintained to track which keys are currently pressed.
-   Constants `MAX_VALUE` (for joystick max movement) and `DIAGONAL_VALUE` (for diagonal stick movement) are defined.
-   Two variables `current_left_state` and `current_right_state` are used to track the current positions of the left and right joysticks.

### 2\. **Key-to-Gamepad Mappings**

-   A dictionary `keyboard_to_gamepad` maps specific keyboard keys (`w`, `a`, `s`, `d`, etc.) to virtual gamepad buttons. For instance:
    -   `'w'` is mapped to the 'Y' button.
    -   `'shift'` is mapped to the left shoulder (LB).
    -   `'z'` is mapped to the right shoulder (RB).

### 3\. **Joystick Updates**

-   The functions `update_left_stick()` and `update_right_stick()` calculate the new x and y values for the left and right joysticks based on the arrow keys pressed.
-   The left stick moves when arrow keys are pressed individually or in combination.
-   The right stick moves when the `Ctrl` key is held down along with the arrow keys.

### 4\. **Key Press Handling**

-   The `on_press()` function detects key presses:
    -   Arrow keys control joystick movements.
    -   The `shift` key controls the left shoulder button (LB).
    -   The `W` key controls the `Y` button.
    -   The `A` key controls the `X` button.
    -   The `S` key controls the `A` button.
    -   The `D` key controls the `B` buuton.
    -   The `[` `]` key controls the D-pad left and right.
    -   The `ctrl_l` key modifies the arrow keys to move the right stick.
    -   The `c` and `e` keys control the LT and RT triggers respectively.

### 5\. **Key Release Handling**

-   The `on_release()` function stops the joystick movement or releases the gamepad buttons when the corresponding keys are released.
