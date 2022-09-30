import tkinter as tk
from tkinter.messagebox import askokcancel

from src.domain.entities import DatEntity, MatEntity
from src.view.services.frames import MainFrame

APP_WIDTH = 1292
APP_HEIGHT = 380
TEXT1 = """

Esta Aplicação is intended to serve as a utility to manage the analysis of watercourse flow monitoring data,
in control sections monitored by SonTek's SL500 and M9 equipment.

Follow the steps to use it:
1) Select a .dat file extension.
2) Enter the starting time and final time of the measurement on date-time format.
   E.g. "1989-10-39 05:30:31" .
3) Record the data into the database.
4) Select a .mat file extension, file corresponding to the measurement file of the step 2.
5) Reccor the data into the database.
6) Export the data in the desired format (.xlsx or .csv).

Code and Development:

Jamilson do Nascimento
github.com/kkcortez-nscmnt
jamil.pyhidrodev@gmail.com
---------------------------------------------------------------------------------

Development:

Gilberto Loguercio Collares
gilbertocollares@gmail.com

Guilherme Kruger Bartels
guilhermebartels@gmail.com

George Marino Soares Gonçalves
george.marino.goncalves@gmail.com
----------------------------------------------------------------------------------
Support:

Lukas dos Santos Boeira
lukasdossantosboeira@gmail.com

Arlene Fehrenbach
arlenefehrenbach@outlook..com
----------------------------------------------------------------------
Universidade Federal de Pelotas - UFPel https://portal.ufpel.edu.br
NEPE - HidroSedi http://www.hidrosedi.com
Agência de Desenvolvimento da Bacia da Lagoa Mirim - São Gonçalo.
https://wp.ufpel.edu.br/alm/banco-de-dados-da-bacia-da-lagoa-mirim/

"""


class MainApp:
    """
    Classe Principal da aplicação
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(
            "IVMDSS: Index Velocity Method's Data Storage System - Module 1"
        )
        self.root.iconbitmap("D:\TCC\index_velocity_method\img\icon.ico")
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.minsize(width=APP_WIDTH, height=APP_HEIGHT)
        self.root.resizable(1, 0)

        self.mat_entity = MatEntity()
        self.mat_entity.create_mat_table()

        self.dat_entity = DatEntity()
        self.dat_entity.create_dat_table()

        self.main_frame = MainFrame(self.root)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        def quit():
            askok_cancel = askokcancel("Attention!", "Exit Application ?")
            if askok_cancel:
                self.root.destroy()

        def about_window():
            top_abt_win = tk.Toplevel()
            top_abt_win.title("Information")
            top_abt_win.geometry("555x655")
            top_abt_win.resizable(0, 0)
            info_lbl = tk.Label(top_abt_win, text=TEXT1)
            info_lbl.grid(row=0, column=0)

        self.menu_bar.add_command(label="About", command=about_window)
        self.menu_bar.add_command(label="Exit", command=quit)
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
