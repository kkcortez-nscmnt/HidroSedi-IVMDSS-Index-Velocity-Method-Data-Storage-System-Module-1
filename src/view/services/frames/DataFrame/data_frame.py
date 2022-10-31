import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
from typing import Type

from src.infra.config import DBConnectionHandler
from src.infra.repositories import DatEntityRepository, MatEntityRepository
from src.usecase import (
    DeleteM9Data,
    DeleteSL500Data,
    FileDiolog,
    InsertM9Data,
    InsertSl500Data,
    ExportFile,
)


class PopulateTrv:
    def populate_m9_trv(self) -> None:
        with DBConnectionHandler("DataBase.db") as cursor:
            self.m9_data_trv.delete(*self.m9_data_trv.get_children())
            query = "SELECT cod, flow_rate, area, mean_velocity FROM mat_table"
            rows = cursor.execute(query).fetchall()
            for i in rows:
                self.m9_data_trv.insert("", "end", values=i)

    def populate_sl500_trv(self) -> None:
        with DBConnectionHandler("DataBase.db") as cursor:
            self.sl500_data_trv.delete(*self.sl500_data_trv.get_children())
            query = "SELECT cod, date_time, velocity_x, level FROM dat_table"
            rows = cursor.execute(query).fetchall()
            for i in rows:
                self.sl500_data_trv.insert("", "end", values=i)


class GetCod:
    def get_m9_query_cod(self):
        for cod_item in self.m9_data_trv.selection():
            self.cod = self.m9_data_trv.item(cod_item)
            self.query_cod = self.cod["values"][0]
            return self.query_cod

    def get_sl500_query_cod(self):
        for cod_item in self.sl500_data_trv.selection():
            self.cod = self.sl500_data_trv.item(cod_item)
            self.query_cod = self.cod["values"][0]
            return self.query_cod


