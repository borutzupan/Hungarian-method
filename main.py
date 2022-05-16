from asyncio.windows_events import NULL
import numpy as np


Matrix = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
npMatrix = np.array(Matrix)
matrix_unchanged = Matrix.copy()
# n vrstic in m stolpcev
(n, m) = npMatrix.shape
k = min(n, m)

# seznam nicel z zvezdico
star_zero = [None]*n
# npMark je matrika kjer bomo oznacevali katere nicle so oznacene z zezdico, katere s crtico
# 1 ce je nicla z zvezdico, 2 ce je nicla s crtico, 0 sicer
npMark = np.array([[0]*m]*n)
# seznam nicel s crtico
prime_zero = []

# v katerem koraku smo
step = 0


# hocemo zmeraj da je vsaj toliko stolpcev kot vrstic
def step0(matrix, step):
    if n > m:
        matrix = np.transpose(matrix)
    step = 1
    return matrix, step


def step1(matrix, step):
    # for each row find the smallest element and subtract it from
    # every element in its row
    for i in range(n):
        row = matrix[i]
        min_el = min(row)
        matrix[i] = list(map(lambda x: x-min_el, row))
    step = 2
    return matrix, step


def step2(matrix, mark_matrix, step):
    # find a zero
    for i in range(n):
        # if there is no starred zero in its column or row, star it
        if 1 not in mark_matrix[i]:
            for j in range(m):
                if (matrix[i, j] == 0) and (1 not in mark_matrix[:,j]):
                    mark_matrix[i, j] = 1
                    break
    # go to step 3
    step = 3
    return mark_matrix, step


# seznama, ki povesta katere vrstice oz. stolpci so pokriti
# 0, ce vrstica oz. stolpec ni pokrit, 1 sicer
row_covered = np.array([0]*n)
column_covered = np.array([0]*m)


# Pokrij vsak stolpec, ki vsebuje niclo z zvezdico
def step3(row_cov, column_cov, mark_matrix, step):
    # array of indeces of starred zeroes
    star_zero = np.where(mark_matrix == 1)
    # column indeces of starred zeroes
    star_zero_column = star_zero[1]
    # cover every column that contains a starred zero
    for j in star_zero_column:
        column_cov[j] = 1
    # if there are k columns covered go to final step, step 7
    if len(column_cov) == k:
        step = 7
    else:
        # if there are < k columns covered go to step 4
        step = 4
    return row_cov, column_cov, step


def step4(matrix, mark_matrix, row_cov, column_cov, step): # ŠE NI VREDU!!!!!!!!!!!!!!!
    # do this until there are no uncovered zeroes left!!!!!!!!!!!!
    # find a noncovered zero
    for i in range(n):
        for j in range(m):
            if column_cov[j] == 0:
                if (matrix[i, j] == 0) and (mark_matrix[i, j] != 1):
                    # prime it
                    mark_matrix[i, j] = 2
                    # if there is a starred zero in the row containing this primed zero
                    # cover this row and uncover the column containing the starred zero
                    if 1 in mark_matrix[i, :]:
                        # the position of the starred zero
                        star = np.where(mark_matrix[i, :] == 1)
                        # cover the row
                        row_cov[i] = 1
                        # uncover the column containing the starred zero
                        column_cov[star[0][0]] = 0
                    else:
                        # if there is no starred zero in the row containing this primed zero,
                        # go to step 5
                        step = 5
    # we need to know which columns and row are uncovered to get the smallest
    # element uot of the submatrix of uncovered rows and columns
    uncovered_col = np.where(column_cov == 0)
    uncovered_col = uncovered_col[0]
    uncovered_row = np.where(row_cov == 0)
    uncovered_row = uncovered_row[0]
    # smallest uncovered value
    min_el = matrix[np.ix_(uncovered_row, uncovered_col)].min()
    # go to step 6
    step = 6
    return mark_matrix, row_cov, column_cov, min_el, step


def step6(matrix, mark_matrix, row_cov, column_cov, min_el, step):
    # add the value found in step 4 to every elemenet of each covered row and
    # subtract it from every element of each uncovered column.
    covered_row = np.where(row_cov == 1)
    covered_row = covered_row[0]
    uncovered_col = np.where(column_cov == 0)
    uncovered_col = uncovered_col[0]
    for i in covered_row:
        matrix[i, :] += min_el
    for j in uncovered_col:
        matrix[:, j] -= min_el
    # return to step 4
    step = 4
    return matrix, step


