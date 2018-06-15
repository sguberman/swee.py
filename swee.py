#!/usr/bin/env python3

import copy
import random


def make_grid(size=15, bombs=30):

    # blank (size x size) grid
    grid = [[0 for box in range(size)] for row in range(size)]

    # place bombs
    bomb_count = 0
    while bomb_count < bombs:
        row, col = random.randint(0, size - 1), random.randint(0, size - 1)
        if grid[row][col] != 'x':
            grid[row][col] = 'x'
            bomb_count += 1

    # count neighboring bombs
    for i in range(size):
        for j in range(size):
            if grid[i][j] == 'x':
                continue
            loc = (i, j)
            grid[i][j] = sum(grid[r][c] == 'x' for r, c in next_to(grid, loc))

    return grid


def draw(grid):
    print(' ' * 6 + ' '.join(str(x + 1).rjust(2) for x in range(len(grid[0]))))
    print('     ' + '=' * 3 * len(grid[0]))
    for i, row in enumerate(grid):
        print(f' {i + 1:2d} | ' + ' '.join(str(box).rjust(2) for box in row))


def next_to(grid, location):
    i, j = location

    left = (i, j - 1)
    right = (i, j + 1)
    up = (i - 1, j)
    down = (i + 1, j)
    left_up = (i - 1, j - 1)
    right_up = (i - 1, j + 1)
    left_down = (i + 1, j - 1)
    right_down = (i + 1, j + 1)

    directions = [
        left, right, up, down,
        left_up, right_up, left_down, right_down
    ]

    minr = 0
    minc = 0
    maxr = len(grid) - 1
    maxc = len(grid[0]) - 1

    valid_coordinates = [
        (r, c) for r, c in directions
        if (minr <= r <= maxr) and (minc <= c <= maxc)
    ]

    return valid_coordinates


def reveal(grid, locations=None):
    if locations is None:
        locations = []
    revealed = copy.deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in locations:
                revealed[i][j] = '.'

    return revealed


def flatten(list_of_lists):
    return [y for x in list_of_lists for y in x]


def pick(grid, location, visited=None):
    if visited is None:
        visited = []
    visited.append(location)

    i, j = location
    if grid[i][j] == 'x':
        return []
    elif grid[i][j] > 0:
        return [location]
    else:
        return (
            [location] +
            flatten(
                [pick(grid, loc, visited) for loc in next_to(grid, location)
                 if loc not in visited]
            )
        )


def parse_input(text):
    i, j = map(int, text.split())
    i -= 1
    j -= 1
    return i, j


def main(size=15, bombs=30, cheat=False):
    grid = make_grid(size, bombs)
    revealed = []

    if cheat:  # show the whole grid without hiding anything
        draw(grid)
    else:
        draw(reveal(grid))

    while True:  # main loop
        if len(revealed) == size * size - bombs:  # found all empty spaces
            print('YOU WIN!')
            break

        text = input('Pick a box [row col] -> ')
        if not text or text.lower() == 'q':
            break

        if text == 'cheat':
            draw(grid)
            continue

        try:
            location = parse_input(text)
        except ValueError:
            print('Invalid input.')
            print('Enter a row and column number separated by a space.')
            print('Or enter a blank line to quit.')
            continue

        i, j = location
        try:
            assert 0 <= i <= len(grid)
            assert 0 <= j <= len(grid[0])
        except AssertionError:
            print('Invalid input.')
            print('Choose a row and column number that actually exist.')
            continue

        new_boxes = pick(grid, location)
        if not new_boxes:  # picked a bomb
            print('BOOM! YOU LOSE.')
            break

        revealed.extend(new_boxes)
        draw(reveal(grid, revealed))

    # end of game
    draw(grid)
    again = input('Play again? [Y/n] -> ')
    if again in 'yY':
        main(size, bombs, cheat)


if __name__ == '__main__':
    main()
