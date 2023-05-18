import PySimpleGUI as sg

import cv2
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip

from file_handler import get_next_gif_save_path, get_next_mp4_save_path


sg.theme("LightGrey1")  # Light grey theme

title_font = ("Helvetica", 18, "bold")
heading_font = ("Helvetica", 14, "bold")
normal_font = ("Helvetica", 12)

bg_color = "#F0F0F0"  # Light gray background color
title_color = "#333333"  # Dark gray title color
text_color = "#000000"  # Black text color
button_color = ("#333333", "#FFFFFF")  # Dark gray button color with white text
button_font = ("Helvetica", 12, "bold")


def crop_video(input_file, output_file, x, y, width, height):
    video = VideoFileClip(input_file)
    cropped_video = video.crop(x, y, width, height)
    cropped_video.write_videofile(output_file, codec="libx264")


def display_first_frame(video_file):
    # Open the video file
    video = cv2.VideoCapture(video_file)

    # Read the first frame
    ret, frame = video.read()

    # Convert the frame from BGR to RGB format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the first frame using matplotlib
    plt.imshow(frame_rgb)
    plt.axis("off")
    plt.show()

    # Release the video file
    video.release()


def crop_video_main(video_file, x, y, target_width, target_height):
    output_file = get_next_mp4_save_path()

    # display_first_frame(path_to_vid)
    crop_video(video_file, output_file, x, y, target_width, target_height)


def convert_to_gif(video_file, output_file):
    clip = VideoFileClip(video_file)
    clip.write_gif(output_file)


def convert_to_gif_main(input_file):
    output_file = get_next_gif_save_path()

    print("converting to gif")
    convert_to_gif(input_file, output_file)
    print("Done converting to gif")


def crop_dimensions(video_file, output_file, x, y, target_width, target_height):
    clip = VideoFileClip(video_file)

    # Crop the video using the provided coordinates and dimensions
    cropped_clip = clip.crop(x1=x, y1=y, x2=x + target_width, y2=y + target_height)

    # Write the cropped video to the output file
    cropped_clip.write_videofile(output_file, codec="libx264")


def mp4_to_gif_gui():
    layout = [
        [
            sg.Text(
                "Select an MP4 video file:", font=normal_font, text_color=title_color
            ),
        ],
        [
            sg.Text(
                "File saves to [Roaming\Py-VideoConverter\mp4_videos]:", font=normal_font, text_color=title_color
            ),
        ],
        [sg.Input(), sg.FileBrowse(font=normal_font)],
        [sg.Button("Submit", font=normal_font, button_color=button_color)],
    ]

    window = sg.Window("MP4 to gif", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Submit":
            file_path = values[0]

            convert_to_gif_main(file_path)
            sg.popup("Done converting to gif")

            window.close()
            main_gui()

    window.close()


def crop_mp4_gui():
    layout = [
        [
            sg.Text(
                "File saves to [Roaming\Py-VideoConverter\mp4_videos]:", font=normal_font, text_color=title_color
            ),
        ],
        [sg.Text("Select an MP4 video file:")],
        [sg.Input(size=(30, 1)), sg.FileBrowse()],
        [
            sg.Text("Top coord:       ", justification="left"),
            sg.InputText(key="top", size=(4, 1), justification="right"),
        ],
        [
            sg.Text("Leftmost coord:", justification="left"),
            sg.InputText(key="left", size=(4, 1), justification="right"),
        ],
        [
            sg.Text("Width:             ", justification="left"),
            sg.InputText(key="w", size=(4, 1), justification="right"),
        ],
        [
            sg.Text("Height:            ", justification="left"),
            sg.InputText(key="h", size=(4, 1), justification="right"),
        ],
        [sg.Button("Submit")],
    ]

    window = sg.Window("MP4 Video Cropper", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Submit":
            file_path = values[0]
            crop_video_main(
                video_file=file_path,
                x=values["left"],
                y=values["top"],
                target_width=values["w"],
                target_height=values["h"],
            )
            print("Cropped video")

            window.close()
            main_gui()

    window.close()


def show_mp4_regions_gui():
    layout = [
        [sg.Text("Select an MP4 video file:", font=title_font, text_color=title_color)],
        [sg.Input(), sg.FileBrowse(font=normal_font)],
        [sg.Button("Submit", font=normal_font, button_color=button_color)],
    ]

    window = sg.Window("Video Region Viewer", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Submit":
            file_path = values[0]
            display_first_frame(video_file=file_path)
            break

    window.close()


def main_gui():
    layout = [
        [sg.Text("Select a Mode:", font=title_font, text_color=title_color)],
        [
            sg.Button(
                "Convert mp4 to gif", font=button_font, button_color=button_color
            ),
            sg.Button("Crop mp4 video", font=button_font, button_color=button_color),
            sg.Button("Show mp4 regions", font=button_font, button_color=button_color),
        ],
    ]

    window = sg.Window("MP4 to gif", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Show mp4 regions":
            show_mp4_regions_gui()

        elif event == "Crop mp4 video":
            crop_mp4_gui()
        elif event == "Convert mp4 to gif":
            mp4_to_gif_gui()

    window.close()


main_gui()
