import matplotlib.pyplot as plt
from vis_bit.main import Visualizer
from matplotlib.widgets import Button
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plotter_functions import trapezoidal_map_vis, findPointVisualised
from DataStructures import Point


class Presenter:
    def __init__(self, scenes):
        self.scenes = []
        self.scene_data = []
        for vis in scenes:
            data, plot_data = vis.getData()
            self.scenes.append(data)
            self.scene_data.append(plot_data)

        self.i = len(self.scenes) - 1

        plt.subplots_adjust(bottom=0.2)

    def __configure_buttons(self):
        plt.subplots_adjust(bottom=0.2)
        ax_prev = plt.axes([0.05, 0.05, 0.15, 0.075])
        ax_next = plt.axes([0.25, 0.05, 0.15, 0.075])
        b_next = Button(ax_next, 'Następny')
        b_next.on_clicked(self.next)
        b_prev = Button(ax_prev, 'Poprzedni')
        b_prev.on_clicked(self.prev)
        return [b_prev, b_next]

    def draw(self):
        self.ax.clear()
        for figure in self.scenes[self.i]:
            figure.draw(self.ax)
        self.ax.autoscale()
        plt.draw()

    def next(self, event):
        self.i = (self.i + 1) % len(self.scenes)
        self.draw()

    def prev(self, event):
        self.i = (self.i - 1) % len(self.scenes)
        self.draw()

    def set_axes(self, ax):
        self.ax = ax


    def display(self):
        plt.close()
        fig = plt.figure()
        self.widgets = self.__configure_buttons()
        self.ax = plt.axes(autoscale_on=False)

        plt.show()
        self.draw()


class Plotter:
    def __init__(self, master, scenes=[], xmin=0, xmax=10, ymin=0, ymax=10):
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

        self.lineSegments = []
        self.prevPoint = None

        self.interactiveFace = Visualizer()

        self.scenes = scenes

        self.filePath = "tmp"

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.label = tk.Label(master=self.master, text="Click on the plot to add points")
        self.label.pack(side=tk.TOP)

        self.quit_button = tk.Button(master=self.master, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.add_segments_button = tk.Button(master=self.master, text="Add line segments", command=self.toggle_add_segments)
        self.add_segments_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.add_segments_button.config(bg='red')
        self.add_segments_enabled = False

        self.dump_points_button = tk.Button(master=self.master, text="Print line segments", command=self.dumpPoints)
        self.dump_points_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.clearDisplay_button = tk.Button(master=self.master, text="Clear display", command=self.clearDisplay)
        self.clearDisplay_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.play_scenes_button = tk.Button(master=self.master, text="Create trapezoid map", command=self.startPresenter)
        self.play_scenes_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.fig.canvas.mpl_connect('button_press_event', self.onClick)

    def findPoint(self):
        findPointVisualised(self.lineSegments, Point(self.addedPoints[-1][0], self.addedPoints[-1][1]))

    def startPresenter(self):
        if self.scenes:
            presenter = Presenter(self.scenes)
            presenter.display()
        else:
            self.T, self.scenes = trapezoidal_map_vis(self.lineSegments)
            presenter = Presenter(self.scenes)
            presenter.display()

    def clearDisplay(self):
        self.ax.clear()
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.set_aspect('equal', adjustable='box')
        self.addedPoints = []
        self.lineSegments = []
        self.prevPoint = None
        self.add_segments_button.config(bg='red')
        self.add_segments_enabled = False
        self.canvas.draw()

    def toggle_add_segments(self):
        self.add_segments_enabled = not self.add_segments_enabled
        if self.add_segments_enabled:
            self.add_segments_button.config(bg='green')
        else:
            self.add_segments_button.config(bg='red')

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
        if self.add_segments_enabled and event.button == 1:
            x, y = event.xdata, event.ydata
            self.ax.plot(x, y, 'bo')

            if self.prevPoint is not None:
                x_prev, y_prev = self.prevPoint
                self.ax.plot([x_prev, x], [y_prev, y], 'b-')
                self.lineSegments.append(((x_prev, y_prev), (x, y)))
                self.prevPoint = None
            else:
                self.prevPoint = (x, y)

            self.canvas.draw()
