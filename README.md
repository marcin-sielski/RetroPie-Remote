# RetroPie-Remote package
RetroPie-Remote package enables control of Emulation Station and Retroarch with remote over HDMI-CEC.

## Installation

Follow the steps:

```git clone https://github.com/marcin-sielski/RetroPie-Remote.git
cd RetroPie-Remote
sudo make install```

and then update ```/opt/retropie/configs/all/retroarch.cfg``` with following config.

```
input_player1_a = "a"
input_player1_b = "b"
input_player1_y = "y"
input_player1_x = "x"
input_player1_start = "d"
input_player1_select = "s"
input_player1_left = "left"
input_player1_right = "right"
input_player1_up = "up"
input_player1_down = "down"
input_player1_enter = "enter"
input_player1_escape = "escape"
input_player1_f1 = "f1"
```

## Issues

Remote control stops working in Retroarch when gamepad is connected on Raspberry Pi 3 B however it works fine on Raspberry Pi Zero W.
