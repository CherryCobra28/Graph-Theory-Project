import numba
import numpy as np

@numba.njit
def square_matrix(matrix):
    # Get the number of rows and columns in the matrix
    rows, cols = matrix.shape
    # Create a new matrix to store the result
    result = np.empty((rows, cols))
    # Iterate over the rows and columns of the matrix
    for i in range(rows):
        for j in range(cols):
            # Square each element of the matrix and store it in the result
            result[i, j] = matrix[i, j] ** 2
    return result

# Test the function
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(square_matrix(matrix))