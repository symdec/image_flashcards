from PIL import Image, ImageTk
import tkinter as tk
import sys
import os
import random
import argparse

COLOR1 = "cyan4"
COLOR2 = "lightgrey"
COLOR3 = "white"


def is_image(filename):
    suffixes = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]
    for suffix in suffixes:
        if filename.endswith(suffix):
            return True
    return False

def get_all_image_paths(images_directory):
    """
    Return all images paths in :images_directory: and its subdirectories
    """
    image_paths = []
    for root, dirs, files in os.walk(images_directory):
        for file in files:
            if is_image(file):
                image_paths.append(os.path.join(root, file))
    return image_paths


def get_image_caption(image_path):
    basename = os.path.basename(image_path)
    caption = ".".join(basename.split(".")[:-1]) # Remove the extension
    caption = caption.replace("_", " ") # Replace underscores with spaces
    return caption


def display_caption_or_next_image(image_widget, counter_widget, caption_widget, action_button, image_caption, image_paths):
    if caption_widget.cget("text") == "":
        display_caption(caption_widget, image_caption)
        action_button.configure(text="Next")
    else:
        display_next_image(image_widget, counter_widget, caption_widget, image_paths)
        action_button.configure(text="Show")



def display_next_image(image_widget, counter_widget, caption_widget, image_paths):
    global image_index
    global image_caption
    nb_images = len(image_paths)
    if image_index >= nb_images:
        # Display "no more image" in image_widget
        image_widget.configure(text="No more image", image=None, compound="center")
        image_widget.image = None
        image_caption = ""
        hide_caption(caption_widget)
    else:
        image_path = image_paths[image_index]
        image_caption = get_image_caption(image_path)
        image_index += 1
        # Load the first image using Pillow
        image = Image.open(image_path)  # Replace with the path to your first image
        # Convert the image for Tkinter
        image_tk = ImageTk.PhotoImage(image)
        # Update image display
        image_widget.configure(image=image_tk)
        image_widget.image = image_tk
        # Hide caption
        hide_caption(caption_widget)
        # Update counter
        counter_widget.configure(text=f"{image_index} / {nb_images}")


def display_caption(caption_widget, image_caption):
    caption_widget.configure(text=image_caption)


def hide_caption(caption_widget):
    caption_widget.configure(text="")


def main(images_directory):
    global image_index
    global image_caption
    image_index = 0
    image_caption = ""
    font = ('Helvetica', '16')

    image_paths = get_all_image_paths(images_directory)
    random.shuffle(image_paths)
    nb_images = len(image_paths)
    if nb_images == 0:
        print("No image found in", images_directory)
        sys.exit(1)

    # init the window
    window = tk.Tk()
    window.config(bg=COLOR1)
    # set the size of the window (full screen)
    screen_width = window.winfo_screenwidth()               
    screen_height = window.winfo_screenheight()               
    window.geometry("%dx%d" % (screen_width, screen_height))
    # set the name of the window
    window.title("Flashcards")
    
    # Counter widget
    counter_frame = tk.Frame(window, width=screen_width, height=(1/10)*screen_height, bg=COLOR2, relief="raised")
    counter_widget = tk.Label(counter_frame, text=f"0 / {nb_images}", bg=COLOR3, relief="raised", padx=10, pady=2, font=font)
    counter_widget.place(relx=0.5, rely=0.5, anchor="center")
    
    # Label widget to display the image
    image_frame = tk.Frame(window, width=screen_width, height=(1/2)*screen_height, bg=COLOR2)
    image_widget = tk.Label(image_frame)
    image_widget.place(relx=0.5, rely=0.5, anchor="center")

    # Caption widget
    caption_frame = tk.Frame(window, width=screen_width, height=(1/10)*screen_height, bg=COLOR2)
    caption_widget = tk.Label(caption_frame, text="", font=font, bg=COLOR2)
    caption_widget.place(relx=0.5, rely=0.5, anchor="center")

    # Action button
    button_frame = tk.Frame(window, width=screen_width, height=(3/10)*screen_height, bg=COLOR2)
    action_button = tk.Button(button_frame, text="Show", font=font, width=20, height=5, bg=COLOR1, command=lambda: display_caption_or_next_image(image_widget, counter_widget, caption_widget, action_button, image_caption, image_paths))
    action_button.place(relx=0.5, rely=0.5, anchor="center")

    counter_frame.pack(padx=10, pady=5)
    image_frame.pack(padx=10, pady=5)
    caption_frame.pack(padx=10, pady=5)
    button_frame.pack(padx=10, pady=5)

    display_next_image(image_widget, counter_widget, caption_widget, image_paths) # to display the first image
    window.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Graphical memory flashcard maker from a directory containing images.',
    )
    parser.add_argument("images_directory", help="The directory containing images")
    args = parser.parse_args()
    main(args.images_directory)