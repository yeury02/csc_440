import imagematrix
import time

class ResizeableImage(imagematrix.ImageMatrix):

    best_path = []
    best_seams = {}
    def best_seam(self, dp=True):
        # calculate all energies
        energy_memo = {}
        for col in range(self.width):
            for row in range(0, self.height):
                energy_memo[(col, row)] = self.energy(col, row)
        start_time = time.time()
        if dp == False:
            seam_list = []
            for col in range(self.width):
                seam = self.naive_alg(col, 0, energy_memo)
                seam_list.append(seam)
            min_seam = self.find_min(seam_list, energy_memo=energy_memo)
            print("--- %s seconds ---" % (time.time() - start_time))
            print(min_seam)
        else:
            seam_list = []
            for col in range(self.width):
                seam = self.dp_alg(col, 0, energy_memo)
                seam_list.append(seam)
            min_seam = self.find_min(seam_list, energy_memo=energy_memo)
            print("--- %s seconds ---" % (time.time() - start_time))
            print(min_seam)

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())

    def dp_alg(self, col, row, energy_memo):
    # is col,row in best_seams[], return best seam tuples likst
        if (col, row) in self.best_seams.keys():
            return self.best_seams[(col, row)]
        # if not, do naive call, before return statement, store result in lookup table
        # base case, if we hit bottom return coords of pixel
        if row == self.height - 1:
            #return energy_memo[col, row]
            return [(col, row)]
        # recursaive case
        # return pixel_energy(i,j) + min(seam energies of three pixels under)

        # loop to check the next pixels
        # for col in range(imagematrix.width):
        # determine which pixels to check while staying in range of image
        if col == 0:
            seam_list = []
            seam_list.append(self.dp_alg(col, row + 1, energy_memo))
            seam_list.append(self.dp_alg(col + 1, row + 1, energy_memo))

            min_seam = self.find_min(seam_list, energy_memo=energy_memo)
            pos_tuple = (col, row)
            min_seam.insert(0, pos_tuple)
            self.best_seams[(col, row)] = min_seam
            return min_seam
            
        elif col == self.width - 1:
            seam_list = []
            seam_list.append(self.dp_alg(col, row + 1, energy_memo))
            seam_list.append(self.dp_alg(col - 1, row + 1, energy_memo))

            min_seam = self.find_min(seam_list, energy_memo=energy_memo)
            pos_tuple = (col, row)
            min_seam.insert(0, pos_tuple)
            self.best_seams[(col, row)] = min_seam
            return min_seam

        else:
            seam_list = []
            seam_list.append(self.dp_alg(col, row + 1, energy_memo))
            seam_list.append(self.dp_alg(col - 1, row + 1, energy_memo))
            seam_list.append(self.dp_alg(col + 1, row + 1, energy_memo))

            min_seam = self.find_min(seam_list, energy_memo=energy_memo)
            pos_tuple = (col, row)
            min_seam.insert(0, pos_tuple)
            self.best_seams[(col, row)] = min_seam
            return min_seam


    def naive_alg(self, col, row, energy_memo):
    # is col,row in best_seams[], return best seam tuples likst
        # if not, do naive call, before return statement, store result in lookup table
        # base case, if we hit bottom return coords of pixel
        if row == self.height - 1:
            #return energy_memo[col, row]
            return [(col, row)]

        # loop to check the next pixels
        # for col in range(imagematrix.width):
        # determine which pixels to check while staying in range of image
        if col == 0:
            seam_list = []
            seam_list.append(self.naive_alg(col, row + 1, energy_memo))
            seam_list.append(self.naive_alg(col + 1, row + 1, energy_memo))

            min_seam = self.find_min(seam_list, energy_memo=energy_memo)
            pos_tuple = (col, row)
            min_seam.insert(0, pos_tuple)
            return min_seam

        elif col == self.width - 1:
            seam_list = []
            seam_list.append(self.naive_alg(col, row + 1, energy_memo))
            seam_list.append(self.naive_alg(col - 1, row + 1, energy_memo))

            min_seam = self.find_min(seam_list, energy_memo=energy_memo)
            pos_tuple = (col, row)
            min_seam.insert(0, pos_tuple)
            return min_seam

        else:
            seam_list = []
            seam_list.append(self.naive_alg(col, row + 1, energy_memo))
            seam_list.append(self.naive_alg(col - 1, row + 1, energy_memo))
            seam_list.append(self.naive_alg(col + 1, row + 1, energy_memo))

            min_seam = self.find_min(seam_list, energy_memo=energy_memo)
            pos_tuple = (col, row)
            min_seam.insert(0, pos_tuple)
            return min_seam

    def find_min(self, seam_list, energy_memo):
        # return the list of tuples for the seam with the lowest energy
        energy_list = []
        energy = 0
        for seam in seam_list:
            # calculate energy of seam
            energy = 0
            for pixel in seam:
                energy += energy_memo[pixel]
            energy_list.append(energy)
        min_index = energy_list.index(min(energy_list))
        return seam_list[min_index]



obj = ResizeableImage('8X8.png')
obj.best_seam(dp=False)