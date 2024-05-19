def read_file_content(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines


def main():
    file_path = input("Enter the path of the file: ")
    try:
        lines = read_file_content(file_path)
        print("File content:")
        for line in lines:
            print(line, end="")
    except FileNotFoundError:
        print("File not found!")


if __name__ == "__main__":
    main()
