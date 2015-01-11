#!/bin/env python

# In our program the pegs are represented by frozensets in a
# tuple and the discs are represented by numbers which specify
# the disk size. As a result a limitation of this representation
# is that disk must have a unique disk size. This is so that
# our states are hashable as both tuples and frozensets are
# hashable.

# Actions are represented by a tuple of the disk identity / size
# the peg index from where the disk came, and the peg index to where
# the disk has moved

# The state space is the number of pegs to the power of the number
# of disk, i.e.

# 3 pegs and 1 disk:
# 3 ^ 1 = 3 possible states

# 1 peg and 3 disks:
# 1 ^ 3 = 1 possible state

# 3 pegs and 3 disks:
#

from itertools import chain

def tprint(val):
    print(str(val))
    return val

def tdebug(fn):
    def inner(*args, **kwargs):
        return tprint(fn(*args, **kwargs))
    return inner

def tpop(peg):
    stack = list(peg)
    stack.sort()
    if len(stack):
        return stack.pop(0)

def tpegactions(disk, i, state):
    actions = []
    if disk is not None:
        for j, other in enumerate(state):
            odisk = tpop(other)
            if not odisk or odisk > disk:
                actions.append((disk, i, j))
    return actions

def tapplyaction(state, action):
    disk, i, j = action
    positions = list(state)
    positions[i] = state[i] - frozenset([disk])
    positions[j] = state[j] | frozenset([disk])
    return tuple(positions)

def tsuccessors(state):
    return {tapplyaction(state, action): action 
            for action in chain.from_iterable(tpegactions(tpop(peg), i, state)
                for i, peg in enumerate(state))}

def tsolver(start, goal):

    if start == goal:
        return [start]

    explored = set([start])
    frontier = [ [start] ]

    while frontier:
        path = frontier.pop(0)
        current = path[-1]
        for (state, action) in tsuccessors(current).items():
            if state not in explored:
                explored.add(state)
                nxt = path + [action, state]
                if state == goal:
                    return nxt
                else:
                    frontier.append(nxt)

    return []

def tactions(result):
    return result[1::2]

def tsteps(result):
    return len(tactions(result))

# A basic example of the Towers of Hanoi problem
basic_case_start = (frozenset([2,1]), frozenset([]), frozenset([]))
basic_case_goal = (frozenset([]), frozenset([]), frozenset([2,1]))

assert tsolver(basic_case_start, basic_case_start) == [
    (frozenset([2,1]), frozenset([]), frozenset([]))
]

assert tsolver(basic_case_start, basic_case_goal) == [
    (frozenset([2,1]), frozenset([]), frozenset([])),
    (1, 0, 1),
    (frozenset([2]), frozenset([1]), frozenset([])),
    (2, 0, 2),
    (frozenset([]), frozenset([1]), frozenset([2])),
    (1, 1, 2),
    (frozenset([]), frozenset([]), frozenset([2,1]))
]

assert tactions(tsolver(basic_case_start, basic_case_goal)) == [
    (1, 0, 1),
    (2, 0, 2),
    (1, 1, 2)
]

assert tsteps(tsolver(basic_case_start, basic_case_goal)) == 3

print('Basic tests pass')

# A more complex example with a large state space (almost 2M possibilities)
complex_case_start = (frozenset([9,8,7,6,5,4,3,2,1]), frozenset([]), frozenset([]), frozenset([]), frozenset([]))
complex_case_goal = (frozenset([9,6,3]), frozenset([]), frozenset([8,5,2]), frozenset([]), frozenset([7,4,1]))

# Running this may take a minute or so
result = tsolver(complex_case_start, complex_case_start) == [
    (frozenset([9,8,7,6,5,4,3,2,1]), frozenset([]), frozenset([]), frozenset([]), frozenset([]))
]

assert tprint(tsolver(complex_case_start, complex_case_goal)) == [
    (frozenset([1, 2, 3, 4, 5, 6, 7, 8, 9]), frozenset([]), frozenset([]), frozenset([]), frozenset([])),
    (1, 0, 2),
    (frozenset([2, 3, 4, 5, 6, 7, 8, 9]), frozenset([]), frozenset([1]), frozenset([]), frozenset([])),
    (2, 0, 1),
    (frozenset([3, 4, 5, 6, 7, 8, 9]), frozenset([2]), frozenset([1]), frozenset([]), frozenset([])),
    (3, 0, 3),
    (frozenset([4, 5, 6, 7, 8, 9]), frozenset([2]), frozenset([1]), frozenset([3]), frozenset([])),
    (2, 1, 3),
    (frozenset([4, 5, 6, 7, 8, 9]), frozenset([]), frozenset([1]), frozenset([2, 3]), frozenset([])),
    (1, 2, 3),
    (frozenset([4, 5, 6, 7, 8, 9]), frozenset([]), frozenset([]), frozenset([1, 2, 3]), frozenset([])),
    (4, 0, 2),
    (frozenset([8, 9, 5, 6, 7]), frozenset([]), frozenset([4]), frozenset([1, 2, 3]), frozenset([])),
    (5, 0, 4),
    (frozenset([8, 9, 6, 7]), frozenset([]), frozenset([4]), frozenset([1, 2, 3]), frozenset([5])),
    (6, 0, 1),
    (frozenset([8, 9, 7]), frozenset([6]), frozenset([4]), frozenset([1, 2, 3]), frozenset([5])),
    (5, 4, 1),
    (frozenset([8, 9, 7]), frozenset([5, 6]), frozenset([4]), frozenset([1, 2, 3]), frozenset([])),
    (7, 0, 4),
    (frozenset([8, 9]), frozenset([5, 6]), frozenset([4]), frozenset([1, 2, 3]), frozenset([7])),
    (4, 2, 4),
    (frozenset([8, 9]), frozenset([5, 6]), frozenset([]), frozenset([1, 2, 3]), frozenset([4, 7])),
    (8, 0, 2),
    (frozenset([9]), frozenset([5, 6]), frozenset([8]), frozenset([1, 2, 3]), frozenset([4, 7])),
    (5, 1, 2),
    (frozenset([9]), frozenset([6]), frozenset([8, 5]), frozenset([1, 2, 3]), frozenset([4, 7])),
    (1, 3, 4),
    (frozenset([9]), frozenset([6]), frozenset([8, 5]), frozenset([2, 3]), frozenset([1, 4, 7])),
    (2, 3, 2),
    (frozenset([9]), frozenset([6]), frozenset([8, 2, 5]), frozenset([3]), frozenset([1, 4, 7])),
    (6, 1, 0),
    (frozenset([9, 6]), frozenset([]), frozenset([8, 2, 5]), frozenset([3]), frozenset([1, 4, 7])),
    (3, 3, 0),
    (frozenset([9, 3, 6]), frozenset([]), frozenset([8, 2, 5]), frozenset([]), frozenset([1, 4, 7]))
]

print('Complex tests pass')
