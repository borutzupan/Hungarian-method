from asyncio.windows_events import NULL
import numpy as np


def step0(matrix, mark_matrix, row_cov, column_cov, step):
    n = len(matrix[:, 0])
    m = len(matrix[0, :])
    if n > m:
        matrix = np.transpose(matrix)
        mark_matrix = np.transpose(mark_matrix)
        (row_cov, column_cov) = (column_cov, row_cov)
    step = 1
    return matrix, mark_matrix, row_cov, column_cov, step


def step1(matrix, step):
    '''
    For each row of the matrix, find the smallest element and subtract it
    from every element in its row.  Go to Step 2.
    '''
    n = len(matrix[:, 0])
    for i in range(n):
        row = matrix[i]
        min_el = min(row)
        # matrix[i] = list(map(lambda x: x-min_el, row))
        matrix[i] = matrix[i] - min_el
    step = 2
    return matrix, step


def step2(matrix, mark_matrix, step):
    '''
    Find a zero (Z) in the resulting matrix.  If there is no starred zero
    in its row or column, star Z. Repeat for each element in the matrix.
    Go to Step 3.
    '''
    # rows
    n = len(matrix[:, 0])
    # columns
    m = len(matrix[0, :])
    # find a zero
    for i in range(n):
        # if there is no starred zero in its column or row, star it
        if 1 not in mark_matrix[i]:
            for j in range(m):
                if (matrix[i, j] == 0) and (1 not in mark_matrix[:, j]):
                    mark_matrix[i, j] = 1
                    break
    # go to step 3
    step = 3
    return mark_matrix, step


def step3(row_cov, column_cov, mark_matrix, step):
    '''
    Cover each column containing a starred zero.  If K columns are covered,
    the starred zeros describe a complete set of unique assignments.
    In this case, go to Step 7, otherwise, go to Step 4.
    '''
    n = len(row_cov)
    m = len(column_cov)
    k = min(n, m)
    # array of indeces of starred zeroes
    star_zero = np.where(mark_matrix == 1)
    # column indeces of starred zeroes
    star_zero_column = star_zero[1]
    # cover every column that contains a starred zero
    for j in star_zero_column:
        column_cov[j] = 1
    # if there are k columns covered go to final step, step 7
    if sum(column_cov) == k:
        step = 7
    else:
        # if there are < k columns covered go to step 4
        step = 4
    return row_cov, column_cov, step


def find_noncov_zero(matrix, row_cov, column_cov):
    '''
    for step4 we need to find a noncovered zero, which we do with this function
    '''
    n = len(row_cov)
    m = len(column_cov)
    # (row,col) are the coordinates of the noncovered zero
    # if there are no more noncovered zeroes than they are (-1,-1)
    row = -1
    col = -1
    # look thorugh matrix
    for r in range(n):
        for c in range(m):
            # if we find the zero we set the row and col to its coordinates
            # and break the loop for columns
            if (matrix[r, c] == 0 and row_cov[r] == 0 and column_cov[c] == 0):
                row = r
                col = c
                break
        # if we founds the zero we break the loop for rows
        if (row != -1):
            break
    return row, col


def step4(matrix, mark_matrix, row_cov, column_cov, step):
    '''
    Find a noncovered zero and prime it.  If there is no starred zero
    in the row containing this primed zero, go to Step 5.
    Otherwise, cover this row and uncover the column containing the starred
    zero. Continue in this manner until there are no uncovered zeros left.
    Go to Step 6.
    '''
    row = -1
    col = -1
    done = False

    # until there are noncovered zeroes we repeat the process
    while(done is False):
        # find a noncovered zero
        (row, col) = find_noncov_zero(matrix, row_cov, column_cov)
        # if there were none we are done and go to step 6
        if (row == -1):
            done = True
            # go to step 6
            step = 6
        else:
            # else prime the zero
            mark_matrix[row, col] = 2
            # if there is a starred zero in the row containing this
            # primed zero cover this row and uncover the column
            # containing the starred zero
            if 1 in mark_matrix[row, :]:
                # the position of the starred zero
                star = np.where(mark_matrix[row, :] == 1)
                # cover the row
                row_cov[row] = 1
                # uncover the column containing the starred zero
                column_cov[star[0][0]] = 0
            else:
                # if there are no starred zeroes in the row of
                # this primed zero we are done and go to step 5
                done = True
                step = 5
    return row, col, mark_matrix, row_cov, column_cov, step


def fix_mark(path, mark_matrix):
    '''
    Unstar each starred zero of the series, star each primed zero of the
    series.
    '''
    # length of series
    s = len(path[:, 0])

    # Unstar each starred zero of the series
    for j in range(1, s, 2):
        row_idx = path[j, 0]
        col_idx = path[j, 1]
        if ((row_idx != -1) and (col_idx != -1)):
            mark_matrix[row_idx, col_idx] = 0

    # star each primed zero of the series
    for i in range(0, s, 2):
        row_idx = path[i, 0]
        col_idx = path[i, 1]
        if ((row_idx != -1) and (col_idx != -1)):
            mark_matrix[row_idx, col_idx] = 1

    return mark_matrix


