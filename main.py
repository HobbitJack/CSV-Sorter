"""Program which can analyse and sort .csv files"""
# imports
import csv

LETTERS = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
CAPITAL_LETTERS = [letter.upper() for letter in LETTERS]


# function definitions
def help_print() -> None:
    """Print the help for each function into the console
    :rtype: None
    """
    print(
        "compare [dataset] [parameter] [value] [reverse: True, False]:"
        " Looks through the dataset and adds all "
        "items where the value of the parameter is greater than or equal to"
        " (less than or equal to for reverse = True) "
        "value to a new dataset, which will be saved as an alias."
    )
    print("data: prints all datasets in-line.")
    print("help: Displays a list of commands.")
    print(
        "import [alias] [filepath]: Imports the csv file"
        " at filepath and saves it to data as alias."
    )
    print("intersection [dataset1] [dataset2]: Finds the intersection of two datasets.")
    print(
        "print [dataset]: Prints a specific dataset with each element of each data item "
        "listed on its own line."
    )
    print("quit: Exits the program.")
    print(
        "save [dataset] [filepath]: Saves the specified dataset to a "
        "file at filepath, which should be a full,"
        " complete directory to which this program has write access."
    )
    print(
        "sort [dataset] [parameter] [reverse]: Sorts the dataset by"
        " parameter; sorts by reverse if reverse is True."
    )
    print("union [dataset1] [dataset2]: Finds the union of two datasets.")


def determine_type(element: object) -> str:
    """Return the type of the inputted element for use in sorting

    :param element: element to find the type of
    :rtype: str
    :return: type of the element as a string
    """
    if isinstance(element, float):
        return "float"
    elif isinstance(element, int):
        return "int"
    elif isinstance(element, str):
        try:
            int(element)
            return "int"
        except ValueError:
            try:
                float(element)
                return "float"
            except ValueError:
                return "str"


def type_convert(convert_type: str, convert_object: str):
    """Convert convert_object to type convert_type

    :param convert_type: type to convert convert_object to
    :param convert_object: object to convert into type convert_type
    :raises ValueError: if convert_type is not 'int', 'float' or 'str'
    :rtype: object
    :return: Type-converted version of convert_object
    """
    if convert_type == "int":
        return int(convert_object)
    elif convert_type == "float":
        return float(convert_object)
    elif convert_type == "str":
        return str(convert_object)
    else:
        raise ValueError


def parameter_check(expected: int, actual: int) -> bool:
    """Return a bool as to whether the command received the expected number of parameters or not

    :param expected: The expected number of parameters to pass to the function
    :param actual: The actual number of parameters entered by the function
    :rtype: bool
    :return: Whether or not the number of parameters entered is the number expected
    """
    if expected == actual:
        return True
    else:
        print(f"Expected {expected} parameters but got {actual} instead.")
        return False


def data_maker(alias: str, file_data: csv.reader) -> None:
    """Create a new dictionary holding inputted .csv data

    :param alias: Alias to save the data as
    :param file_data: csv.reader iterable containing the read-in file data
    :rtype: None
    :return: Nothing
    """
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
    """Import a .csv file. Wrapper for data_maker()

    :param alias: Alias to save the inputted data as; human readable + typeable
    :param filepath: Filepath to .csv file to input
    :rtype: None
    :return: Nothing
    """
    with open(filepath, "r", encoding="utf8") as file:
        data_maker(alias, csv.reader(file, delimiter=","))


def sort_data(dataset: str, parameter: str, reverse: str) -> list:
    """Sort the list by parameter, and reverse sort if reverse is True

    :param dataset: The dataset to sort
    :param parameter: The parameter by which to sort
    :param reverse: Will place the largest item at the start instead of end
    :rtype: list
    :return: List sorted by parameter
    """
    # we need to CLONE data[dataset], not alias it!
    temp_list = data[dataset][:]
    sort_type = determine_type(temp_list[0][parameter])

    for i in range(len(temp_list) - 1):
        # for remaining elements
        for j in range(len(temp_list) - 1 - i):
            # if need to be swapped
            if (
                type_convert(sort_type, temp_list[j][parameter])
                < type_convert(sort_type, temp_list[j + 1][parameter])
                and not reverse
                or type_convert(sort_type, temp_list[j][parameter])
                > type_convert(sort_type, temp_list[j + 1][parameter])
                and reverse
            ):

                # Swap
                temp_list[j], temp_list[j + 1] = temp_list[j + 1], temp_list[j]

    return temp_list


