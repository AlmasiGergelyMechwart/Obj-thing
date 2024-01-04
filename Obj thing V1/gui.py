import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
import os
import math

from object import Object

class GUI(tk.Tk):

    canvasPanelRatio = [0.75, 0.9]

    baseBackgroundColor = "grey"
    baseCanvasColor = "white"
    baseFillColor = "lightgrey"
    baseLineColor = "black"

    backgroundColor = baseBackgroundColor
    canvasColor = baseCanvasColor
    fillColor = baseFillColor
    lineColor = baseLineColor

    windowSize = [0, 0]
    canvasSize = [0, 0]
    rightPanelSize = [0, 0]
    bottomPanelSize = [0, 0]

    object = None

    def __init__(self):
        super().__init__()

        # root
        self.minsize(900, 500)
        self["bg"] = self.backgroundColor
        self.title("Obj thing")

        canvasOffset = [0.015, 0.02]

        # canvas
        self.canvas = tk.Canvas(self, background=self.canvasColor)
        self.canvas.place(relx=canvasOffset[0], rely=canvasOffset[1], relwidth=self.canvasPanelRatio[0], relheight=self.canvasPanelRatio[1])
        self.canvas.update()

        # -----x-----

        # right panel
        self.rightPanel = tk.Frame(self, background=self.backgroundColor)
        self.rightPanel.place(relx=canvasOffset[0]+self.canvasPanelRatio[0], rely=canvasOffset[1], relwidth=1-self.canvasPanelRatio[0]-canvasOffset[0], relheight=self.canvasPanelRatio[1])
        self.rightPanel.update()

        self.rightPanelButtonNames = ["reset_zoom", "reset_position", "reset_rotation", "reset_canvas_color", "reset_fill_color", "reset_line_color"]
        numOfButtons = 10
        self.rightPanelButtons = [0 for i in range(numOfButtons)]
        panelPadding = [0.04, 0.03] # top, bottom
        margin = [0.01, 0.1] # top-bottom, left-right

        self.rotationTypes = ["Local Axis rotation", "Global Axis rotation"]
        self.currentRotationType = tk.StringVar(self)
        self.rightPanelButtons[6] = ttk.OptionMenu(self.rightPanel, self.currentRotationType, self.rotationTypes[0], *self.rotationTypes, command=lambda x: self.reset_rotation())

        self.rightPanelButtons[numOfButtons-1] = ttk.Button(self.rightPanel, text="Open file", command=self.open_file)

        for i in range(len(self.rightPanelButtons)):
            try:
                if self.rightPanelButtons[i] == 0:
                    self.rightPanelButtons[i] = ttk.Button(self.rightPanel, text=" ".join(self.rightPanelButtonNames[i].split("_")).capitalize(), command=eval("self.%s" % self.rightPanelButtonNames[i]))
                self.rightPanelButtons[i].place(relx=margin[1], rely=panelPadding[0]+margin[0]+i/numOfButtons-sum([panelPadding[n]/numOfButtons*i for n in range(2)]), relwidth=1-margin[1]*2, relheight=1/numOfButtons-margin[0]*2-sum([panelPadding[n]/numOfButtons for n in range(2)]))
            except:
                pass

        # -----x-----

        # bottom panel
        self.bottomPanel = tk.Frame(self, background=self.backgroundColor)
        self.bottomPanel.place(relx=canvasOffset[0], rely=canvasOffset[1]+self.canvasPanelRatio[1], relwidth=1-canvasOffset[0], relheight=1-self.canvasPanelRatio[1]-canvasOffset[1])
        self.bottomPanel.update()

        self.bottomPanelButtonNames = ["canvas_color", "fill_color", "line_color"]
        self.bottomPanelCheckButtonNames = ["fill", "show all"]
        self.bottomPanelButtons = []
        self.bottomPanelCheckButtons = []

        numOfButtons = 4
        panelPadding = [0.005, 0.005] # left, right
        margin = [0.1, 0.02] # top-bottom, left-right

        labelButtonRatio = 0.4
        buttonRelSize = [0.8, 0.8]
        fullwidth = 1/numOfButtons-margin[1]*2-sum([panelPadding[j]/numOfButtons for j in range(2)])

        self.fill = tk.BooleanVar(value=True)
        self.showall = tk.BooleanVar(value=True)

        for i in range(len(self.bottomPanelButtonNames)):
            self.bottomPanelButtons.append([0, 0])
            self.bottomPanelButtons[i][0] = ttk.Label(self.bottomPanel, text=self.bottomPanelButtonNames[i].replace("_", " ").capitalize()+":", background=self.backgroundColor)
            self.bottomPanelButtons[i][0].place(relx=panelPadding[0]+margin[1]+i/numOfButtons-sum([panelPadding[j]/numOfButtons*i for j in range(2)]), rely=margin[0], relwidth=fullwidth*labelButtonRatio, relheight=1-margin[0]*2)

            varName = "self.%s" % list(map(lambda y: y[0].lower()+y[1:], ["".join(map(lambda x: x[0].upper()+x[1:], self.bottomPanelButtonNames[i].split("_")))]))[0]
            self.bottomPanelButtons[i][1] = tk.Button(self.bottomPanel, relief="flat", background=eval(varName), command=lambda x=varName: self.change_color(x))
            self.bottomPanelButtons[i][1].place(relx=float(self.bottomPanelButtons[i][0].place_info()["relx"])+fullwidth*labelButtonRatio+fullwidth*(1-labelButtonRatio)*(1-buttonRelSize[0])/2, rely=float(self.bottomPanelButtons[i][0].place_info()["rely"])+float(self.bottomPanelButtons[i][0].place_info()["relheight"])*(1-buttonRelSize[1])/2, relwidth=fullwidth*(1-labelButtonRatio)*buttonRelSize[0], relheight=float(self.bottomPanelButtons[i][0].place_info()["relheight"])*buttonRelSize[1])

        numOfButtons = 2
        panelPadding = [0.75, 0.01] # left, right
        margin = [0.1, 0] # top-bottom, left-right
        labelButtonRatio = 0.6
        buttonRelSize = [0.35, 0.45]
        fullwidth = 1/numOfButtons-margin[1]*2-sum([panelPadding[j]/numOfButtons for j in range(2)])

        for i in range(len(self.bottomPanelCheckButtonNames)):
            self.bottomPanelCheckButtons.append([0, 0])
            self.bottomPanelCheckButtons[i][0] = ttk.Label(self.bottomPanel, text=self.bottomPanelCheckButtonNames[i].capitalize()+":", background=self.backgroundColor, anchor="e")
            self.bottomPanelCheckButtons[i][0].place(relx=panelPadding[0]+margin[1]+i/numOfButtons-sum([panelPadding[j]/numOfButtons*i for j in range(2)]), rely=margin[0], relwidth=fullwidth*labelButtonRatio, relheight=1-margin[0]*2)

            # self.bottomPanelCheckButtons[i][1] = tk.Button(self.bottomPanel, background=self.backgroundColor, command=self.update_canvas, text="P", font=("Wingdings 2", "12", "bold"))
            self.bottomPanelCheckButtons[i][1] = tk.Checkbutton(self.bottomPanel, background=self.backgroundColor, command=self.update_canvas, variable=eval("self.%s" % "".join(self.bottomPanelCheckButtonNames[i].split(" "))))
            self.bottomPanelCheckButtons[i][1].place(relx=float(self.bottomPanelCheckButtons[i][0].place_info()["relx"])+fullwidth*labelButtonRatio+fullwidth*(1-labelButtonRatio)*(1-buttonRelSize[0])/2, rely=float(self.bottomPanelCheckButtons[i][0].place_info()["rely"])+float(self.bottomPanelCheckButtons[i][0].place_info()["relheight"])*(1-buttonRelSize[1])/2, relwidth=fullwidth*(1-labelButtonRatio)*buttonRelSize[0], relheight=float(self.bottomPanelCheckButtons[i][0].place_info()["relheight"])*buttonRelSize[1])

        # -----x-----

        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<ButtonRelease-1>", self.move_end)

        self.canvas.bind("<ButtonPress-3>", self.rotate_start)
        self.canvas.bind("<ButtonRelease-3>", self.rotate_end)

        self.canvas.bind("<MouseWheel>", self.zoom_change)

        self.bind("<Configure>", self.on_window_resize)

        self.on_window_resize()

    def update_canvas(self):
        if self.object == None: return
        
        self.canvas.delete("all")

        self.canvas['bg'] = self.canvasColor

        faces = []

        for i in range(len(self.object.faces)):
            points = []
            vertexNormals = []
            for j in range(len(self.object.faces[i])):
                point = [(self.object.vertices[self.object.faces[i][j][0]-1][n]+self.object.offset[n]) for n in range(3)]
                # multiply by -1 so it is not upside down
                point[1] *= -1

                point = self.rotate_point(point)

                points.append([(point[i]*self.object.zoom+(self.object.position[i] if i < 2 else 0)) for i in range(3)])

                if len(self.object.vertexNormals) > 0:
                    vertexNormal = self.object.vertexNormals[self.object.faces[i][j][2]-1]
                    vertexNormal = [vertexNormal[0], -vertexNormal[1], vertexNormal[2]]

                    vertexNormal = self.rotate_point(vertexNormal)
                    vertexNormals.append(vertexNormal)

                    # self.canvas.create_line([points[j][n] for n in range(2)], [points[j][n]+vertexNormal[n]*10 for n in range(2)], fill="orange", width=2)

            # midPoints = [sum([points[m][n] for m in range(len(points))])/len(points) for n in range(2)]
            # midVertexNormals = [sum([vertexNormals[m][n] for m in range(len(vertexNormals))])/len(vertexNormals) for n in range(2)]
            # self.canvas.create_line(midPoints, [midPoints[n]+midVertexNormals[n]*20 for n in range(2)], fill="orange", width=2)

            if len(vertexNormals) > 0 and not self.showall.get():
                facingZ = max([vertexNormals[m][2] for m in range(len(vertexNormals))])

                if facingZ > 0:
                    faces.append(points)
            else:
                faces.append(points)


        if self.fill.get():
            faces.sort(key=lambda points: sum([points[n][2] for n in range(len(points))])/len(points))

        for points in faces:
            points = [[point[n] for n in range(2)] for point in points]
            self.canvas.create_polygon(points, fill=self.fillColor if self.fill.get() else "", outline=self.lineColor)

        print("%s/%s" % (len(faces), len(self.object.faces)))


    def on_window_resize(self, event=""):
        if event != "":
            if event.widget == self and self.windowSize != [event.width, event.height]:
                self.windowSize = [event.width, event.height]
            elif event.widget == self.canvas and self.canvasSize != [event.width, event.height]:
                relCanvasSize = [event.width - self.canvasSize[0], event.height - self.canvasSize[1]]
                self.object.position = [self.object.position[i]+relCanvasSize[i]/2 for i in range(2)]
                self.canvasSize = [event.width, event.height]
                self.update_canvas()
            elif event.widget == self.rightPanel and self.rightPanelSize != [event.width, event.height]:
                self.rightPanelSize = [event.width, event.height]
            elif event.widget == self.bottomPanel and self.bottomPanelSize != [event.width, event.height]:
                self.bottomPanelSize = [event.width, event.height]
        else:
            self.windowSize = [self.winfo_width(), self.winfo_height()]
            self.canvasSize = [self.canvas.winfo_width(), self.canvas.winfo_height()]
            self.rightPanelSize = [self.rightPanel.winfo_width(), self.rightPanel.winfo_height()]
            self.bottomPanelSize = [self.bottomPanel.winfo_width(), self.bottomPanel.winfo_height()]


    def move_start(self, event):
        if self.object == None: return
        self.movePrevPos = [event.x, event.y]
        self.moveEventID = self.canvas.bind("<Motion>", self.move)

    def move(self, event):
        moveRelPos = [event.x - self.movePrevPos[0], event.y - self.movePrevPos[1]]
        self.object.position = [self.object.position[i]+moveRelPos[i] for i in range(2)]

        self.update_canvas()

        self.movePrevPos = [event.x, event.y]

    def move_end(self, event):
        if self.object == None: return
        self.canvas.unbind("<Motion>", self.moveEventID)

    def reset_position(self):
        if self.object == None: return
        self.object.position = [self.canvas.winfo_width()/2, self.canvas.winfo_height()/2]

        self.update_canvas()


    def rotate_start(self, event):
        if self.object == None: return
        self.rotatePrevPos = [event.x, event.y]
        self.rotateEventID = self.canvas.bind("<Motion>", self.rotate)

    def rotate(self, event):
        # in pixels
        rotateRelPos = [event.x - self.rotatePrevPos[0], event.y - self.rotatePrevPos[1]]

        # in radians
        angle = [math.radians(rotateRelPos[1-i]/2) for i in range(2)]
        angle[1] *= -1

        # 2 pixel moved by cursor is 1 degree rotation

        if self.currentRotationType.get() == self.rotationTypes[0]:
            self.object.rotation["angles"] = [self.object.rotation["angles"][i] + angle[i] for i in range(2)]

        elif self.currentRotationType.get() == self.rotationTypes[1]:
            s = math.sin(angle[0])
            c = math.cos(angle[0])

            Rx = [[ 1,  0,  0],
                  [ 0,  c, -s],
                  [ 0,  s,  c]]

            s = math.sin(angle[1])
            c = math.cos(angle[1])

            Ry = [[ c,  0,  s],
                  [ 0,  1,  0],
                  [-s,  0,  c]]

            self.object.rotation["matrix"] = self.multiply_matricies(self.multiply_matricies(self.object.rotation["matrix"], Ry), Rx)

        self.update_canvas()

        self.rotatePrevPos = [event.x, event.y]

    def rotate_end(self, event):
        if self.object == None: return
        self.canvas.unbind("<Motion>", self.rotateEventID)

    def reset_rotation(self):
        if self.object == None: return
        self.object.rotation["angles"] = [0, 0]
        self.object.rotation["matrix"] = [[1, 0, 0],
                                          [0, 1, 0],
                                          [0, 0, 1]]

        self.update_canvas()


    def rotate_point(self, point):
        if self.currentRotationType.get() == self.rotationTypes[0]:
            s = math.sin(self.object.rotation["angles"][0])
            c = math.cos(self.object.rotation["angles"][0])

            Rx = [[ 1,  0,  0],
                  [ 0,  c, -s],
                  [ 0,  s,  c]]

            s = math.sin(self.object.rotation["angles"][1])
            c = math.cos(self.object.rotation["angles"][1])

            Ry = [[ c,  0,  s],
                  [ 0,  1,  0],
                  [-s,  0,  c]]

            point = self.multiply_matricies(self.multiply_matricies(point, Ry), Rx)

        elif self.currentRotationType.get() == self.rotationTypes[1]:
            point = self.multiply_matricies(point, self.object.rotation["matrix"])

        return point


    def multiply_matricies(self, M1, M2):
        for i in range(2):
            M = [M1, M2]
            if str(type(M[i][0]))[8:-2] != "list":
                M[i] = [M[i]]
                M1, M2 = M[0], M[1]

        if len(M1[0]) != len(M2):
            raise

        Mout = [[0 for i in range(len(M2[0]))] for i in range(len(M1))]

        for i in range(len(Mout)):
            for j in range(len(Mout[0])):
                for k in range(len(M1[0])):
                    Mout[i][j] += M1[i][k] * M2[k][j]

        if len(Mout) == 1:
            Mout = Mout[0]

        return Mout

    def zoom_change(self, event):
        if self.object == None: return
        if event.delta > 0:
            self.object.zoom = self.object.zoom*1.1
        elif event.delta < 0:
            self.object.zoom = self.object.zoom/1.1

        self.update_canvas()

    def reset_zoom(self):
        if self.object == None: return
        if self.object.size[0] > self.object.size[1]:
            self.object.zoom = self.canvasSize[0]/self.object.size[0]*0.8
        else:
            self.object.zoom = self.canvasSize[1]/self.object.size[1]*0.8

        self.update_canvas()

    def change_color(self, variable):
        if self.object == None: return
        color = colorchooser.askcolor()
        if color[1] != None:
            exec("%s = color[1]" % variable)
            try:
                exec("self.bottomPanelButtons[%s][1]['bg'] = color[1]" % self.bottomPanelButtonNames.index("%s_color" % variable[5:-5]))
            except:
                pass

        self.update_canvas()

    def reset_canvas_color(self):
        self.canvasColor = self.baseCanvasColor
        self.bottomPanelButtons[0][1]["bg"] = self.baseCanvasColor
        self.update_canvas()

    def reset_fill_color(self):
        self.fillColor = self.baseFillColor
        self.bottomPanelButtons[1][1]["bg"] = self.baseFillColor
        self.update_canvas()

    def reset_line_color(self):
        self.lineColor = self.baseLineColor
        self.bottomPanelButtons[2][1]["bg"] = self.baseLineColor
        self.update_canvas()

    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Object Files","*.obj")], initialdir=os.getcwd()+"/obj")
        if filename != "":
            if self.object == None:
                self.object = Object(filename)
            else:
                self.object.__init__(filename)
            self.object.position = [self.canvas.winfo_width()/2, self.canvas.winfo_height()/2]
            self.reset_zoom()