def step5(row, col, matrix, mark_matrix, row_cov, column_cov, step):
    '''
    Construct a series of alternating primed and starred zeros as follows.
    Let Z0 represent the uncovered primed zero found in Step 4.
    Let Z1 denote the starred zero in the column of Z0 (if any).
    Let Z2 denote the primed zero in the row of Z1.  Continue until the series
    terminates at a primed zero that has no starred zero in its column.
    Unstar each starred zero of the series, star each primed zero of the
    series, erase all primes and uncover every line in the matrix.
    Return to Step 3.
    '''
    n = len(row_cov)
    m = len(column_cov)
    done = False
    path_count = 1
    path = np.array([[-1, -1]]*(2*m))
    path[path_count - 1, 0] = row
    path[path_count - 1, 1] = col

    while (done is False):
        if 1 in mark_matrix[:, path[path_count - 1, 1]]:
            star_col = np.where(mark_matrix[:, path[path_count - 1, 1]] == 1)
            star_col = star_col[0][0]
            path_count += 1
            path[path_count - 1, 0] = star_col
            path[path_count - 1, 1] = path[path_count - 2, 1]
        else:
            done = True
        if (done is False):
            prime_row = np.where(mark_matrix[path[path_count - 1, 0], :] == 2)
            prime_row = prime_row[0][0]
            path_count += 1
            path[path_count - 1, 0] = path[path_count - 2, 0]
            path[path_count - 1, 1] = prime_row

    # primes -> star, star -> unmarked
    mark_matrix = fix_mark(path, mark_matrix)
    # uncover every line in the matrix
    row_cov[row_cov == 1] = 0
    # erase all primes
    mark_matrix[mark_matrix == 2] = 0
    # return to step 3
    step = 3
    return mark_matrix, row_cov, column_cov, step


def step6(matrix, row_cov, column_cov, step):
    '''
    Find the smallest uncovered value. Add the this value to every element
    of each covered row and subtract it from every element of each uncovered
    column. Return to Step 4 without altering any stars, primes,
    or covered lines.
    '''
    uncovered_row = np.where(row_cov == 0)
    uncovered_row = uncovered_row[0]
    uncovered_col = np.where(column_cov == 0)
    uncovered_col = uncovered_col[0]
    covered_row = np.where(row_cov == 1)
    covered_row = covered_row[0]
    # smallest uncovered value
    min_el = matrix[np.ix_(uncovered_row, uncovered_col)].min()
    for i in covered_row:
        matrix[i, :] = matrix[i, :] + min_el
    for j in uncovered_col:
        matrix[:, j] = matrix[:, j] - min_el
    # return to step 4
    step = 4
    return matrix, step


def hungarian_method(mat, problem):
    # npMatrix = np.random.randint(0, high=10, size=(5, 5))
    if(problem == 'min'):
        cost_matrix = mat
    elif(problem == 'max'):
        # Using the maximum value of the profit_matrix to get the
        # corresponding cost_matrix
        max_value = np.max(mat)
        # Using the cost matrix to find which positions are the answer
        cost_matrix = max_value - mat
    else:
        print('The problem can only be minimum or maximum weight')
    matrix = cost_matrix.copy()
    # the weight of the matching
    weight = 0
    # n vrstic in m stolpcev
    (n, m) = mat.shape
    # mark je matrika kjer bomo oznacevali katere nicle so oznacene z zezdico,
    # katere s crtico 1 ce je nicla z zvezdico, 2 ce je nicla s crtico, 0 sicer
    mark = np.array([[0]*m]*n)
    # seznama, ki povesta katere vrstice oz. stolpci so pokriti
    # 0, ce vrstica oz. stolpec ni pokrit, 1 sicer
    row_cov = np.array([0]*n)
    col_cov = np.array([0]*m)
    # v katerem koraku smo
    step = 0

    done = False
    while(done is False):
        #print('===============================')
        #print(matrix)
        #print('-------------------------------')
        #print(mark)
        #print('-------------------------------')
        #print('row covered: {}'.format(row_cov))
        #print('column covered: {}'.format(col_cov))
        #print('===============================')
        #print('step {}'.format(step))
        if (step == 0):
            (matrix, mark, row_cov, col_cov, step) = step0(matrix, mark, row_cov, col_cov, step)
        elif (step == 1):
            (matrix, step) = step1(matrix, step)
        elif (step == 2):
            (mark, step) = step2(matrix, mark, step)
        elif (step == 3):
            (row_cov, col_cov, step) = step3(row_cov, col_cov, mark, step)
        elif (step == 4):
            (row, col, mark, row_cov, col_cov, step) = step4(matrix, mark, row_cov, col_cov, step)
        elif (step == 5):
            (mark, row_cov, col_cov, step) = step5(row, col, matrix, mark, row_cov, col_cov, step)
        elif (step == 6):
            (matrix, step) = step6(matrix, row_cov, col_cov, step)
        elif (step == 7):
            if (mat.shape == mark.shape):
                weight = mat[mark == 1].sum()
                idx = np.where(mark == 1)
                pairing = list(zip(idx[0], idx[1]))
            #if(problem == 'min'):
                #print(mat)
                #print('pairing: {}'.format(pairing))
                #print('minimum weight of matrix: {}'.format(weight))
            #elif(problem == 'max'):
                #print(mat)
                #print('pairing: {}'.format(pairing))
                #print('maximum weight of matrix: {}'.format(weight))
                done = True
            else:
                mat = np.transpose(mat)
                weight = mat[mark == 1].sum()
                idx = np.where(mark == 1)
                pairing = list(zip(idx[0], idx[1]))
                done = True
    return weight, pairing
