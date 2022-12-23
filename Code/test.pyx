# Import the necessary C libraries
cimport numpy as np
import numpy as np

def raise_matrix(double[:, :] A):
    # Create a copy of the matrix
    cdef double[:, :] B = np.copy(A)
    cdef int n = A.shape[0]
    cdef int m = A.shape[1]

    # Raise the matrix to a power until all entries are positive
    cdef int i, j, k
    while True:
        for i in range(n):
            for j in range(m):
                if B[i, j] <= 0:
                    break
        else:
            return B

        # Compute the matrix product
        for i in range(n):
            for j in range(m):
                B[i, j] = 0
                for k in range(m):
                    B[i, j] += A[i, k] * A[k, j]

# Test the function
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(raise_matrix(A))
