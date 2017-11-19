# Hand mouse control

#### Install conda

#### Get code from repository

    git clone https://github.com/jackersson/hand_mouse_control.git
    cd hand_mouse_control

#### Create conda environment (prepared environment in repository folder environment.yml)

    conda env create -f environment.yml
     source activate tutor (environment name - ‘tutor’)

#### Required libraries: python3, OpenCV, numpy, pyautogui

#### Controls

    press ‘a’ - start/stop mouse control
    press ‘w’ - draw blind zones (transparent green) where hand can’t be placed at full size
    press ‘h’ - show/hide green rectangles for hand extraction
    press ‘s’ - calculate range for color hand extraction (color collected from green 9 green rectangles.
    press ‘q’ - quit program

#### Start program

    python main.py -c 0
    # -c 0 -> camera id (if only one camera - 0)

#### Usage

    from the window (‘Colored mask’) you can see how you hand is extracted. 
    place your hand on green rectangles and press ‘s’ until image in window (‘Hand’) show you only your extracted hand
    press ‘h’ to hide green rects
    press ‘a’ to start mouse movements
    move your left hand and watch at mouse. 2 fingers - move, 1 finger - left click, 0 - right click
    press ‘w’ to see blind zones

