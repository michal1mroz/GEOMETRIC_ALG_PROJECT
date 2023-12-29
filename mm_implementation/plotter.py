import matplotlib.pyplot as plt
import matplotlib.collections as mcoll
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Button

class Plotter:
    def __init__(self, master, xmin=0, xmax=10, ymin=0, ymax=10):
        self.master = master
        self.master.title("Plotter")

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)
        self.ax.set_aspect('equal', adjustable='box')

        self.addedPoints = []
        self.pointLabels = []

        self.lineSegments = []
        self.prevPoint = None

        self.pointCounter = 0
        self.scenes = []

        self.filePath = "tmp"

        self.pointColor = {0: 'green', 1: 'red', 2: 'darkblue', 3: 'lightblue', 4: 'brown'}

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.label = tk.Label(master=self.master, text="Click on the plot to add points")
        self.label.pack(side=tk.TOP)

        self.quit_button = tk.Button(master=self.master, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.add_points_button = tk.Button(master=self.master, text="Add line segments", command=self.toggle_add_points)
        self.add_points_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.add_points_button.config(bg='red')
        self.add_points_enabled = False

        self.dump_points_button = tk.Button(master=self.master, text="Print line segments", command=self.dumpPoints)
        self.dump_points_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.save_points_button = tk.Button(master=self.master, text="Save to .json", command=self.saveToFile)
        self.save_points_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.load_points_button = tk.Button(master=self.master, text="Load points from .json",
                                            command=self.loadFromFile)
        self.load_points_button.pack(side=tk.LEFT, padx=10, pady=10)


        self.clearDisplay_button = tk.Button(master=self.master, text="Clear display", command=self.clearDisplay)
        self.clearDisplay_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.fig.canvas.mpl_connect('button_press_event', self.onClick)

    def clearDisplay(self):
        self.ax.clear()
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.set_aspect('equal', adjustable='box')
        self.addedPoints = []
        self.pointLabels = []
        self.lineSegments = []
        self.prevPoint = None
        self.pointCounter = 0
        self.add_points_button.config(bg='red')
        self.add_points_enabled = False
        self.canvas.draw()

    def toggle_add_points(self):
        self.add_points_enabled = not self.add_points_enabled
        if self.add_points_enabled:
            self.add_points_button.config(bg='green')
        else:
            self.add_points_button.config(bg='red')

    def dumpPoints(self):
        if self.lineSegments != []:
            print("Added line segments:\n")
            for line in self.lineSegments:
                print(line)

    def saveToFile(self):
        if self.filePath is not None:
            with open(f"{self.filePath}.json", "w") as f:
                for line in self.lineSegments:
                    l = ', '.join([f"({x},{y})" for (x, y) in line])
                    f.write(f"{l}\n")

    def loadFromFile(self):
        if self.filePath is not None:
            self.clearDisplay()
            with open(f"{self.filePath}.json", "r") as f:
                for line in f:
                    vals = [tuple(map(float, pair.strip('()').split(','))) for pair in line.strip().split('), (')]
                    self.lineSegments.append(tuple(vals))
            if self.lineSegments != []:
                for line in self.lineSegments:
                    print(line)
                    (x1, y1), (x2, y2) = line
                    self.ax.plot(x1, y1, 'bo')
                    self.ax.plot(x2, y2, 'bo')
                    self.ax.plot([x1, x2], [y1, y2], 'b-')
            self.canvas.draw()

    def setPath(self, fileName):
        self.filePath = fileName

    def onClick(self, event):
        if self.add_points_enabled and event.button == 1:
            x, y = event.xdata, event.ydata
            label = self.pointCounter
            self.addedPoints.append((x, y))
            self.pointLabels.append(label)
            self.ax.plot(x, y, 'bo')
            self.ax.text(x, y, label, fontsize=11, ha='right')

            if self.prevPoint is not None:
                x_prev, y_prev = self.prevPoint
                self.ax.plot([x_prev, x], [y_prev, y], 'b-')
                self.lineSegments.append(((x_prev, y_prev), (x, y)))
                self.prevPoint = None
            else:
                self.prevPoint = (x, y)

            self.pointCounter += 1
            self.canvas.draw()