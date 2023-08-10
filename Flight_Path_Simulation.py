import tkinter as tk
import time
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

            self.x = min(max(new_x, 0), xlim[1])
            self.y = min(max(new_y, 0), ylim[1])

            self.altitude += self.vertical_speed * time_interval
            self.flight_path.append((self.x, self.y))


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
    elif key == 'z':
        zoom_in()
    elif key == 'x':
        zoom_out()
    elif key == 'r':
        reset_aircraft()


def toggle_pause():
    aircraft.paused = not aircraft.paused


def reset_aircraft():
    aircraft.x = 100
    aircraft.y = 100
    aircraft.altitude = 100
    aircraft.speed = 5
    aircraft.heading = 45
    aircraft.vertical_speed = 0
    aircraft.flight_path = [(aircraft.x, aircraft.y)]


def on_scroll(event):
    if event.delta > 0:
        zoom_in()
    else:
        zoom_out()


def zoom_in():
    ax.set_xlim(ax.get_xlim()[0] * 0.9, ax.get_xlim()[1] * 0.9)
    ax.set_ylim(ax.get_ylim()[0] * 0.9, ax.get_ylim()[1] * 0.9)
    canvas.draw()


def zoom_out():
    ax.set_xlim(ax.get_xlim()[0] * 1.1, ax.get_xlim()[1] * 1.1)
    ax.set_ylim(ax.get_ylim()[0] * 1.1, ax.get_ylim()[1] * 1.1)
    canvas.draw()


def main():
    global aircraft
    global ax, canvas

    root = tk.Tk()
    root.title("Flight Path Simulation")

    fig, ax = plt.subplots()
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    ax.set_aspect('equal', adjustable='box')

    terrain_img = mpimg.imread("mapImage.png")
    ax.imshow(terrain_img, extent=[0, 5000, 0, 5000])

    aircraft = Aircraft(x=100, y=100, altitude=100, speed=5, heading=45)
    aircraft_img = mpimg.imread('aircraft.png')
    aircraft_image = ax.imshow(aircraft_img,
                               extent=[aircraft.x - 10, aircraft.x + 10, aircraft.y - 10, aircraft.y + 10],
                               origin='upper')

    time_interval = 0.05

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

            canvas.draw_idle()

        info_label.config(
            text=f"Altitude: {aircraft.altitude:.2f} | X-coordinate: {aircraft.x:.2f} | Y-coordinate: {aircraft.y:.2f} | Speed: {aircraft.speed:.2f}")

        # Save data every 5 minutes
        if int(time.time() - start_time) % 300 == 0:
            with open("flight_data.txt", "a") as file:
                file.write(
                    f"Altitude: {aircraft.altitude:.2f} | X-coordinate: {aircraft.x:.2f} | Y-coordinate: {aircraft.y:.2f} | Speed: {aircraft.speed:.2f}\n")

        root.after(int(time_interval * 1000), update_plot)

    start_time = time.time()  # Record the start time

    root.bind('<KeyPress>', on_key)
    root.bind('<MouseWheel>', on_scroll)

    root.after(int(time_interval * 1000), update_plot)
    root.mainloop()


if __name__ == "__main__":
    xlim, ylim = (0, 1000), (0, 1000)
    main()
