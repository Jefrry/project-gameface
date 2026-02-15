import logging
import tkinter
import webbrowser

import customtkinter

from src.config_manager import ConfigManager
from src.gui.frames.safe_disposable_frame import SafeDisposableFrame

logger = logging.getLogger("PageAbout")

LINK_COLOR = "#1A73E8"
TITLE_SIZE = 20
TEXT_SIZE = 14
SMALL_TEXT_SIZE = 12


class PageAbout(SafeDisposableFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        logging.info("Create PageAbout")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(10, weight=1)

        row = 0

        # Page title
        title_label = customtkinter.CTkLabel(
            master=self,
            text="About",
            anchor="w",
        )
        title_label.cget("font").configure(size=TITLE_SIZE, weight="bold")
        title_label.grid(row=row, column=0, padx=30, pady=(25, 15), sticky="nw")
        row += 1

        # Application name and version
        version = ConfigManager().version
        app_name_label = customtkinter.CTkLabel(
            master=self,
            text=f"Project Gameface  v{version}",
            anchor="w",
        )
        app_name_label.cget("font").configure(size=16, weight="bold")
        app_name_label.grid(row=row, column=0, padx=30, pady=(10, 5), sticky="nw")
        row += 1

        # Description
        desc_text = (
            "Project Gameface helps gamers control their mouse cursor "
            "using head movement and facial gestures.\n\n"
            "Originally created by Google, this application uses MediaPipe "
            "Face Landmark Detection to track facial expressions and translate "
            "them into mouse and keyboard actions."
        )
        desc_label = customtkinter.CTkLabel(
            master=self,
            text=desc_text,
            wraplength=500,
            justify=tkinter.LEFT,
            anchor="w",
        )
        desc_label.cget("font").configure(size=TEXT_SIZE)
        desc_label.grid(row=row, column=0, padx=30, pady=(5, 15), sticky="nw")
        row += 1

        # Separator
        sep1 = customtkinter.CTkFrame(master=self, height=1, fg_color="gray80")
        sep1.grid(row=row, column=0, padx=30, pady=5, sticky="ew")
        row += 1

        # Author section
        author_title = customtkinter.CTkLabel(
            master=self,
            text="Author",
            anchor="w",
        )
        author_title.cget("font").configure(size=16, weight="bold")
        author_title.grid(row=row, column=0, padx=30, pady=(15, 5), sticky="nw")
        row += 1

        author_name = customtkinter.CTkLabel(
            master=self,
            text="Egor Ilin",
            anchor="w",
        )
        author_name.cget("font").configure(size=TEXT_SIZE)
        author_name.grid(row=row, column=0, padx=30, pady=(0, 5), sticky="nw")
        row += 1

        # GitHub link
        github_url = "https://github.com/Jefrry/project-gameface"
        github_link = customtkinter.CTkLabel(
            master=self,
            text=github_url,
            text_color=LINK_COLOR,
            cursor="hand2",
            anchor="w",
        )
        github_link.cget("font").configure(size=SMALL_TEXT_SIZE)
        github_link.bind("<Button-1>", lambda e: webbrowser.open(github_url))
        github_link.grid(row=row, column=0, padx=30, pady=(0, 15), sticky="nw")
        row += 1

        # Separator
        sep2 = customtkinter.CTkFrame(master=self, height=1, fg_color="gray80")
        sep2.grid(row=row, column=0, padx=30, pady=5, sticky="ew")
        row += 1

        # Technology section
        tech_title = customtkinter.CTkLabel(
            master=self,
            text="Technology",
            anchor="w",
        )
        tech_title.cget("font").configure(size=16, weight="bold")
        tech_title.grid(row=row, column=0, padx=30, pady=(15, 5), sticky="nw")
        row += 1

        tech_text = (
            "MediaPipe Face Landmark Detection API\n"
            "MediaPipe BlazeFace Model\n"
            "MediaPipe FaceMesh Model\n"
            "MediaPipe Blendshape V2 Model"
        )
        tech_label = customtkinter.CTkLabel(
            master=self,
            text=tech_text,
            justify=tkinter.LEFT,
            anchor="w",
            text_color="gray40",
        )
        tech_label.cget("font").configure(size=SMALL_TEXT_SIZE)
        tech_label.grid(row=row, column=0, padx=30, pady=(0, 15), sticky="nw")
        row += 1

        # Disclaimer at bottom
        disclaimer = customtkinter.CTkLabel(
            master=self,
            text="Disclaimer: Project Gameface is not intended for medical use.",
            text_color="gray60",
            anchor="w",
        )
        disclaimer.cget("font").configure(size=SMALL_TEXT_SIZE)
        disclaimer.grid(row=row, column=0, padx=30, pady=(5, 20), sticky="sw")
