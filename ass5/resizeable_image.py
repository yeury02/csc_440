import imagematrix
import time

class ResizeableImage(imagematrix.ImageMatrix):

    def naive_path(self, row, col, path, energy_pos):
        # once I reach the last row
        if col == self.height - 1:
            self.all_seams.append((path,energy_pos))
            return path

        max_row = max(0, row - 1)
        min_row = min(self.width, row + 2)
        for c in range(max_row, min_row):
            cur_energy = self.energy(c, (col + 1))                  # calc current energy
            pixel = [(c, col + 1)]
            self.naive_path(c, col + 1, path + pixel, energy_pos + cur_energy)
    
    def dynamic_path(self, energy_grid, tracker):
        # start looking at the second row 
        for row in range(1, self.height):
            for col in range(self.width):
                
                # if at the first column
                if col == 0:
                    # get the boottom and right neighbors
                    neighbors = [energy_grid[row - 1][col], energy_grid[row - 1][col + 1]]
                    # get the minimun one
                    minimun = neighbors.index(min(neighbors))
                    # tracker keeps track of the minimun one
                    tracker[row][col] = minimun + col-1
                    # add it to the energy_grid list
                    ans = energy_grid[row - 1][minimun + col-1]

                elif col == self.width - 1:
                    #end point
                    neighbors = [energy_grid[row - 1][col - 1], energy_grid[row - 1][col]] 

                    minimun = neighbors.index(min(neighbors))

                    tracker[row][col] = minimun + col - 1

                    ans = energy_grid[row - 1][minimun + col - 1]
                    
                else:
                    # get all the neighbors
                    neighbors = [energy_grid[row - 1][col - 1], energy_grid[row - 1][col], energy_grid[row - 1][col + 1]] 
                    # get the minimun one
                    minimun = neighbors.index(min(neighbors))
                    tracker[row][col] = minimun + col - 1
                    ans = energy_grid[row - 1][minimun + col - 1]


                energy_grid[row][col] = energy_grid[row][col] + ans


        val = energy_grid[-1]
        min_sum = min(val)
        col = val.index(min(val))
        path = []
        # looping in a reverse manner because I appended values
        # I should of inserted at pos 0 to not have to do this step
        # but felt more comfortable going about it like this!
        for row in reversed(range(self.height)):
            path = [(col, row)] + path
            col = tracker[row][col]
        return (path, min_sum)

    def best_seam(self, dp=True):
        # this list will have all the paths of all seams
        # for naive solution
        self.all_seams = []

        if dp == False:
            start_time = time.time()
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
            best_path_with_lowest_energy = min(self.all_seams, key=lambda n: n[1])
            best_path = best_path_with_lowest_energy[0]
            print("--- %s seconds ---" % (time.time() - start_time))

        if dp == True:
            start_time = time.time()
            energy_grid = []
            tracker = []
            for h in range(self.height):
                row_e = []
                row_t = []
                for w in range(self.width):
                    row_e.append(self.energy(w, h))
                    row_t.append(0)
                energy_grid.append(row_e)
                tracker.append(row_t)
            best_path_with_lowest_energy = self.dynamic_path(energy_grid, tracker)
            best_path = best_path_with_lowest_energy[0]
            print("--- %s seconds ---" % (time.time() - start_time))

        # returns seam with lowest energy
        return best_path

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
    
obj = ResizeableImage('sunset_full.png')
print(obj.best_seam(True))