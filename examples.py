# -*- coding: utf-8 -*-
"""Examples

Usage:
`python -c "from examples import *; simple()"` as an example
"""
import random
from time import sleep

from blessings import Terminal

from progressive.bar import Bar
from progressive.tree import ProgressTree, Value, BarDescriptor


def progress_tree():
    """Example showing tree progress view"""

    #############
    # Test data #
    #############

    # For this example, we're obviously going to be feeding fictitious data
    #   to ProgressTree, so here it is
    leaf_values = [Value(0) for i in range(5)]

    test_d = {
        "Warp Jump": {
            "1) Prepare fuel": {
                "Load Tanks": {
                    "Tank 1": BarDescriptor(type=Bar, value=leaf_values[0]),
                    "Tank 2": BarDescriptor(type=Bar, value=leaf_values[1]),
                },
                "Refine tylium ore": BarDescriptor(type=Bar,
                                                   value=leaf_values[2]),
            },
            "2) Calculate jump co-ordinates": {
                "Resolve common name to co-ordinates": {
                    "Querying resolution from baseship": BarDescriptor(
                        type=Bar, value=leaf_values[3]
                    ),
                },
            },
            "3) Check FTL drive readiness": BarDescriptor(
                type=Bar, value=leaf_values[4]
            )
        }
    }

    # We'll use this function to bump up the leaf values
    def incr_value(obj):
        for val in leaf_values:
            if val.value == 100:
                pass
            elif val.value >= 98:
                val.value = 100
            else:
                val.value += random.choice(range(3))

    # And this to check if we're to stop drawing
    def are_we_done(obj):
        return all(val.value == 100 for val in leaf_values)

    ###################
    # The actual code #
    ###################

    # Create blessings.Terminal instance
    t = Terminal()
    # Initialize a ProgressTree instance
    n = ProgressTree(term=t)
    # We'll use the make_room method to make sure the terminal
    #   is filled out with all the room we need
    n.make_room(test_d)

    while not are_we_done(test_d):
        sleep(0.1 * random.random())
        # After the cursor position is first saved (in the first draw call)
        #   this will restore the cursor back to the top so we can draw again
        n.restore()
        # We use our incr_value method to bump the fake numbers
        incr_value(test_d)
        # Actually draw out the bars
        n.draw(test_d)


def simple():
    """Simple example using just the Bar class

    This example is intended to show usage of the Bar class at the lowest
    level.
    """
    MAX_VALUE = 100

    # Create our test progress bar
    bar = Bar(max_value=MAX_VALUE, fallback=True)

    bar.clear_lines(2)
     # Before beginning to draw our bars, we save the position
    #   of our cursor so we can restore back to this position before writing
    #   the next time.
    bar.save()
    for i in range(MAX_VALUE + 1):
        sleep(0.1 * random.random())
        # We restore the cursor to saved position before writing
        bar.restore()
        # Now we draw the bar
        bar.draw(value=i)
