# Keyboard Tray Status Indicator
A lightweight utility that shows your keyboard activity status in the Windows system tray. Simply run the Python script—no build or compilation required. You can also package it as a standalone EXE for easy distribution.
## Key Features
- Detects keyboard inactivity after **10 seconds** of no key presses
- Overlays a red ring on the tray icon when inactive
- Displays the original icon when active
- Supports packaging into a single EXE with PyInstaller
## Requirements
- Windows 10 or 11
- Python 3.7+
### Python Packages
Install the dependencies:
```bash
pip install keyboard pystray pillow
```
## Installation & Usage
1. Clone the repository:
```shell
git clone https://github.com/USERNAME/keyboard-tray-indicator.git cd keyboard-tray-indicator
```
2. Place `keyboard.png` (16×16) in the project root directory.  
3. Run the script:
```bash
python keyboard_tray.py
```
## Building an EXE
Package as a single EXE using PyInstaller:
```bash
# Convert PNG to ICO first (optional)
# python png2ico.py
pyinstaller --onefile --windowed \
    --icon keyboard.ico \
    --add-data "keyboard.png;." \
    keyboard_tray.py
```
- `--onefile`: Bundle into one executable
- `--windowed`: Run without console window
- `--icon keyboard.ico`: Set the EXE icon
- `--add-data "keyboard.png;."`: Include the PNG resource
After building, find `dist/keyboard_tray.exe` and run it to see the tray icon.
## Project Structure
```
keyboard-tray-indicator/
├─ keyboard_tray.py      # Main script
├─ png2ico.py            # PNG→ICO conversion script (optional)
├─ keyboard.png          # Original tray icon image
├─ keyboard.ico          # Icon for the EXE
└─ README.md             # Project documentation
```
## Contributing
Feel free to open issues for bugs or feature requests. Pull requests are always welcome!
## License
This project is licensed under the MIT License. See `LICENSE` for details.
