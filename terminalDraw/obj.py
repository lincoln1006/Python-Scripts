class OBJ:
    def __init__(self, filename):
        with open(filename, "r") as f:
            text = f.readlines()
        temp = [[], [], []]
        cleanText = []
        ind = 0
        for val in text:
            if val == "\n":
                ind += 1   
            val = val.split()
            for i in range(len(val)):
                if ind == 0:
                    val[i] = float(val[i].strip("(,)"))
                else:
                    val[i] = int(val[i].strip("(,)"))
            val = tuple(val)
            temp[ind].append(val)
        temp[1].pop(0)
        temp[2].pop(0)

        self.points = []
        for val in temp[0]:
            self.points.append(val)
        self.lines = []
        for val in temp[1]:
            self.lines.append(val)
        self.faces = []
        for val in temp[2]:
            self.faces.append(val)