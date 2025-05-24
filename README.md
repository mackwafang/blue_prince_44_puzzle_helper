# ⚠ Spoiler for Blue Prince Puzzles ahead ⚠
# Blue Prince - Puzzle Helper

A tool to visualize and assist with some puzzles for Blue Prince

## Installation
1. Requires Python 3.10
1. Clone this repo
1. Run `pip install -r requirements.txt`

## How to Run
Simply run `python interface.py`

## How to use the 44 Puzzle Helper
1. On the upper half of the window, select the corresponding square that you are in the game
1. Type in your two hints in any order, separated by a comma (e.g. "Apple, Orange")
1. Look on the lower half of the window, the corresponding grid square (highlighted in light blue) will have the differences in letters.
1. If the differences between the two words is one letter, the grid will be highlighted as green

### Hints Section
- White: Unfilled hint
- Blue: Selected square
- Yellow: Filled out hint
- Black: Antichamber

### Solution Section
- Clear: Unfilled hint
- Blue: Selected Square
- Red: Solution has **more than** 1 letter
- Green: Solution has **exactly** 1 letter
- Black: Antichamber

## How to use the Gallery Helper
1. Place your hints in a square.
1. Start at column 1 and the left most letter in the gallery.
1. Cycle through the choices of the first letter and enter each letter into the columns.
1. Repeat until you have no more letter for this painting.
1. Press submit until you ran out of letters.
1. A list of possible words are generated after submitting (May take a while for 8 words).


### Solution Section
A list of possilbe words and its synomyns are generated in this section after submitting.

## FAQ
- Does my hints save after each sessions?
    - Yes. When you close the tool via the window's close button, the program will write a CSV file in the root directory of this project.
- How do I start fresh?
    - Close the tool, delete `hints.csv` and start again