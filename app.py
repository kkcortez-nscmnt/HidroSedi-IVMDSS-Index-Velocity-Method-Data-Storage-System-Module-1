import tkinter as tk

from src.domain.entities import DatEntity, MatEntity
from src.view.services.frames import MainFrame

APP_WIDTH = 1292
APP_HEIGHT = 358


class MainApp:
    """
    Classe Principal da aplicação
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(
            "HidroSedi - IVMDSS: Index Velocity Method's Data Storage System - Module 1"
        )
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.minsize(width=APP_WIDTH, height=APP_HEIGHT)
        self.root.resizable(1, 0)

        self.mat_entity = MatEntity()
        self.mat_entity.create_mat_table()

        self.dat_entity = DatEntity()
        self.dat_entity.create_dat_table()

        self.main_frame = MainFrame(self.root)

        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
