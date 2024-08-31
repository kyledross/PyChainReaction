"""
This is the basic-strategy computer player logic.
This logic will choose a playing position based off of the following criteria, in order.

1. Select a cell that is adjacent to an opponent's cell that will result in a capture of opponent's pieces in a chain reaction.
2. Select a cell that is adjacent to an opponent's cell that will result in a capture of opponent's piece in a single reaction.
3. Select a cell that is adjacent to an opponent's cell that is not full that won't result in a chain reaction, but is increasing the
number of the computer's pieces.
4. Select a cell that is not adjacent to any opponent's cell but is increasing the number of the computer's pieces.
5. Select an empty cell.

In the event that there are more than one possibility that ranks the highest, choose one at random.

Future enhancements:
If there are more than one ranking choice, run a simulation to see what the number of computer cells will be, and choose
the one that yields the best results.

Use machine learning to play the game.
"""

