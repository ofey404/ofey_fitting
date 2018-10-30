import os
import sys


# ------------------- function about parse a matrix from lines ----------------


def is_element(word):
    try:
        float(word)
    except ValueError:
        return False
    return True


def turn_word_to_element(word):
    return float(word)


def is_line(line):
    """Args: a single line splited by space or \n
    Returns: if is a 'line of matrix', return True"""
    words_list = line.split()
    for word in words_list:
        if is_element(word):
            return True
    return False


def parse_matrix(lines_list,
                 is_line=is_line,
                 is_element=is_element,
                 turn_word_to_element=turn_word_to_element):
    """Args: lines contains a matrix, more than 2 will be rejected
    Returns: the matrix"""

    def find_lines_contain_matrix(lines_list):
        """TODO: capture errors"""
        lines_contain_matrix = []

        for line in lines_list:
            if is_line(line):
                lines_contain_matrix.append(line)

        return lines_contain_matrix

    def parse_matrix_from_lines(lines_contain_matrix):
        """Args: output of function find_lines_contain_matrix
        Returns: the matrix"""
        def get_begin_and_end_of_line(words_list):
            """Args: words list splited from a line contains matrix
            Returns:
              a tuple, (begin index, end index + 1)
              line[result[0]: result[1]] = all elements contains the matrix
            """
            begin, end = None, None
            for index, word in enumerate(words_list):
                if is_element(word):
                    if begin is None:
                        begin = index
                    elif end is not None and begin is not None:
                        raise Exception("elements are not consistant")
                else:
                    if (end is None) and (begin is not None):
                        end = index

            return (begin, end)

        result = []
        temp_begin_and_end = None
        for line in lines_contain_matrix:
            words_list = line.split()
            if temp_begin_and_end is None:
                temp_begin_and_end = get_begin_and_end_of_line(words_list)
            else:
                if temp_begin_and_end != get_begin_and_end_of_line(words_list):
                    raise Exception("length of lines are not all the same")
            begin, end = get_begin_and_end_of_line(words_list)
            result.append(
                [turn_word_to_element(word)
                 for word in words_list[begin: end]])

        return result

    """-------------------- the body of function ---------------------"""

    return parse_matrix_from_lines(find_lines_contain_matrix(lines_list))


# --------------------------- end ----------------------------------------


# --------------------------- functions about mygrep ----------------------


def line_contain_kwd(line, kwd):
    """Args: a str input from OUTCAR
    Returns: boolean value of kwd exist or not"""
    if line.find(kwd) != -1:
        return True
    else:
        return False


def file_filter(outcar_path, kwds_list):
    """Args:
      outcar_path: path of OUTCAR File
      kwds_list: keywords list for search
    Returns:
      a dict whose keys are keywords, values are list of lines contain that kwd."""
    values = dict.fromkeys(kwds_list, None)
    print(values)

    with open(outcar_path, "rt") as file:
        while 1:
            line = file.readline()
            if not line:
                break
            for kwd in kwds_list:
                if line_contain_kwd(line, kwd):
                    if values[kwd] is None:
                        values[kwd] = [line]
                    else:
                        values[kwd].append(line)

    return values


def my_grep(file_object, kwd_list, exception_list=None, line_numbers=1):
    """Args:
      file_object: file object of file you want to manage
      kwds_list: keyword
      exception_list: exceptions
      line_numbers: get line numbers after find a filted line, if another filted line appeared, recount.
    Returns:
      [[matched line 1, ...(<line_numbers> lines), ...], [matched line 2, ... ], ...]
    """
    def is_target(line):
        flag = False
        for kwd in kwd_list:
            if line_contain_kwd(line, kwd):
                flag = True
                break
        if exception_list is not None:
            for exc in exception_list:
                if line_contain_kwd(line, exc):
                    flag = False
                    break

        return flag

    result = []
    count = 0
    temp = []

    while 1:
        line = file_object.readline()
        if not line:
            break
        if is_target(line):
            if count != 0:
                # another filted line appeared before get all line numbers
                result.append(temp)
                count = line_numbers - 1
            else:
                temp.append(line)
                count = line_numbers - 1
        elif count != 0:
            temp.append(line)
            count -= 1
            if count == 0:
                result.append(temp)
                temp = []

        # if line_contain_kwd(line, kwd) and count == 0:
        #     count = line_numbers
        # if count != 0:
        #     temp.append(line)
        #     count -= 1
        #     if count == 0:
        #         result.append(temp)
        #         temp = []

    return result


# ---------------------------- end --------------------------------


def main():
    with open("data/OUTCAR", "rt") as file:
        # l = my_grep(file,
        #             ["ELASTIC"],
        #             exception_list=["SYMMETRIZED", "CONTR", "TOTAL"],
        #             line_numbers=10)
        m = my_grep(file, ["volume"], line_numbers = 1)
        # for lines in l:
        #     for line in lines:
        #         print(line)
        # print(parse_matrix(l[0]))
        for line in m[0]:
            print(line)

if __name__ == "__main__":
    main()
