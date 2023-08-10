import tkinter as tk
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.transforms import Affine2D

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
        if not self.paused:
            new_x = self.x + self.speed * time_interval * math.cos(math.radians(self.heading))
            new_y = self.y + self.speed * time_interval * math.sin(math.radians(self.heading))

            if 0 <= new_x <= xlim[1]:
                self.x = new_x
            elif new_x < 0:
                self.x = 0
            else:
                self.x = xlim[1]

            if 0 <= new_y <= ylim[1]:
                self.y = new_y
            elif new_y < 0:
                self.y = 0
            else:
                self.y = ylim[1]

            self.altitude += self.vertical_speed * time_interval
            self.flight_path.append((self.x, self.y))


def reset_aircraft():
    aircraft.x = 0
    aircraft.y = 0
    aircraft.altitude = 0
    aircraft.speed = 1
    aircraft.heading = 45
    aircraft.vertical_speed = 0
    aircraft.flight_path = [(aircraft.x, aircraft.y)]


def on_key(event):
    key = event.keysym
    if key == 'Up':
        aircraft.vertical_speed += 1
    elif key == 'Down':
        aircraft.vertical_speed -= 1
    elif key == 'Left':
        aircraft.heading += 10
    elif key == 'Right':
        aircraft.heading -= 10
    elif key == 'a':
        aircraft.speed += 1
    elif key == 's':
        aircraft.speed -= 1
    elif key == 'p':
        toggle_pause()
    elif key == 'r':  # Add this condition for the reset key
        reset_aircraft()

def toggle_pause():
    aircraft.paused = not aircraft.paused

def main():
    global aircraft
    global xlim, ylim, ax, canvas

    root = tk.Tk()
    root.title("Flight Path Simulation")

    xlim, ylim = (0, 500), (0, 500)

    fig, ax = plt.subplots()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal', adjustable='box')

    terrain_img = mpimg.imread("mapImage.png")
    ax.imshow(terrain_img, extent=[0, xlim[1], 0, ylim[1]])

    aircraft = Aircraft(x=0, y=0, altitude=0, speed=1, heading=45)
    aircraft_img = mpimg.imread('aircraft.png')
    aircraft_image = ax.imshow(aircraft_img, extent=[aircraft.x - 10, aircraft.x + 10, aircraft.y - 10, aircraft.y + 10], origin='upper')

    time_interval = 0.1

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    info_label = tk.Label(root, text="", font=("Arial", 12))
    info_label.pack()

    flight_path_plot, = ax.plot([], [], 'g-', linewidth=2)  # Flight path plot

    def update_plot():
        old_position = (aircraft.x, aircraft.y)

        aircraft.update_position(time_interval)

        if (aircraft.x, aircraft.y) != old_position:
            aircraft_image.set_extent([aircraft.x - 10, aircraft.x + 10, aircraft.y - 10, aircraft.y + 10])
            trans = Affine2D().rotate_deg(90 - aircraft.heading)
            aircraft_image.set_transform(trans + ax.transData)

            flight_path_plot.set_data(*zip(*aircraft.flight_path))

            canvas.draw_idle()  # Use draw_idle() instead of draw() to avoid blocking

        info_label.config(
            text=f"Altitude: {aircraft.altitude:.2f} | X-coordinate: {aircraft.x:.2f} | Y-coordinate: {aircraft.y:.2f} | Speed: {aircraft.speed:.2f}")

        root.after(int(time_interval * 1000), update_plot)

    root.bind('<KeyPress>', on_key)

    root.after(int(time_interval * 1000), update_plot)  # Start the update loop
    root.mainloop()

if __name__ == "__main__":
    main()


