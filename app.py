import tkinter as tk
from tkinter.messagebox import askokcancel

from src.domain.entities import DatEntity, MatEntity
from src.view.services.frames import MainFrame

APP_WIDTH = 1292
APP_HEIGHT = 380
TEXT1 = """

O objetivo desta aplicação é funcionar como um utilitário para dar suporte ao tratamento de dados
obtidos pelos equipamentos acústicos de effeito Doppler SideLooker 500 e HydroSurveyor M9 da marca
SonTek.

Execute os seguintes passos para usá-lo:
1) Selecione um arquivo de extensão .dat proveniente do equipamento SL500.
2) Insira as datas inicial e final das medição realizada pelo equipamento M9 no formato date-time.
   Ex: "1989-10-39 05:30:31" .
3) Registre o dado no banco de dados.
4) Selecione um arquivo de extensção .mat proveniente do equimanto M9 e que se relacione com o arquivo
selecionado no passo 2.
5) Registre o dado no banco de dados.
6) Exporte os dados registrados em arquivo com extensão desejada (.xlsx ou .csv)

Código fonte e desenvolvimento:

Jamilson do Nascimento
github.com/kkcortez-nscmnt
jamil.pyhidrodev@gmail.com
---------------------------------------------------------------------------------
Desenvolvimento:
Gilberto Loguercio Collares
gilbertocollares@gmail.com

Guilherme Kruger Bartels
guilhermebartels@gmail.com

George Marino Soares Gonçalves
george.marino.goncalves@gmail.com
----------------------------------------------------------------------------------
Suporte:
Lukas dos Santos Boeira
lukasdossantosboeira@gmail.com

Arlene Fehrenbach
arlenefehrenbach@outlook.com
----------------------------------------------------------------------
icon : "https://www.flaticon.com/free-icons/air-flow" title="air flow icons"
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
            "STAMVI: Sistema de Tratamento e Armazenamento de dados para a Aplicação do Método das Velocidades Indexadas"
        )
        self.root.iconbitmap("D:\TCC\index_velocity_method\img\icon.ico")
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.minsize(width=APP_WIDTH, height=APP_HEIGHT)
        self.root.resizable(0, 0)

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
            top_abt_win.title("Informações")
            top_abt_win.geometry("600x730")
            top_abt_win.resizable(0, 0)
            info_lbl = tk.Label(top_abt_win, text=TEXT1)
            info_lbl.grid(row=0, column=0)

        self.menu_bar.add_command(label="Info", command=about_window)
        self.menu_bar.add_command(label="Sair", command=quit)
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