def save_file(dataset: str, location: str) -> None:
    """Save a particular dataset as a new .csv file

    :param dataset: The dataset to save
    :param location: The full filepath of the save location
    :rtype: None
    :return: Nothing
    """
    with open(location, mode="w", encoding="utf8") as file_save:

        line = ""
        for key in data[dataset][0].keys():
            line += f"{key},"
        line += "\n"
        line = line.replace(",\n", "\n")
        file_save.write(line)

        for data_item in data[dataset]:
            line = ""
            for item in data_item.items():
                line += f"{item[1]},"
            line += "\n"
            line = line.replace(",\n", "\n")
            file_save.write(line)


def compare_data(
    dataset: str, parameter: str, value: str | int | float, reverse: str
) -> list:
    """Save only the elements which are greater than/less than or equal to the inputted value

    :param dataset: The dataset to look at
    :param parameter: The parameter to compare from
    :param value: The value to compare to
    :param reverse: Whether to do greater than or less than
    :rtype: list
    :return: A new list which has only the elements which passed the compare with value
    """
    # need to CLONE data[dataset], not alias it!
    new_list = []

    # determine type
    compare_type = determine_type(data[dataset][0][parameter])
    value = type_convert(compare_type, value)

    # run comparison
    for item in data[dataset]:
        if (
            type_convert(compare_type, item[parameter]) <= value
            and not reverse
            or type_convert(compare_type, item[parameter]) >= value
            and reverse
        ):
            new_list.append(item)

    return new_list


def combine_lists(dataset_1: str, dataset_2: str, operation: bool) -> list:
    """Combine two lists by a union or intersection

    :param dataset_1: The first dataset to look at
    :param dataset_2: The second dataset to look at
    :param operation: True -> Intersection; False -> Union
    :rtype: list
    :return: A new list made by combining the inputted lists through the given operation
    """
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
    """Print inline all current datasets

    :rtype: None
    :return: Nothing
    """
    for item in data.items():
        print(f"{item[0]}:\n{item[1]}")


def dataset_print(dataset: str) -> None:
    """Pretty-print all elements of a particular dataset

    :param dataset:
    :rtype: None
    :return: Nothing
    """
    print(f"{dataset}:")
    for item in data[dataset]:
        print()
        for key in item.keys():
            print(f"{key}: {item[key]}")


# startup
data = {}
commands = []
print("Welcome to CSV Analyzer. Enter a command or type help for a list of commands")


# main command line interface
def main() -> None:
    """Main program loop
    :rtype: None
    :return: Nothing
    """

    while True:
        command = input("> ")
        commands.insert(0, command)
        command = command.split(" ")

        match command[0]:
            case "compare":
                if parameter_check(4, len(command) - 1):
                    new_dataset = compare_data(
                        command[1], command[2], command[3], command[4]
                    )
                    print(new_dataset)
                    save_as = input(
                        "Input an alias to save the compared "
                        "data as, or None to not save it: "
                    )
                    if save_as.lower() != "none":
                        data[save_as] = new_dataset

            case "data":
                data_print()

            case "help":
                help_print()

            case "import":
                if parameter_check(2, len(command) - 1):
                    import_csv(command[1], command[2])
                    print("CSV file successfully imported.")

            case "intersection":
                if parameter_check(2, len(command) - 1):
                    combined_list = combine_lists(command[1], command[2], True)
                    print(combined_list)
                    save_as = input(
                        "Input an alias to save the intersection"
                        " as, or None to not save it: "
                    )
                    if save_as.lower() != "none":
                        data[save_as] = combined_list

            case "print":
                if parameter_check(1, len(command) - 1):
                    dataset_print(command[1])

            case "quit":
                print("Thank you for using this program.")
                break

            case "save":
                if parameter_check(2, len(command) - 1):
                    save_file(command[1], command[2])
                    print("File saved successfully.")

            case "sort":
                if parameter_check(3, len(command) - 1):
                    new_dataset = sort_data(command[1], command[2], command[3])
                    print(new_dataset)
                    save_as = input(
                        "Input an alias to save the sorted data as,"
                        " or None to not save it: "
                    )
                    if save_as.lower() != "none":
                        data[save_as] = new_dataset

            case "union":
                if parameter_check(2, len(command) - 1):
                    combined_list = combine_lists(command[1], command[2], True)
                    print(combined_list)
                    save_as = input(
                        "Input an alias to save the union as, or None to not save it: "
                    )
                    if save_as.lower() != "none":
                        data[save_as] = combined_list

            case _:
                print("Error: Command not recognized.")

    print("Program exited successfully")


if __name__ == "__main__":
    main()
