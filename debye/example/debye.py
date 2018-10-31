import sys
sys.path.append('../')

from parse_outcar import my_grep, parse_matrix


def main():
    with open("data/OUTCAR", "rt") as file:
        grep_lines = file.readlines()

    # transform some data into a matrix
    lines_with_matrix_list = my_grep(grep_lines,
                                     ["ELASTIC"],
                                     exception_list=["SYMMETRIZED", "CONTR", "TOTAL"],
                                     line_numbers=10)

    print("this is the matrix grepped for transformation")
    for part in lines_with_matrix_list:
        for line in part:
            print(line)

    print("the matrix transformationed")
    for lines_list in lines_with_matrix_list:
        print(parse_matrix(lines_list))


if __name__ == "__main__":
    main()
