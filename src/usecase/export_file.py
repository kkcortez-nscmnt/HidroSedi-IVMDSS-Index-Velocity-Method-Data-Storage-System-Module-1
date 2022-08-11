from tkinter import filedialog

import pandas as pd
from src.infra.config import DBConnectionHandler


class ExportFile:
    """
    Classe para exportação dos arquivos em .xlsx e csv
    """

    def export_to_excel(self) -> None:
        """
        Exporta arquivo em formato xlsx
        :param - None
        return - None
        """

        with DBConnectionHandler(file_name="DataBase.db") as cursor:
            self.mat_table = cursor.execute(
                """
                SELECT * FROM mat_table
                """
            ).fetchall()

            self.dat_table = cursor.execute(
                """
                SELECT * FROM dat_table
                """
            ).fetchall()

            self.dt_mat = pd.DataFrame(
                self.mat_table,
                columns=["cod", "Total_Q (m3/s)", "Area(m2)", "Mean Velocity(m/s)"],
            )

            self.dt_dat = pd.DataFrame(
                self.dat_table,
                columns=["cod", "DateTime", "Veocity_X(m/s)", "Level(m)"],
            )
            try:
                with filedialog.asksaveasfile(
                    mode="w", defaultextension=".xlsx"
                ) as file:
                    self.df_final = pd.merge(self.dt_dat, self.dt_mat, how="outer")
                    self.df_final_xlsx = self.df_final.to_excel(file.name, index=False)
            except AttributeError:
                print("Cancelled Save")

    def export_to_csv(self) -> None:
        """
        Exporta arquivo em formato xlsx
        :param - None
        return - None
        """

        with DBConnectionHandler(file_name="DataBase.db") as cursor:
            self.mat_table = cursor.execute(
                """
                SELECT * FROM mat_table
                """
            ).fetchall()

            self.dat_table = cursor.execute(
                """
                SELECT * FROM dat_table
                """
            ).fetchall()

            self.dt_mat = pd.DataFrame(
                self.mat_table,
                columns=["cod", "Total_Q (m3/s)", "Area(m2)", "Mean Velocity(m/s)"],
            )

            self.dt_dat = pd.DataFrame(
                self.dat_table,
                columns=["cod", "DateTime", "Veocity_X(m/s)", "Level(m)"],
            )
            try:
                with filedialog.asksaveasfile(
                    mode="w", defaultextension=".csv"
                ) as file:
                    self.df_final = pd.merge(self.dt_dat, self.dt_mat, how="outer")
                    self.df_final_xlsx = self.df_final.to_csv(file.name, index=False)
            except AttributeError:
                print("Cancelled Save")
