## Environment
Python version: 3.8+

OS: Windows10/Linux

Tested on Windows10 and Ubuntu20.04.

If error message of "Could not load the Qt platform plugin "xcb"..." occurs on Linux, try `apt-get install libxcb-xinerama0`.

## Execution
`python .\start.py` for main window

`python .\start_remote.py` for remote window

## Usage
![name](https://github.com/han11008/Elevator-Simulator/blob/remote/sampleV2.png)
Click button **Add passenger** to input which floor the passenger is at and which floor he/she is going to.

Then the computer will decide which elevator can be taken, you may check the movement of elevators by the values shown on the interface.

You can open remote window to monitor the elevators and schedule their maintenance (that is, the elevator will not be taken unless you restart it).
