def read_file_content(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def main():
    file_path = input("Enter the path of the file: ")
    try:
        content = read_file_content(file_path)
        print("File content:")
        print(content)
    except FileNotFoundError:
        print("File not found!")


if __name__ == "__main__":
    main()
