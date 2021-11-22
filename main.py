# imports
import csv

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
CAPITAL_LETTERS = [letter.upper() for letter in LETTERS]


# function definitions
def help_print() -> None:
    print('compare [dataset] [parameter] [value] [reverse: True, False]: Looks through the dataset and adds all '
          'items where the value of the parameter is greater than or equal to'
          ' (less than or equal to for reverse = True) value to a new dataset, which will be saved as an alias.')
    print('data: prints all datasets in-line.')
    print('help: Displays a list of commands.')
    print('import [alias] [filepath]: Imports the csv file at filepath and saves it to data as alias.')
    print('intersection [dataset1] [dataset2]: Finds the intersection of two datasets.')
    print('print [dataset]: Prints a specific dataset with each element of each data item listed on its own line.')
    print('quit: Exits the program.')
    print('save [dataset] [filepath]: Saves the specified dataset to a file at filepath, which should be a full,'
          ' complete directory to which this program has write access.')
    print('sort [dataset] [parameter] [reverse]: Sorts the dataset by parameter; sorts by reverse if reverse is True.')
    print('union [dataset1] [dataset2]: Finds the union of two datasets.')


def determine_type(element) -> str:
    if type(element) is float:
        return 'float'
    elif type(element) is int:
        return 'int'
    elif type(element) is str:
        try:
            int(element)
            return 'int'
        except ValueError:
            try:
                float(element)
                return 'float'
            except ValueError:
                return 'str'


def parameter_check(expected, actual):
    if expected == actual:
        return True
    else:
        print('Expected %d parameters but got %d instead.' % (expected, actual))
        return False


def data_maker(alias: str, file_data) -> None:
    keys = []
    lines = []

    for line_0 in file_data:
        for key in line_0:
            for letter in key:
                if letter not in LETTERS and letter not in CAPITAL_LETTERS:
                    key = key.removeprefix(letter)
            keys.append(key.lower())
        break

    for line in file_data:
        values = {}
        for index, value in enumerate(line):
            values[keys[index]] = value
        lines.append(values)

    data[alias] = lines


def import_csv(alias: str, filepath: str) -> None:
    data_maker(alias, csv.reader(open(filepath, 'r'), delimiter=','))


def sort_data(dataset: str, parameter, reverse) -> list:
    # we need to CLONE data[dataset], not alias it!
    temp_list = data[dataset][:]
    sort_type = determine_type(temp_list[0][parameter])

    for i in range(len(temp_list) - 1):
        # for remaining elements
        for j in range(len(temp_list) - 1 - i):
            # if need to be swapped
            if eval('%s(temp_list[j][parameter]) < %s(temp_list[j + 1][parameter])'
                    % (sort_type, sort_type)) and not reverse or \
                    eval('%s(temp_list[j][parameter]) < %s(temp_list[j + 1][parameter])'
                         % (sort_type, sort_type)) and reverse:

                # Swap
                temp_list[j], temp_list[j + 1] = temp_list[j + 1], temp_list[j]

    return temp_list


def save_file(dataset: str, location: str) -> None:
    file_save = open(location, mode='w')
    for dictionary in data[dataset]:
        line = ''
        for key in dictionary.keys():
            line += ('%s,' % dictionary[key])
        line += '\n'
        line = line.replace(',\n', '\n')
        file_save.write(line)
    file_save.close()


# noinspection PyUnusedLocal
def compare_data(dataset: str, parameter: str, value: str | int | float, reverse: str) -> list:
    # need to CLONE data[dataset], not alias it!
    new_list = []

    # determine type
    compare_type = determine_type(data[dataset][0][parameter])
    value = eval('%s(value)' % compare_type)

    # run comparison
    for index, item in enumerate(data[dataset]):
        if eval('%s(item[parameter]) <= value and not reverse or %s(item[parameter]) >= value and reverse' %
                (compare_type, compare_type)):
            new_list.append(item)

    return new_list


def combine_lists(dataset_1: str, dataset_2: str, operation):
    new_list = []

    if operation:
        # intersection
        if data[dataset_1] == [] or data[dataset_2] == []:
            return []

        for item in data[dataset_1]:
            if item in data[dataset_2] and item not in new_list:
                new_list.append(item)

    else:
        # union
        if not data[dataset_1]:
            return data[dataset_2]

        elif not data[dataset_2]:
            return data[dataset_1]

        for item in data[dataset_1]:
            if item not in new_list:
                new_list.append(item)

        for item in data[dataset_2]:
            if item not in new_list:
                new_list.append(item)

    return new_list


def data_print() -> None:
    for dataset in data.keys():
        print('%s:' % dataset)
        print(data[dataset])


def dataset_print(dataset):
    print('%s:' % dataset)
    for item in data[dataset]:
        print()
        for key in item.keys():
            print('%s: %s' % (key, item[key]))


# startup
data = {}
commands = []
print('Welcome to CSV Analyzer. Enter a command or type help for a list of commands')


# main command line interface
def main() -> None:
    while True:
        command = input('> ')
        commands.insert(0, command)
        command = command.split(' ')

        match command[0]:
            case 'compare':
                if parameter_check(4, len(command) - 1):
                    new_dataset = compare_data(command[1], command[2], command[3], command[4])
                    print(new_dataset)
                    save_as = input('Input an alias to save the compared data as, or None to not save it: ')
                    if save_as.lower() != 'none':
                        data[save_as] = new_dataset

            case 'data':
                data_print()

            case 'help':
                help_print()

            case 'import':
                if parameter_check(2, len(command) - 1):
                    import_csv(command[1], command[2])
                    print('CSV file successfully imported.')

            case 'intersection':
                if parameter_check(2, len(command) - 1):
                    combined_list = combine_lists(command[1], command[2], True)
                    print(combined_list)
                    save_as = input('Input an alias to save the intersection as, or None to not save it: ')
                    if save_as.lower() != 'none':
                        data[save_as] = combined_list

            case 'print':
                if parameter_check(1, len(command) - 1):
                    dataset_print(command[1])

            case 'quit':
                print('Thank you for using this program.')
                break

            case 'save':
                if parameter_check(2, len(command) - 1):
                    save_file(command[1], command[2])

            case 'sort':
                if parameter_check(3, len(command) - 1):
                    new_dataset = sort_data(command[1], command[2], command[3])
                    print(new_dataset)
                    save_as = input('Input an alias to save the sorted data as, or None to not save it: ')
                    if save_as.lower() != 'none':
                        data[save_as] = new_dataset

            case 'union':
                if parameter_check(2, len(command) - 1):
                    combined_list = combine_lists(command[1], command[2], True)
                    print(combined_list)
                    save_as = input('Input an alias to save the union as, or None to not save it: ')
                    if save_as.lower() != 'none':
                        data[save_as] = combined_list

            case _:
                print('Error: Command not recognized.')

    print('Program exited successfully')


if __name__ == '__main__':
    main()
