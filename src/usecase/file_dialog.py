import tkinter as tk
from tkinter import filedialog


class FileDiolog:
    """Caixa de dialogo com os arquivos"""

    def __init__(self) -> None:
        self.filename = None

    def _select_dat_file(self) -> str:
        """
        Diálogo para seleção de  arquivo com extensão .dat
        :param - None
        :return - String
        """
        self.filename = filedialog.askopenfilename(
            # initialdir="/",
            title=" Select a .dat extension file.",
            filetype=(("dat files", ".dat"), ("all files", ".")),
        )
        try:
            if self.filename:
                self.label_sl500_dat_path["text"] = self.filename
                print(self.filename)
                return self.filename
        except ValueError:
            tk.messagebox.showerror("Information", "Error: File type.")
            return None
        except FileNotFoundError:
            tk.messagebox.showerror("Information", "No such file found.")
            return None

    def _select_mat_file(self) -> str:
        """
        Diálogo para seleção de  arquivo com extensão .mat
        :param - None
        :return - String
        """
        self.filename = filedialog.askopenfilename(
            # initialdir="/",
            title=" Select a .dat extension file.",
            filetype=(("vel files", ".mat"), ("all files", ".")),
        )
        try:
            if self.filename:
                self.label_m9_mat_path["text"] = self.filename
                print(self.filename)
                return self.filename
        except ValueError:
            tk.messagebox.showerror("Information", "Error: File type.")
            return None
        except FileNotFoundError:
            tk.messagebox.showerror("Information", "No such file found.")
            return None
