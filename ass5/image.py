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
    def dynamic_path(self, matrix, tracker):
        for w in range(1, self.height):
            for h in range(self.width):
                if h == 0:
                    neighbors = [matrix[w - 1][h], matrix[w - 1][h + 1]]
                    mini = neighbors.index(min(neighbors))
                    tracker[w][h] = mini + h
                    mine = matrix[w - 1][mini + h]
                elif h == self.width - 1:
                    neighbors = [matrix[w - 1][h - 1], matrix[w - 1][h]] 
                    mini = neighbors.index(min(neighbors))
                    tracker[w][h] = mini + h - 1
                    mine = matrix[w - 1][mini + h - 1]
                else:
                    neighbors = [matrix[w - 1][h - 1], matrix[w - 1][h], matrix[w - 1][h + 1]] 
                    mini = neighbors.index(min(neighbors))
                    tracker[w][h] = mini + h - 1
                    mine = matrix[w - 1][mini + h - 1]
                matrix[w][h] = matrix[w][h] + mine
        row = matrix[-1]
        lowest_sum = min(row)
        column = row.index(min(row))
        path = []
        for w in reversed(range(self.height)):
            path = [(column, w)] + path
            column = tracker[w][column]
        return (path, lowest_sum)              
    def best_seam(self, dp=True):
        if dp:
            energy_matrix = []
            tracker = []
            for h in range(self.height):
                rowe = []
                rowt = []
                for w in range(self.width):
                    rowe.append(self.energy(w, h))
                    rowt.append(0)
                energy_matrix.append(rowe)
                tracker.append(rowt)
            best = self.dynamic_path(energy_matrix, tracker)
        else:
            self.seams = []
            for c in range(self.width):
                self.naive_path(c, 0,[(c,0)], 10000)
            best = min(self.seams, key=lambda n: n[1])
        return best[0]
        # raise NotImplemented
    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
obj = ResizeableImage('8x5.png')
print(obj.best_seam(False))