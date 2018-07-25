import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I
    
def dot_product(vector_one, vector_two):
        elements = []
        for i in range(len(vector_one)):
            elements.append(vector_one[i] * vector_two[i])
        return sum(elements)

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a square Matrix.
        Modified, recursive version to also handle matrices larger than 2x2
        """
        if not self.is_square():
            raise ValueError("Cannot calculate determinant of non-square matrix.")
        
        det = 0
        
        #Exit cases for recursion with 1x1 and 2x2 matrices, otherwise else statement calls function again
        if self.h == 1:
            det = self[0][0]
        elif self.h == 2:
            a = self[0][0]
            b = self[0][1]
            c = self[1][0]
            d = self[1][1]
            det = a*d - b*c
        else:
            for first_row_column in range(self.w):
                #construct matrix excluding top row and current column
                temp = []
                for row in range(1, self.h): #start at 1 to skip top row
                    row_temp = []
                    for column in range(self.w):
                        if not column == first_row_column:
                            row_temp.append(self[row][column])
                    temp.append(row_temp)
                
                smaller_matrix = Matrix(temp)
                #Calculate determinant recursively
                #-1 raised to the power of the current column determines sign of determinant
                det += math.pow(-1, first_row_column) * self[0][first_row_column] * smaller_matrix.determinant()        
                
        return det
    
    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise ValueError("Cannot calculate the trace of a non-square matrix.")
        
        tr = 0
        for i in range(self.h):
            tr += self[i][i]
        return tr

    def inverse(self):
        """
        Calculates the inverse of a square Matrix.
        """
        if not self.is_square():
            raise ValueError("Non-square Matrix does not have an inverse.")
        
        det = self.determinant()
        if det == 0.:
            raise ValueError("This matrix does not have an inverse (determinant is zero).")
        
        if self.h == 1:
            inverse = Matrix([
                [1/self[0][0]]
            ])
        elif self.h == 2:
            inverse = Matrix([
                [self[1][1] / det, -self[0][1] / det],
                [-self[1][0] / det, self[0][0] / det],
            ])
        else: # Utilize row reduction method to find inverse
            # Create identity matrix of identical size, and append to right side of matrix to invert
            I = identity(self.h)
            to_reduce = []
            for row in range(self.h):
                to_reduce_row = []
                for column in range(self.w):
                    to_reduce_row.append(self[row][column])
                for identity_column in range(I.w):
                    to_reduce_row.append(I[row][identity_column])
                to_reduce.append(to_reduce_row)
            to_reduce = Matrix(to_reduce)
            
            # Reduce this matrix to reduced row echelon form; second half of the matrix will be inverse
            to_reduce.rref()
            
            # Isolate second half of matrix and return
            inverse = []
            for row in range(to_reduce.h):
                inverse_row = []
                for column in range(self.w, to_reduce.w):
                    inverse_row.append(to_reduce[row][column])
                inverse.append(inverse_row)
            inverse = Matrix(inverse)
            
        return inverse
    
    def rref(self):
        """
        Returns a reduced row echelon form of this Matrix.
        """
        
        # Algorithm for row reduction:
            # 1) Swap rows to make sure pivotal 1 exists
            # 2) Divide entire row to create pivotal 1
            # 3) Subtract values in current row from other rows
            # 4) Repeat until all rows contain pivotal 1s
        
        counter = 0
        while counter < self.h:
            if self[counter][counter] == 0:
                self.rref_swap(counter)
            elif self[counter][counter] != 1:
                self.rref_divide(counter)
            else:
                self.rref_subtract(counter)
                counter += 1
        
        return self
    
    def rref_swap(self, pivot):
        """
        Returns the matrix with rows swapped so that the leftmost column that
        is not all zeroes has a nonzero entry in the current row
        """
        
        temp = []
        for column in range(self.w):
            temp.append(self[pivot][column])
        
        for current_row in range(pivot+1, self.h):
            if self[current_row][pivot] != 0:
                for current_column in range(self.w):
                    self[pivot][current_column] = self[current_row][current_column]
                    self[current_row][current_column] = temp[current_column]
                break
        
        return self
    
    def rref_divide(self, pivot):
        """
        Returns the matrix with rows divided by entry to get a pivotal 1
        """
        div = self[pivot][pivot]
        for column in range(self.w):
            self[pivot][column] /= div
        
        return self
    
    def rref_subtract(self, pivot):
        """
        Returns the matrix with multiples of the current row subtracted from
        other rows to clear out rest of the columns
        """
        current_row = 0
        while current_row < self.h:
            if current_row == pivot:
                current_row += 1
            else:
                multiplier = self[current_row][pivot]
                for current_column in range(self.w):
                    self[current_row][current_column] -= multiplier * self[pivot][current_column]
                current_row += 1
        return self

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        transpose = []
        for column in range(self.w):
            row_transpose = []
            for row in range(self.h):
                row_transpose.append(self[row][column])
            transpose.append(row_transpose)
        return Matrix(transpose)  

    def is_square(self):
        return self.h == self.w
    
    

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise ValueError("Matrices can only be added if the dimensions are the same") 
        
        matrixSum = []
        for row in range(self.h):
            current_row = []
            for column in range(self.w):
                current_row.append(self[row][column] + other[row][column])
            matrixSum.append(current_row)
        return Matrix(matrixSum)

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        negative = []
        for row in range(self.h):
            current_row = []
            for column in range(self.w):
                current_row.append(-1 * self[row][column])
            negative.append(current_row)
        return Matrix(negative)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        matrixDif = []
        for row in range(self.h):
            current_row = []
            for column in range(self.w):
                current_row.append(self[row][column] - other[row][column])
            matrixDif.append(current_row)
        return Matrix(matrixDif)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        product = []
        transpose_other = other.T()
        
        for row in range(self.h):
            row_product = []
            for column in range(transpose_other.h):
                row_product.append(dot_product(self[row], transpose_other[column]))
            product.append(row_product)
        return Matrix(product)
            

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        
        if isinstance(other, numbers.Number):
            rproduct = []
            for row in range(self.h):
                row_rproduct = []
                for column in range(self.w):
                    row_rproduct.append(self[row][column] * other)
                rproduct.append(row_rproduct)
            return Matrix(rproduct)