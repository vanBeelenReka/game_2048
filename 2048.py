# for printing the table
from tabulate import tabulate
# for chosing the random positions
from random import randint
# for pressing a key without the enter
from msvcrt import getch
# tabulate.PRESERVE_WHITESPACE = True
import os


def print_table(table):
    print(tabulate(table, tablefmt="fancy_grid"))


def get_random_position():
    return (randint(0, 3), randint(0, 3))


def add_new_number_to_the_table(table):
    # if there is no empty space in the table, returns false
    if ("_" not in [elem for sublist in table for elem in sublist]):
        return False

    while True:
        position = get_random_position()
        if table[position[0]][position[1]] == "_":
            percent = randint(1, 100)
            if percent < 70:
                value = 2
            else:
                value = 4
            table[position[0]][position[1]] = value
            break

    # if it could add a new value, returns True
    return True


def initialize_game(table, starting_numbers_count):
    for i in range(starting_numbers_count):
        if add_new_number_to_the_table(table) is False:
            print("The table is full")


def column(table, i):
    return [row[i] for row in table]


def check_for_free_space(table):
    for inside in table:
        for j in inside:
            if j == "_":
                return True
    return False


def check_neighbours(element, table, pozi, pozj):
    if ((pozj + 1) < len(table[0])) and ((pozi + 1) < len(table[0])):
        if element == table[pozi+1][pozj] or element == table[pozi][pozj+1]:
            return True
    if ((pozj + 1) == len(table[0])) and ((pozi + 1) < len(table[0])):
        if element == table[pozi+1][pozj]:
            return True
    if ((pozj + 1) < len(table[0])) and ((pozi + 1) == len(table[0])):
        if element == table[pozi][pozj + 1]:
            return True
    return False


def exist_movement(table):
    if check_for_free_space(table):
        return True
    for i in range(len(table[0])):
        for j in range(len(table[0])):
            if check_neighbours(table[i][j], table, i, j):
                return True
    return False


# from left to right
def add_duplicates(one_column):
    index = len(one_column) - 1
    while index > 0:
        if one_column[index] == "_":
            index -= 1
        else:
            inside_index = index - 1
            while one_column[inside_index] == "_" and inside_index > 0:
                inside_index -= 1
            if one_column[index] == one_column[inside_index]:
                one_column[index] += one_column[inside_index]
                one_column[inside_index] = "_"

            index -= 1
    return one_column


# from left to right
def move_values(one_column):
    index = len(one_column) - 2
    while index >= 0:
        if one_column[index] == "_":
            pass
        else:
            inside_index = index + 1
            while one_column[inside_index] == "_" and inside_index < len(one_column):
                inside_index += 1
                if inside_index == len(one_column):
                    break
            if (one_column[inside_index - 1] == "_"):
                one_column[inside_index-1] = one_column[index]
                one_column[index] = "_"
        index -= 1
    return one_column


def move_down(table):
    new_table = [["_"] * len(table[0]) for i in range(len(table[0]))]
    for i in range(len(table[0])):
        new_table[i] = move_values(add_duplicates(column(table, i)))

    # rotate back the table
    for i in range(len(new_table[0])):
        table[i] = column(new_table, i)


def move_up(table):
    new_table = [["_"] * len(table[0]) for i in range(len(table[0]))]
    for i in range(len(table[0])):
        new_table[i] = column(table, i)[::-1]
    for i in range(len(table[0])):
        new_table[i] = move_values(add_duplicates(new_table[i]))

    # rotate back the table
    for i in range(len(new_table[0])):
        table[i] = column(new_table, len(new_table[0]) - (i+1))


def move_right(table):
    for i in range(len(table[0])):
        table[i] = move_values(add_duplicates(table[i]))


def move_left(table):
    new_table = [["_"] * len(table[0]) for i in range(len(table[0]))]
    for i in range(len(table[0])):
        new_table[i] = move_values(add_duplicates(table[i][::-1]))

    for i in range(len(table[0])):
        table[i] = new_table[i][::-1]


def max_value(table):
    max = -1
    for i in range(len(table[0])):
        for j in range(len(table[0])):
            if table[i][j] != "_" and table[i][j] > max:
                max = table[i][j]
    return max


def check_winning(table, winning_condition):
    if (max_value(table) == winning_condition):
        print("Congratulation! You win!")
        answer = input("Would you like to continue? Y/N ")
        if answer.upper() == "Y":
            return -1
        return 1
    return 0


def move(table, winning_condition):
    repeat = 0
    while True:
        print(max_value(table))
        if repeat != -1:
            repeat = check_winning(table, winning_condition)
            if repeat == 1:
                break
        if not (add_new_number_to_the_table(table) or exist_movement(table)):
            print("Game over")
            break
        os.system("cls")
        print_table(table)
        print("Use the arrow keys for moving the values (or q for quit)")
        input_char = getch()
        if input_char.upper() == b"Q":
            break
        if (input_char != b'\x00'):
            print("Invalid move. Repeat it!")
            continue
        else:
            input_char = getch()
            if input_char == b"H":
                move_up(table)
            elif input_char == b"P":
                move_down(table)
            elif input_char == b"K":
                move_left(table)
            elif input_char == b"M":
                move_right(table)
            else:
                continue


def main():
    dimension_of_the_table = 4
    starting_numbers_count = 1
    winning_condition = 2048
    table = [["_"] * dimension_of_the_table for i in range(dimension_of_the_table)]
    initialize_game(table, starting_numbers_count)
    move(table, winning_condition)


if __name__ == "__main__":
    main()
