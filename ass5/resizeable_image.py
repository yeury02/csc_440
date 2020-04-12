import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):

    def naive_path(self, w, h, path, e):
        if h == self.height - 1:
            self.seams.append((path,e))
            return path

        for c in range(max(0, w - 1), min(self.width, w + 2)):
            energy = self.energy(c, (h + 1))
            pixel = [(c, h + 1)]
            self.naive_path(c, h + 1, path + pixel, e + energy)
        
        return

        # if row == self.height - 1:
        #     return [(col, row)]

    def best_seam(self, dp=True):
        # this list will have all the paths of all seams
        self.seams = []

        if dp == False:
            col = 0
            while col < self.width:
                # third paramet is a list of tuple because it will allow me
                # to manupulate it later on by appending paths to it
                # fourth parameter is the energy at the current position
                # which initializes at 0
                self.naive_path(col, 0,[(col,0)], 10000)                    # for every pixel of first row, find a path
                col += 1
            
            # this gets the seam with the lowest energy
            # and its energy
            best_path_with_lowest_energy = min(self.seams, key=lambda n: n[1])
            best_path = best_path_with_lowest_energy[0]
    
        # returns seam with lowest energy
        return best_path

        if dp == True:
            pass

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
    
obj = ResizeableImage('8x5.png')
print(obj.best_seam(False))