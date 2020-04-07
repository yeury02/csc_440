import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):

    def naive_alg(self, row, col):
        #base case: bottom row
            # return energy(i,j)
        #recursion: in the middle
            #return energy(i,j) + min(seam energies of three pixels under i, j)

        # 2 edge cases:
            # first colum
            # last colum

        # base case
        # check that I am at the last row
        if row == self.height - 1:
            # print(row)
            # print(self.height - 1)
            return self.energy(row,col)
        # edge case
        # check first column
        elif col == 0:
            # print('first col')
            return self.energy(row, col) + min(self.naive_alg(row+1, col), self.naive_alg(row+1, col+1))
        
        # edge case
        # check that I am at the last colum
        elif col == self.width - 1:
            # print('last columns')
            return self.energy(row, col) + min(self.naive_alg(row+1, col-1), self.naive_alg(row+1, col))

        # recursion approach
        else:
            # print('recursion')
            return self.energy(row,col) + min(self.naive_alg(row+1, col-1), self.naive_alg(row+1, col), self.naive_alg(row+1, col+1))

    def best_seam(self, dp=True):

        if dp == False:
            self.naive_alg(0,0)
        # raise NotImplemented

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())

# obj = ResizeableImage('sunset_small.png')
# obj.best_seam()