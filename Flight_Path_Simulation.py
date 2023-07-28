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

    def update_position(self, time_interval):
        # Update the aircraft's position based on speed, heading, and altitude
        self.x += self.speed * time_interval * math.cos(math.radians(self.heading))
        self.y += self.speed * time_interval * math.sin(math.radians(self.heading))
        self.altitude += self.vertical_speed * time_interval

    def change_heading(self, angle_change):
        # Change the aircraft's heading
        self.heading += angle_change

    def change_vertical_speed(self, speed_change):
        # Change the aircraft's vertical speed
        self.vertical_speed += speed_change

# Function to handle key press events
def on_key_press(event):
    if event.keysym == 'Up':
        aircraft.change_vertical_speed(10)  # Increase vertical speed
    elif event.keysym == 'Down':
        aircraft.change_vertical_speed(-10)  # Decrease vertical speed
    elif event.keysym == 'Left':
        aircraft.change_heading(-10)  # Turn left
    elif event.keysym == 'Right':
        aircraft.change_heading(10)  # Turn right

# Function to update the aircraft position and redraw the plot
def update_plot():
    aircraft.update_position(time_interval)
    aircraft_plot.set_data([aircraft.x], [aircraft.y])
    canvas.draw()
    print(f"Altitude: {aircraft.altitude} | Longitude: {aircraft.x} | Latitude: {aircraft.y}")
    root.after(int(time_interval * 1000), update_plot)

# GUI setup
root = tk.Tk()
root.title("Flight Path Simulation")

# Set the size of the simulation area (adjust as needed)
xlim, ylim = (0, 100), (0, 100)

# Create a random 2D terrain grid
terrain = np.random.randint(0, 100, size=(xlim[1], ylim[1]))

# Create a matplotlib figure and plot the random terrain
fig, ax = plt.subplots()
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_aspect('equal', adjustable='box')
ax.imshow(terrain, cmap='terrain', origin='lower', extent=[xlim[0], xlim[1], ylim[0], ylim[1]], alpha=0.7)

# Create the aircraft and plot its initial position
aircraft = Aircraft(x=10, y=10, altitude=1000, speed=5, heading=45)  # Example initial values
aircraft_plot, = ax.plot([aircraft.x], [aircraft.y], 'ro', markersize=10)

# Time interval for simulation update (adjust as needed)
time_interval = 0.1  # 0.1 second, for example

# Create the Tkinter canvas for embedding the matplotlib plot
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Bind key press events to the on_key_press function
root.bind('<KeyPress>', on_key_press)

# Start the simulation by updating the plot at regular intervals
root.after(int(time_interval * 1000), update_plot)

# Run the Tkinter main loop
root.mainloop()