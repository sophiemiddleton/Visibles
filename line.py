def add_line_to_file(filename, line_to_add):
    """Adds a line to the end of a file.

    Args:
        filename: The path to the file.
        line_to_add: The line to add to the file.
    """
    with open(filename, "a") as file:
        file.write(line_to_add + "\n")

def main() :
    # Example usage
    filename = "m50_prima.lhe"
    line_to_add = "</LesHouchesEvents>"
    add_line_to_file(filename, line_to_add)
if __name__ == "__main__":
    main()
