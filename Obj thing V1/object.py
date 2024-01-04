import math

class Object:
    def __init__(self, file):
        self.vertices = []
        self.vertexTextures = []
        self.vertexNormals = []
        self.faces = []
        self.min = [math.inf, math.inf, math.inf]
        self.max = [-math.inf, -math.inf, -math.inf]
        self.size = [0, 0, 0]
        self.offset = [0, 0]
        self.position = [0, 0]
        self.rotation = {
            "angles": [0, 0],
            "matrix": [[1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1]]
        }
        self.zoom = 0

        f = open(file, "r")
        for line in f.readlines():
            if line[:2] == "v ":
                vertex = list(map(float, line[2:].split()))
                self.vertices.append(vertex)
                for i in range(3):
                    if   vertex[i] > self.max[i]: self.max[i] = vertex[i]
                    elif vertex[i] < self.min[i]: self.min[i] = vertex[i]
            elif line[:2] == "f ":
                self.faces.append(list(map(lambda x: list(map(lambda y: int(y) if y != "" else None, x.split("/"))), line[2:].split())))
            elif line[:3] == "vt ":
                self.vertexTextures.append(list(map(float, line[3:].split())))
            elif line[:3] == "vn ":
                self.vertexNormals.append(list(map(float, line[3:].split())))
        f.close()

        self.size = [(self.max[i]-self.min[i]) for i in range(3)]
        self.offset = [(-self.min[i]-self.size[i]/2) for i in range(3)]

        print(f"Verticies:\n%s" % self.vertices)
        print(f"Vertex Textures:\n%s" % self.vertexTextures)
        print(f"Vertex Normals:\n%s" % self.vertexNormals)
        print(f"Faces:\n%s" % self.faces)
        print(f"Min/Max of each coordinate:\n%s" % self.min, self.max)
        print(f"Size:\n%s" % self.size)
        print(f"Offset:\n%s" % self.offset)
