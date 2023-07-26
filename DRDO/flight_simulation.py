import tkinter as tk
import folium
from io import BytesIO
from PIL import Image, ImageTk



def update_parameters(event):
    global longitude, latitude, altitude, velocity

    # Define the step size for parameter updates
    step_size = 0.1

    # Handle the arrow key inputs
    if event.keysym == "Up":
        altitude += step_size
    elif event.keysym == "Down":
        altitude -= step_size
    elif event.keysym == "Left":
        longitude -= step_size
    elif event.keysym == "Right":
        longitude += step_size

    # Update the GUI labels with the new parameter values
    longitude_label.config(text=f"Longitude: {longitude:.2f}")
    latitude_label.config(text=f"Latitude: {latitude:.2f}")
    altitude_label.config(text=f"Altitude: {altitude:.2f}")
    velocity_label.config(text=f"Velocity: {velocity:.2f}")

def on_key_press(event):
    # Get the key pressed from the event object
    key = event.keysym

    # Check if the key pressed is an arrow key
    if key in ["Up", "Down", "Left", "Right"]:
        # Call the update_parameters() function to adjust the parameters
        update_parameters(event)

        # Optionally, you can add additional logic or actions here if needed

        # For example, you could trigger other events or animations related to the plane movement or GUI updates.

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Flight Path Simulation")

    # Create a canvas to display the map and plane pointer
    canvas = tk.Canvas(root, width=800, height=600, bg="black")
    canvas.pack()

    # Load the plane pointer image 
    plane_image = tk.PhotoImage(file="plane.png")

    # Initial parameters 
    longitude = 0.0
    latitude = 0.0
    altitude = 10000.0
    velocity = 200.0

    # Create labels to display the parameters
    longitude_label = tk.Label(root, text=f"Longitude: {longitude}")
    latitude_label = tk.Label(root, text=f"Latitude: {latitude}")
    altitude_label = tk.Label(root, text=f"Altitude: {altitude}")
    velocity_label = tk.Label(root, text=f"Velocity: {velocity}")

    # Pack the labels to display them on the GUI
    longitude_label.pack()
    latitude_label.pack()
    altitude_label.pack()
    velocity_label.pack()

    # Bind the arrow key events to the on_key_press function
    root.bind("<KeyPress>", on_key_press)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
