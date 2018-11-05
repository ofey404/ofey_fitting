import sys
sys.path.append('../')
from parse_outcar import my_grep, parse_matrix
from scipy.constants import k, h, N_A
from math import sqrt, pi


def load_data():
    def elastic():
        lines_with_matrix_list = my_grep(grep_lines,
                                         ["ELASTIC"],
                                         exception_list=["SYMMETRIZED", "CONTR", "TOTAL"],
                                         line_numbers=10)
        # print("this is the matrix grepped for transformation")
        # for part in lines_with_matrix_list:
        #     for line in part:
        #         print(line)

        # print("the matrix transformationed")
        # for lines_list in lines_with_matrix_list:
        #     print(parse_matrix(lines_list))

        return parse_matrix(lines_with_matrix_list[0])

    def pomass():
        pomass_matrix_list = my_grep(grep_lines,
                                     ["POMASS"],
                                     exception_list=["ZVAL"],
                                     line_numbers=1)

        return parse_matrix(pomass_matrix_list[0])[0]

    def volume():
        volume_matrix_list = my_grep(grep_lines,
                                     ["volume"],
                                     line_numbers=1)
        return parse_matrix(volume_matrix_list[-1])[0][0]

    with open("data/OUTCAR", "rt") as file:
        grep_lines = file.readlines()

    return elastic(), pomass(), volume()


def main():
    elastic_matrix, pomass, volume = load_data()
    # pomass_mo, pomass_s = pomass
    number_of_atoms = [1, 2]

    bulk_modulus = (
        (elastic_matrix[0][0]+elastic_matrix[1][1]+elastic_matrix[2][2])/9
        + (elastic_matrix[0][1]+elastic_matrix[1][2]+elastic_matrix[2][0])*(2/9)
    )
    bulk_modulus = bulk_modulus / 10  # 单位转换，KBa->GBa

    shear_modulus = (
        (elastic_matrix[0][0]+elastic_matrix[1][1]+elastic_matrix[2][2])/15
        + (elastic_matrix[0][1]+elastic_matrix[1][2]+elastic_matrix[2][0])*(-1/15)
        + (elastic_matrix[3][3]+elastic_matrix[4][4]+elastic_matrix[5][5])
    )
    shear_modulus = shear_modulus / 10  # 单位转换，KBa->GBa

    density = (sum([m*n for m, n in zip(pomass, number_of_atoms)])
               / (volume * N_A))  # 单位为g/A^3

    vl = sqrt((3*bulk_modulus + 4*shear_modulus)/(3*density))  # v longitudinal
    vt = sqrt(shear_modulus/density)  # v transverse

    vm = ((2/(vt**3) + 1/(vl**3))/3)**(-1/3)

    theta_d = (h/2*pi) / k * (3*sum(number_of_atoms)/4*pi*volume)**(1/3) * vm

    return theta_d


if __name__ == "__main__":
    print(main())
