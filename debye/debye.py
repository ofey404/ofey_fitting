import vaspy
import parse_outcar

def main():
    with open("data/OUTCAR", "rt") as file:
        print(
            parse_outcar.my_grep(file, ["volume"]))

if __name__ == "__main__":
    main()
