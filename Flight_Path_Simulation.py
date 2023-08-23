import tkinter as tk
import time
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from gmplot import gmplot
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
        aircraft.heading += 1
    elif key == 'Right':
        aircraft.heading -= 1
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
    aircraft.speed = 10
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

def update_radar_angle(angle):
    global radar_angle
    radar_angle = angle


def main():
    global aircraft
    global ax, canvas, gmap

    root = tk.Tk()
    root.title("Flight Path Simulation")

    fig, ax = plt.subplots()
    ax.set_xlim(0, 5000)
    ax.set_ylim(0, 5000)
    ax.set_aspect('equal', adjustable='box')

    terrain_img = mpimg.imread("mapImage.png")
    ax.imshow(terrain_img, extent=[0, 5000, 0, 5000])

    aircraft = Aircraft(x=100, y=100, altitude=100, speed=5, heading=45)
    time_interval = 0.05
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    info_label = tk.Label(root, text="", font=("Arial", 12))
    info_label.pack()

    flight_path_plot, = ax.plot([], [], 'g-', linewidth=2)  # Flight path plot
    aircraft_position_dot, = ax.plot([], [], 'ro')  # Aircraft position dot

    # Initialize gmplot instance with center coordinates
    gmap = gmplot.GoogleMapPlotter(aircraft.x, aircraft.y, 13)  # Adjust zoom level as needed

    # Define the radar station coordinates
    radar_station = (1500, 2000)  # Replace with your desired radar station coordinates
    # Plot the radar station on the map
    gmap.marker(radar_station[0], radar_station[1], color='blue', title='Radar Station')
    # Initialize radar line plot
    radar_line, = ax.plot([], [], 'b--', linewidth=0.5)

    # Load the antenna image
    antenna_img = mpimg.imread("radar.png")
    # Display the antenna image at the radar station location
    radar_image = ax.imshow(antenna_img, extent=[radar_station[0] - 50, radar_station[0] + 50, radar_station[1] - 50, radar_station[1] + 50])
    radar_angle = 0  # Initialize radar angle
    radar_angle_scale = tk.Scale(root, from_=0, to=360, orient="horizontal", label="Radar Angle", command=update_radar_angle)
    radar_angle_scale.pack()

    def update_plot():
        old_position = (aircraft.x, aircraft.y)
        aircraft.update_position(time_interval)

        distance = math.sqrt((aircraft.x - radar_station[0]) ** 2 + (aircraft.y - radar_station[1]) ** 2)

        # Display the distance label
        distance_label = ax.text(
            radar_station[0] + 10,
            radar_station[1] + 10,
            f"Distance: {distance:.2f}",
            fontsize=10,
            color='black',
            backgroundcolor='white',  # Add a white background color
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'),  # Customize the background box
            verticalalignment='bottom'  # Position the label above the radar station
        )

        aircraft.update_position(time_interval)

        if (aircraft.x, aircraft.y) != old_position:
            flight_path_plot.set_data(*zip(*aircraft.flight_path))
            aircraft_position_dot.set_data(aircraft.x, aircraft.y)  # Update aircraft position dot

            # Update radar line plot
            radar_line.set_data([aircraft.x, radar_station[0]], [aircraft.y, radar_station[1]])

            canvas.draw_idle()

        info_label.config(
            text=f"Altitude: {aircraft.altitude:.2f} | X-coordinate: {aircraft.x:.2f} | Y-coordinate: {aircraft.y:.2f} | Speed: {aircraft.speed:.2f}")

        if int(time.time() - start_time) % 300 == 0:
            with open("flight_data.txt", "a") as file:
                file.write(
                    f"Altitude: {aircraft.altitude:.2f} | X-coordinate: {aircraft.x:.2f} | Y-coordinate: {aircraft.y:.2f} | Speed: {aircraft.speed:.2f}\n")

        root.after(int(time_interval * 1000), update_plot)

        angle_to_radar = math.degrees(math.atan2(aircraft.y - radar_station[1], aircraft.x - radar_station[0]))
        relative_angle = (radar_angle - angle_to_radar) % 360

        # Display the angle label
        angle_label = ax.text(
            radar_station[0] + 10,
            radar_station[1] - 20,
            f"Angle to Radar: {relative_angle:.2f}°",
            fontsize=10,
            color='black',
            backgroundcolor='white',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'),
            verticalalignment='top'
        )

    start_time = time.time()  # Record the start time
    root.bind('<KeyPress>', on_key)
    root.bind('<MouseWheel>', on_scroll)

    root.after(int(time_interval * 1000), update_plot)
    root.mainloop()


if __name__ == "__main__":
    xlim, ylim = (0, 5000), (0, 5000)
    main()
