import copy
import random


def make_grid(size=10, bombs=20):

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
    print('    ' + '0 1 2 3 4 5 6 7 8 9')
    print('    ' + '===================')
    for i, row in enumerate(grid):
        print(f'{i} | ' + ' '.join(str(box) for box in row))


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


def reveal(grid, locations):
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


def main():
    grid = make_grid(bombs=10)
    revealed = []
    draw(grid)
    while True:
        i, j = map(int, input('Pick a box: ').split())
        turn = pick(grid, (i, j))
        if not turn:
            print('GAME OVER!')
            draw(grid)
            break
        revealed.extend(turn)
        draw(reveal(grid, revealed))


if __name__ == '__main__':
    main()
