import sys
import pprint


def get_grid_from_string(string):
    grid = []
    line = []
    for ind, char in enumerate(string):
        if ind and ind % 9 == 0:
            grid.append(line)
            line = []
        line.append(char)
    grid.append(line)
    return grid


def get_base_list():
    return [str(i) for i in range(1, 10)]


def get_col_values(col_num, sudoku):
    ls = []
    for row in range(9):
        ls.append(sudoku[row][col_num])
    return ls


def get_impossible_values_from_row_and_col(row, col, sudoku):
    return set(sudoku[row] + get_col_values(col, sudoku))


def get_small_grid_dims(row, col):
    if 0 <= row <= 2:
        sm_row_start = 0
        sm_row_fin = 3
    elif 3 <= row <= 5:
        sm_row_start = 3
        sm_row_fin = 6
    elif 6 <= row <= 8:
        sm_row_start = 6
        sm_row_fin = 9

    if 0 <= col <= 2:
        sm_col_start = 0
        sm_col_fin = 3
    elif 3 <= col <= 5:
        sm_col_start = 3
        sm_col_fin = 6
    elif 6 <= col <= 8:
        sm_col_start = 6
        sm_col_fin = 9

    return sm_row_start, sm_row_fin, sm_col_start, sm_col_fin


def get_small_grid_values(row, col, sudoku):
    '''
    It's the most tricky part
    For every sell in main grid small grid 3x3 is analysed for possible numbers except for current string
    all this numbers added to a set
    in the end this set is excluded from the list of base numbers
    '''

    ls = []

    sm_row_start, sm_row_fin, sm_col_start, sm_col_fin = get_small_grid_dims(row, col)

    for sm_row in range(sm_row_start, sm_row_fin):
        for sm_col in range(sm_col_start, sm_col_fin):
            if sm_row == row and sm_col == col:
                continue
            # ls.append(sudoku[sm_row][sm_col])

            if int(sudoku[sm_row][sm_col]):
                ls.extend([sudoku[sm_row][sm_col]])
            else:
                val_list = get_base_list()
                impossible_val = get_impossible_values_from_row_and_col(sm_row, sm_col, sudoku)
                val_list = exclude_items_from_list(val_list, impossible_val)
                ls.extend(val_list)

    return set(ls)


def exclude_items_from_list(l1, *args):
    return [item for item in l1 if item not in [item2 for ls in args for item2 in ls]]


def grid_inspection(sudoku):
    while True:
        value_is_set = False

        for row in range(9):
            for col in range(9):
                if int(sudoku[row][col]):
                    continue

                val_list = get_base_list()
                impossible_val = get_impossible_values_from_row_and_col(row, col, sudoku)
                cur_grid = get_small_grid_values(row, col, sudoku)
                val_list = exclude_items_from_list(val_list, impossible_val, cur_grid)

                if len(val_list) == 1:
                    sudoku[row][col] = val_list[0]
                    pprint.pprint(f'{row}:{col}={val_list[0]}')
                    value_is_set = True

        if not value_is_set:
            return sudoku


sudoku = get_grid_from_string(sys.argv[1])

pprint.pprint(sudoku)
sudoku = grid_inspection(sudoku)
pprint.pprint(sudoku)
