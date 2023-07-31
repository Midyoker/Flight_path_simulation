import tkinter as tk
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Aircraft:
    def __init__(self, x, y, altitude, speed, heading):
        self.x = x
        self.y = y
        self.altitude = altitude
        self.speed = speed
        self.heading = heading
        self.vertical_speed = 0  # Initialize vertical speed
        self.paused = False  # Initialize movement as not paused

    def update_position(self, time_interval):
        if not self.paused:  # Only update position if not paused
            self.x += self.speed * time_interval * math.cos(math.radians(self.heading))
            self.y += self.speed * time_interval * math.sin(math.radians(self.heading))
            self.altitude += self.vertical_speed * time_interval

    def change_heading(self, angle_change):
        self.heading += angle_change

    def change_vertical_speed(self, speed_change):
        self.vertical_speed += speed_change

    def toggle_pause(self):
        self.paused = not self.paused

def on_key_press(event):
    if event.keysym == 'Up':
        aircraft.change_vertical_speed(1)  # Increase vertical speed
    elif event.keysym == 'Down':
        aircraft.change_vertical_speed(-1)  # Decrease vertical speed
    elif event.keysym == 'Left':
        aircraft.change_heading(1)  # Turn left
    elif event.keysym == 'Right':
        aircraft.change_heading(-1)  # Turn rightz
    elif event.char == 'a':
        aircraft.speed += 1  # Increase speed
    elif event.char == 's':
        aircraft.speed -= 1  # Decrease speed
    elif event.char == 'r':
        aircraft.x = 10
        aircraft.y = 10
        aircraft.altitude = 500
        aircraft.change_vertical_speed(0)  # Reset vertical speed to zero
        aircraft.heading = 45
    elif event.char == 'z':
        aircraft.toggle_pause()  # Toggle pause movement

def update_plot():
    global data_file
    aircraft.update_position(time_interval)
    aircraft_plot.set_data([aircraft.x], [aircraft.y])
    canvas.draw()
    print(f"Altitude: {aircraft.altitude} | Longitude: {aircraft.x} | Latitude: {aircraft.y} | Speed: {aircraft.speed}")
    root.after(int(time_interval * 1000), update_plot)

root = tk.Tk()
root.title("Flight Path Simulation")

xlim, ylim = (0, 100), (0, 100)

terrain = np.random.randint(0, 500, size=(xlim[1], ylim[1]))

fig, ax = plt.subplots()
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_aspect('equal', adjustable='box')
ax.imshow(terrain, cmap='terrain', origin='lower', extent=[xlim[0], xlim[1], ylim[0], ylim[1]], alpha=0.7)

aircraft = Aircraft(x=10, y=10, altitude=1000, speed=5, heading=45)  # Example initial values
aircraft_plot, = ax.plot([aircraft.x], [aircraft.y], 'ro', markersize=10)

time_interval = 0.1  # 0.1 second, for example

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root.bind('<KeyPress>', on_key_press)

root.after(int(time_interval * 1000), update_plot)

root.mainloop()
r
