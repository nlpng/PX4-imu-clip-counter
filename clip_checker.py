from __future__ import print_function

import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

import pyulog


class tkinterGUI:
    def __init__(self) -> None:
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.title("PX4 clip counter")
        root.geometry("400x400+50+100")

        frame_grid = tk.Frame(root, relief=tk.GROOVE, borderwidth=2)
        frame_grid.pack(side=tk.TOP)

        frame_file = tk.Frame(frame_grid)

        frame_file.grid(column=0, row=0, padx=5, pady=5)

        butn_select = tk.Button(
            frame_file,
            text="ULog Select",
            command=self.select_dialog,
            bg="#2196f3"
        )
        butn_select.pack(side=tk.LEFT, padx=10)

        self.cap_filename = tk.StringVar()
        textbox_cap = tk.Entry(
            frame_file,
            textvariable=self.cap_filename, width=30
        )
        textbox_cap.pack(side=tk.LEFT, padx=10)

        # abs path to .ulog
        self.ulog_abs_path = None

        separator = ttk.Separator(frame_grid, orient="horizontal")
        separator.grid(column=0, row=1, sticky="ew")

        frame_pack = tk.Frame(root, relief=tk.GROOVE, borderwidth=2)
        frame_pack.pack(side=tk.TOP, pady=5)

        butn_parser = tk.Button(
            frame_pack, text="GO", command=self.start_parser, bg="#2196f3"
        )
        butn_parser.pack(side=tk.LEFT, padx=10)

        log_label = tk.Label(frame_pack, text="OUTPUT")
        log_label.pack(side=tk.LEFT, padx=5)

        self.logbox = tk.Text(frame_pack, width=40, height=35)
        self.logbox.pack(side=tk.TOP)

        root.mainloop()

    def clip_counter(self):
        print(self.ulog_abs_path)
        ulog = pyulog.ULog(self.ulog_abs_path)

        imu_ind = 0
        for d in ulog.data_list:
            if d.name == "vehicle_imu_status":
                x = max(d.data["accel_clipping[0]"])
                y = max(d.data["accel_clipping[1]"])
                z = max(d.data["accel_clipping[2]"])
                clip_count_total = x + y + z
                imu_ind += 1
                self.pprint(f"acc {imu_ind} clip count: {clip_count_total} ({x}, {y}, {z})")

    def start_parser(self):
        if self.ulog_abs_path is None:
            self.pprint("File not valid!")
            return

        self.pprint(f"Parsing {os.path.basename(self.ulog_abs_path)} file")
        self.clip_counter()

    def select_dialog(self):
        path = os.path.abspath(os.path.dirname(__file__))
        cap_filepath = filedialog.askopenfilename(initialdir=path)
        self.ulog_abs_path = cap_filepath

        filename = os.path.basename(cap_filepath)
        self.cap_filename.set(filename)

    def pprint(self, str):
        self.logbox.insert(tk.END, str + "\n")
        self.logbox.see(tk.END)



if __name__ == "__main__":
    clip_counter = tkinterGUI()
