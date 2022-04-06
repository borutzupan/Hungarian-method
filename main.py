from asyncio.windows_events import NULL


Matrix = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
matrix_unchanged = Matrix.copy()
# stevilo stolpcev
m = len(Matrix[0])
# stevilo vrstic
n = len(Matrix)
k = min(n,m)

# seznam nicel z zvezdico
star_zero = [None]*n
# seznam nicel s crtico
prime_zero = []


def transpose(matrix):
    matrix_T = [[matrix[j][i] for j in range(n)] for i in range(len(m))]
    return matrix_T


# hocemo zmeraj da je vsaj toliko stolpcev kot vrstic
if n > m:
    Matrix = transpose(Matrix)


def step1(matrix):
    for i in range(n):
        row = matrix[i]
        min_el = min(row)
        matrix[i] = list(map(lambda x: x-min_el, row))
    return matrix


# 0, ce vrstica oz. stolpec ne vsebuje nicle z zvezdico, 1 sicer
row_star = [0]*n
column_star = [0]*m


def step2(matrix, row_star, column_star, star_zero):
    for i in range(n):
        if row_star[i] == 0:
            for j in range(m):
                if (matrix[i][j] == 0) and (column_star[j] == 0):
                    star_zero[i] = j
                    row_star[i] = 1
                    column_star[j] = 1
                    break
    return row_star, column_star


# 0, ce vrstica oz. stolpec ni pokrit, 1 sicer
row_covered = [0]*n
column_covered = [0]*m


def step3(row_lst, column_lst, star_zero):
    row_cov = [0]*n
    column_cov = [0]*m
    for j in star_zero:
        column_cov[j] = 1
    return row_cov, column_cov


def step4(matrix, star_zero, prime_zero, row_star, column_star, row_cov, column_cov):
    for i in range(n):
        for j in range(m):
            if (matrix[i][j] == 0) and ((i, j) not in star_zero):
                prime_zero.append((i, j))
                if row_star[i] == 1:
                    row_cov[i] = 1
                    column_cov[star_zero[i]] = 1
                    min_noncov = 0
                   
    
matrika2 = step1(Matrix)
print(matrika2)