class FrameData(PopulateTrv, GetCod):
    """
    Frame para micro servico relacionados a arquivos
    """

    def __init__(
        self,
        parent,
        m9_data: Type[InsertM9Data],
        m9_data_delete: Type[DeleteM9Data],
        f_dialog: Type[FileDiolog],
        mat_entity_repository: Type[MatEntityRepository],
        sl500_data: Type[InsertSl500Data],
        sl500_data_delete: Type[DeleteSL500Data],
        dat_entity_repository: Type[DatEntityRepository],
        export_file: Type[ExportFile],
        query_cod=None,
    ) -> None:

        self.m9_data = m9_data
        self.m9_data_delete = m9_data_delete
        self.f_dialog = f_dialog
        self.mat_entity_repository = mat_entity_repository
        self.sl500_data = sl500_data
        self.sl500_data_delete = sl500_data_delete
        self.dat_entity_repository = dat_entity_repository
        self.export_file = export_file

        self.var_initial_datetime = tk.StringVar()
        self.var_final_datetime = tk.StringVar()

        # variavel de estado
        self.file_path_m9 = None
        self.file_path_sl500 = None
        self.query_cod = query_cod

        # Frame de contenção
        self.data_container_frame = tk.Frame(parent)
        self.data_container_frame.place(relx=0, rely=0, relheight=1, relwidth=0.998)

        ########## Serviços de Exportação ##########
        self.label_export_data = ttk.LabelFrame(
            self.data_container_frame, text="Exportar Dados:"
        )
        self.label_export_data.place(relx=0.015, rely=0.8, height=60, width=180)

        ########## Serviços de Regressão ##########
        self.label_regression = ttk.LabelFrame(
            self.data_container_frame, text=" Velocidades Indexadas - Relações:"
        )
        self.label_regression.place(relx=0.17, rely=0.8, height=60, width=263)

        ######### Botões ##########
        self.export_xlxs_btn = ttk.Button(
            self.label_export_data,
            padding=2,
            text="Como .xlsx",
            command=lambda: self.export_file.export_to_excel(self),
        )
        self.export_xlxs_btn.place(relx=0.01, rely=0.3)

        self.export_csv_btn = ttk.Button(
            self.label_export_data,
            padding=2,
            text="Como .csv",
            command=lambda: self.export_file.export_to_csv(self),
        )
        self.export_csv_btn.place(relx=0.54, rely=0.3)

        self.mmq_nivel_area = ttk.Button(
            self.label_regression,
            padding=2,
            text="Nível-Área",
            command=lambda: self.export_file.export_to_excel(self),
        )
        self.mmq_nivel_area.place(relx=0.01, rely=0.3)

        self.mmq_velmed_velx = ttk.Button(
            self.label_regression,
            padding=2,
            text="Vel méd-Vel x",
            command=lambda: self.export_file.export_to_csv(self),
        )
        self.mmq_velmed_velx.place(relx=0.34, rely=0.3)

        self.vel_index = ttk.Button(
            self.label_regression,
            padding=2,
            text="Vel Index",
            command=lambda: self.export_file.export_to_csv(self),
        )
        self.vel_index.place(relx=0.69, rely=0.3)

        # self.del_all_data_btn = ttk.Button(
        #     self.label_export_data,
        #     padding=2,
        #     text="Deletar Dados",
        #     command=lambda: [
        #         self.delete_data_from_dat_table(),
        #         self.delete_data_from_mat_table(),
        #     ],
        # )
        # self.del_all_data_btn.place(relx=0.6, rely=0.3)

        ########## Serviços dos dados do M9 ##########
        self.label_frame_m9 = ttk.LabelFrame(
            self.data_container_frame, text="Dados HydroSurveyor M9"
        )
        self.label_frame_m9.place(relx=0.015, rely=0.48, height=93, width=460)

        self.label_frame_m9_trv = ttk.LabelFrame(
            self.data_container_frame, text="View M9 Data"
        )
        self.label_frame_m9_trv.place(relx=0.70, rely=0.009, height=345, width=400)

        # __botoes__ #

        # Botão para carregar path de arquivos m9
        self.btn_m9_file = ttk.Button(
            self.label_frame_m9,
            padding=2,
            text="Arquivo .mat",
            command=self.loat_m9_file_path,
        )  # todo
        self.btn_m9_file.place(relx=0.01, rely=0.04)

        # Botão para inserir dados M9 na base de dados
        self.btn_insert_m9_data = ttk.Button(
            self.label_frame_m9,
            padding=2,
            text="Inserir Dado",
            command=self.insert_m9_data,
        )
        self.btn_insert_m9_data.place(relx=0.64, rely=0.6)

        # Botão para deletar dados M9 na base de dados
        self.btn_delete_m9_data = ttk.Button(
            self.label_frame_m9,
            padding=2,
            text="Deletar Dado",
            command=lambda: [self.delete_from_mat_table_trv(), self.populate_m9_trv()],
        )
        self.btn_delete_m9_data.place(relx=0.82, rely=0.6)

        # Label para o path dos caminhos de arquivos M9
        self.label_m9_mat_path = ttk.Label(
            self.label_frame_m9, relief="ridge", anchor="w"
        )
        self.label_m9_mat_path.place(relx=0.195, rely=0.071, height=23.6, width=366)

        self.m9_data_trv = ttk.Treeview(
            self.label_frame_m9_trv,
            columns=(1, 2, 3, 4),
            show="headings",
            height="15",
        )
        self.m9_data_trv.pack(anchor=tk.S, fill="x")
        self.m9_data_trv.heading(1, text="Cod")
        self.m9_data_trv.column(1, width=40, anchor="c")
        self.m9_data_trv.heading(2, text="Vazão (m³/s)")
        self.m9_data_trv.column(2, width=100, anchor="c")
        self.m9_data_trv.heading(3, text="Área (m²)")
        self.m9_data_trv.column(3, width=100, anchor="c")
        self.m9_data_trv.heading(4, text="Vel. Méd. (m/s)")
        self.m9_data_trv.column(4, width=100, anchor="c")

        self.m9_trv_scroll_lista = tk.Scrollbar(
            self.label_frame_m9_trv, orient="vertical"
        )
        self.m9_data_trv.configure(yscroll=self.m9_trv_scroll_lista)
        self.m9_trv_scroll_lista.place(
            relx=0.956, rely=0.098, relwidth=0.04, relheight=0.89
        )
        with DBConnectionHandler("DataBase.db") as cursor:
            query = "SELECT cod, flow_rate, area, mean_velocity FROM mat_table"
            rows = cursor.execute(query).fetchall()
            for i in rows:
                self.m9_data_trv.insert("", tk.END, values=i)

        ########## Services SL500 ##########
        self.label_frame_sl500 = ttk.LabelFrame(
            self.data_container_frame, text="Dados SideLooker 500"
        )
        self.label_frame_sl500.place(relx=0.015, rely=0.009, height=140, width=460)

        self.label_frame_sl500_trv = ttk.LabelFrame(
            self.data_container_frame, text="View SL500 Data"
        )
        self.label_frame_sl500_trv.place(relx=0.38, rely=0.009, height=345, width=400)

        # Entrada Data Inicial
        self.entry_initial_datetime = ttk.Entry(
            self.label_frame_sl500, textvariable=self.var_initial_datetime
        )
        self.entry_initial_datetime.place(relx=0.185, rely=0.45, width=185)
        self.entry_initial_datetime.insert(16, "YYYY-mm-dd HH:MM:SS")
        self.entry_initial_datetime.focus()

        # Entrada Data Final
        self.entry_final_datetime = ttk.Entry(
            self.label_frame_sl500, textvariable=self.var_final_datetime
        )
        self.entry_final_datetime.place(relx=0.185, rely=0.75, width=185)
        self.entry_final_datetime.insert(16, "YYYY-mm-dd HH:MM:SS")

        # Botão Load SL500 Data
        self.btn_sl500_file = ttk.Button(
            self.label_frame_sl500,
            padding=2,
            text=" Arquivo .dat",
            command=self.load_sl500_file_data,
        )
        self.btn_sl500_file.place(relx=0.01, rely=0.04)

        # Botão Insert SL500 Data
        self.btn_insert_sl500_data = ttk.Button(
            self.label_frame_sl500,
            padding=2,
            text="Inserir Dado",
            command=self.insert_sl500_data,
        )
        self.btn_insert_sl500_data.place(relx=0.64, rely=0.72)

        # Botão Delete SL500 Data
        self.btn_delete_sl500_data = ttk.Button(
            self.label_frame_sl500,
            padding=2,
            text="Deletar Dado",
            command=lambda: [
                self.delete_from_dat_table_trv(),
                self.populate_sl500_trv(),
            ],
        )
        self.btn_delete_sl500_data.place(relx=0.821, rely=0.72)

        # Rotulo Datetime Incial
        self.label_initial_datetime = ttk.Label(
            self.label_frame_sl500, text="Data Inicial:"
        )
        self.label_initial_datetime.place(relx=0.02, rely=0.47, height=23)
        # Rotulo Datetime final
        self.label_final_datetime = ttk.Label(
            self.label_frame_sl500, text="Data Final:"
        )
        self.label_final_datetime.place(relx=0.02, rely=0.75, height=23)

        # Rotulo Label SL500 Path
        self.label_sl500_dat_path = ttk.Label(
            self.label_frame_sl500, relief="ridge", anchor="w"
        )
        self.label_sl500_dat_path.place(relx=0.190, rely=0.063, height=23, width=367)

        # SL500 treeview
        self.sl500_data_trv = ttk.Treeview(
            self.label_frame_sl500_trv,
            columns=(1, 2, 3, 4),
            show="headings",
            height="15",
        )
        self.sl500_data_trv.pack(anchor=tk.S, fill="x")
        self.sl500_data_trv.heading(1, text="Cod")
        self.sl500_data_trv.column(1, width=40, anchor="c")
        self.sl500_data_trv.heading(2, text="Date Time")
        self.sl500_data_trv.column(2, width=100, anchor="c")
        self.sl500_data_trv.heading(3, text="Vel. X (m/s)")
        self.sl500_data_trv.column(3, width=100, anchor="c")
        self.sl500_data_trv.heading(4, text="Nível (m)")
        self.sl500_data_trv.column(4, width=100, anchor="c")

        self.sl500_trv_scroll_lista = tk.Scrollbar(
            self.label_frame_sl500_trv, orient="vertical"
        )
        self.sl500_data_trv.configure(yscroll=self.sl500_trv_scroll_lista)
        self.sl500_trv_scroll_lista.place(
            relx=0.956, rely=0.098, relwidth=0.04, relheight=0.89
        )
        with DBConnectionHandler("DataBase.db") as cursor:
            query = "SELECT cod, date_time, velocity_x, level FROM dat_table"
            rows = cursor.execute(query).fetchall()
            for i in rows:
                self.sl500_data_trv.insert("", tk.END, values=i)

    def loat_m9_file_path(self) -> None:
        """
        Utiliza o UseCase FileDialog para obter o path de arquivos .mat e
        configura a variavel de estado.
        :param - None
        :return - None
        """
        self.m9_file_path = self.f_dialog._select_mat_file(self)
        self.file_path_m9 = self.m9_file_path
        print(f"Returned Path: {self.file_path_m9}")
        return None

    def get_m9_data(self) -> str:
        """
        Retorna a string path de arquivos .mat
        :param - None
        :return - String
        """
        return self.file_path_m9

    def insert_m9_data(self):
        """
        Utiliza o UseCase InsertM9Data para realizar o registro
        na m9_table.
        :param - None
        :return - None
        """
        self.file_path = self.get_m9_data()
        try:
            if self.file_path:
                self.m9_data._insert_m9_data_to_data_base(self, self.file_path)
                messagebox.showinfo("Info!", "Dado inserido!")
                self.populate_m9_trv()
                return None
        except:
            messagebox.showerror(
                "Value Error",
                "Deve-se inserir um registro .dat com correspondência relacionada antes da inserção!",
            )

    def delete_data_from_mat_table(self):
        """
        Utiliza o UseCase DeleteM9Data para apagar todos os registros
        na m9_table.
        """
        askokcancel = messagebox.askokcancel("Attention!", "Deletar dado?")
        try:
            if askokcancel:
                self.m9_data_delete._delete_m9_data_to_data_base(self)
                self.showinfo = messagebox.showinfo("Info", "Dados Deletados!")
                self.populate_m9_trv()
                return None

        except:
            return None

    def delete_from_mat_table_trv(self):
        """
        Utiliza o UseCase DeleteM9Data para apagar todos os registros
        na m9_table.
        """
        for cod_item in self.m9_data_trv.selection():
            self.cod = self.m9_data_trv.item(cod_item)
            self.query_cod = self.cod["values"][0]
        print(f"Registro selecionado {self.query_cod} ")
        askokcancel = messagebox.askokcancel("Attention!", "Deletar dado?")
        print(askokcancel)
        try:
            if askokcancel:
                with DBConnectionHandler(file_name="DataBase.db") as cursor:
                    if self.query_cod is not None:
                        print(self.query_cod)
                        self.query_cod = str(self.query_cod)
                        cursor.execute(
                            """ DELETE FROM mat_table WHERE cod = ? """,
                            (self.query_cod,),
                        )
                        self.populate_m9_trv()
                        self.query_cod = None
                        print("Data Deletada")
                        return None
                    else:
                        messagebox.showerror("ERROR", "Selecione uma linha no View M9")
                        return None
        except:
            print(f"Algo deu errado {self.query_cod}")
            messagebox.showerror("ERROR", "Selecione uma linha no View M9")
            return None

    def set_initial_datetime(self) -> str:
        """
        Retorna string com as data fornecida pelo usuario
        :param - None
        :return  - String
        """

        self.initial_time = self.entry_initial_datetime.get()
        print(self.initial_time)
        try:
            if self.initial_time:
                date_format = "%Y-%m-%d %H:%M:%S"
                res = bool(datetime.strptime(self.initial_time, date_format))
                if res:
                    print(f"returned initial datetime: {self.initial_time}")
                    return self.initial_time
        except ValueError:
            messagebox.showerror("Information", "Error: Formato inválido")

    def set_final_datetime(self) -> str:
        """
        Retorna string com a data fornecida pelo usuario
        :param - None
        :return  - String
        """

        self.final_time = self.entry_final_datetime.get()
        try:
            if self.final_time:
                date_format = "%Y-%m-%d %H:%M:%S"
                res = bool(datetime.strptime(self.final_time, date_format))
                if res:
                    print(f"returned final datetime: {self.final_time}")
                    return self.final_time
        except ValueError:
            messagebox.showerror("Information", "Error: Formato inválido")

    def load_sl500_file_data(self):
        """
        Utiliza o UseCase FileDialog para obter o path de arquivos .dat e
        configura a variavel de estado.
        :param - None
        :return - None
        """
        self.sl500_file_path = self.f_dialog._select_dat_file(self)
        self.file_path_sl500 = self.sl500_file_path
        print(f"Returned path: {self.file_path_sl500}")
        return None

    def get_sl500_file_path(self):
        """
        Retorna a string path de arquivos .dat
        :param - None
        :return - String
        """
        return self.file_path_sl500

    def insert_sl500_data(self):
        """
        Utiliza o UseCase InsertSL500Data para realizar o registro
        na DataBase
        :param - None
        :return - None
        """
        self.file_path = self.get_sl500_file_path()
        self.initial_time = self.set_initial_datetime()
        self.final_time = self.set_final_datetime()
        try:
            self.sl500_data._insert_sl500_data_to_data_base(
                self, self.file_path, self.initial_time, self.final_time
            )
            self.showinfo = messagebox.showinfo("Info!", "Dado Inserido!")
            self.populate_sl500_trv()
        except:
            self.showerror = messagebox.showerror(
                "Error", "Dado não encontrado no intervalo de tempo especificado"
            )

        return None

    def delete_data_from_dat_table(self):
        """
        Utiliza o UseCase DeleteSL500Data para apagar todos os registros
        na sl500_table.
        """
        self.askokcancel = messagebox.askokcancel("Attention!", "Deletar dados ?")
        try:
            if self.askokcancel:
                self.sl500_data_delete._delete_SL500_data_to_data_base(self)
                self.showinfo = messagebox.showinfo(
                    "Info", " Dados deletados do banco de dados!"
                )
                self.populate_sl500_trv()
                return None
        except:
            return None

    def delete_from_dat_table_trv(self):
        """
        Utiliza o UseCase DeleteM9Data para apagar todos os registros
        na dat_table.
        """
        for cod_item in self.sl500_data_trv.selection():
            self.cod = self.sl500_data_trv.item(cod_item)
            self.query_cod = self.cod["values"][0]
        print(f"Registro selecionado {self.query_cod} ")
        askokcancel = messagebox.askokcancel("Attention!", "Deletar dados?")
        print(askokcancel)
        try:
            if askokcancel:
                with DBConnectionHandler(file_name="DataBase.db") as cursor:
                    if self.query_cod is not None:
                        print(self.query_cod)
                        self.query_cod = str(self.query_cod)
                        cursor.execute(
                            """ DELETE FROM dat_table WHERE cod = ? """,
                            (self.query_cod,),
                        )
                        self.query_cod = None
                        return None
                    else:
                        messagebox.showerror(
                            "ERROR", "Selecione uma linha na View SL500"
                        )
                        return None
        except:
            print(f"Algo deu errado {self.query_cod}")
            messagebox.showerror("ERROR", "Selecione uma linha na View SL500")
            return None
