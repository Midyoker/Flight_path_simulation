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
        self.vertical_speed = 0 
        self.paused = False 
        self.flight_path = [(self.x, self.y)]  
    def update_position(self, time_interval):
        if not self.paused:  # Only update position if not paused
            new_x = self.x + self.speed * time_interval * math.cos(math.radians(self.heading))
            new_y = self.y + self.speed * time_interval * math.sin(math.radians(self.heading))
            
            # Boundary check for longitude (x-axis)
            if 0 <= new_x <= xlim[1]:
                self.x = new_x
            elif new_x < 0:
                self.x = 0
            else:
                self.x = xlim[1]

            # Boundary check for latitude (y-axis)
            if 0 <= new_y <= ylim[1]:
                self.y = new_y
            elif new_y < 0:
                self.y = 0
            else:
                self.y = ylim[1]

            self.altitude += self.vertical_speed * time_interval
            self.flight_path.append((self.x, self.y))  # Add current position to flight path

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
        aircraft.change_heading(-1)  # Turn right
    elif event.char == 'a':
        aircraft.speed += 1  # Increase speed
    elif event.char == 's':
        aircraft.speed -= 1  # Decrease speed
    elif event.char == 'r':
        aircraft.x = 0
        aircraft.y = 0
        aircraft.altitude = 0
        aircraft.change_vertical_speed(0)  # Reset vertical speed to zero
        aircraft.heading = 45
        aircraft.flight_path = [(aircraft.x, aircraft.y)]  # Clear the flight path
    elif event.char == 'z':
        aircraft.toggle_pause()  # Toggle pause movement

def on_mouse_scroll(event):
    # Zoom-in and zoom-out using the mouse scroll event
    zoom_factor = 0.9 if event.delta < 0 else 1.1
    ax.set_xlim(ax.get_xlim()[0] * zoom_factor, ax.get_xlim()[1] * zoom_factor)
    ax.set_ylim(ax.get_ylim()[0] * zoom_factor, ax.get_ylim()[1] * zoom_factor)
    canvas.draw()

def update_plot():
    global data_file
    aircraft.update_position(time_interval)
    aircraft_plot.set_data([aircraft.x], [aircraft.y])
    flight_path_plot.set_data(*zip(*aircraft.flight_path))  
    canvas.draw()
    info_label.config(text=f"Altitude: {aircraft.altitude} | Longitude: {aircraft.x} | Latitude: {aircraft.y} | Speed: {aircraft.speed}")
    root.after(int(time_interval * 1000), update_plot)

root = tk.Tk()
root.title("Flight Path Simulation")

xlim, ylim = (0, 1000), (0, 1000)

terrain = np.random.randint(0, 500, size=(xlim[1], ylim[1]))

fig, ax = plt.subplots()
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_aspect('equal', adjustable='box')
ax.imshow(terrain, cmap='terrain', origin='lower', extent=[xlim[0], xlim[1], ylim[0], ylim[1]], alpha=0.7)

aircraft = Aircraft(x=10, y=10, altitude=1000, speed=5, heading=45)  
aircraft_plot, = ax.plot([aircraft.x], [aircraft.y], 'ro', markersize=10)
flight_path_plot, = ax.plot([], [], 'g-', linewidth=2) 

time_interval = 0.1  # 0.1 second, for example

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create a label to display aircraft information
info_label = tk.Label(root, text="", font=("Arial", 12))
info_label.pack()

root.bind('<KeyPress>', on_key_press)
root.bind('<MouseWheel>', on_mouse_scroll)  # Bind the mouse scroll event

root.after(int(time_interval * 1000), update_plot)

root.mainloop()
