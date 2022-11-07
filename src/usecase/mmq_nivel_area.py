import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from src.infra.repositories import DatEntityRepository, MatEntityRepository
from yellowbrick.regressor import ResidualsPlot


class MinimosQuadradosNivelArea(LinearRegression):
    """
    Método dos mínimos quadrados considerando relação level-area
    """

    def __init__(self) -> None:
        self.mat_repository = MatEntityRepository()
        self.dat_repository = DatEntityRepository()
        self.lista_area = None
        self.lista_nivel = None
        self.mmq_nivel_area = None

    def configura_var_dependente_area(self) -> np.array:
        """
        Retorna matriz da variavel independente area
        :param - None
        :return - matriz np.array
        """

        self.lista_area = self.mat_repository.select_area_from_mat_table()
        self.lista_area = np.array(self.lista_area)
        self.mtx_area = self.lista_area.reshape(-1, 1)
        return self.mtx_area

    def configura_var_independente_nivel(self) -> np.array:
        """
        Retorna matriz da variavel independente nivel
        :param - None
        :return - matriz np.array
        """
        self.lista_nivel = self.dat_repository.select_level_from_dat_table()
        self.lista_nivel = np.array(self.lista_nivel)
        self.mtx_nivel = self.lista_nivel.reshape(-1, 1)
        return self.mtx_nivel

    def minimos_quadrados_nivel_area(self, mtx_nivel, mtx_area) -> None:
        """
        Executa o ajuste da reta pelo metodo dos minimos quadrados.
        :param - mtx_nivel = matriz numpy com os valores de nível.
               - mtx_area = matriz numpy com os valores de area.
        :return - None
        """

        self.mtx_nivel = mtx_nivel
        self.mtx_area = mtx_area
        self.mmq_nivel_area = LinearRegression()
        self.mmq_nivel_area.fit(mtx_nivel, mtx_area)
        return None

    def obter_coef_linear(self) -> float:
        """
        Retorna o coeficiente linear da reta
        :param - None
        :return - Float
        """
        self.coef_linear = self.mmq_nivel_area.intercept_
        return float(round(self.coef_linear[0], 3))

    def obter_coef_angular(self) -> float:
        """
        Retorna o coeficiente angular da reta
        :param - None
        :return - float
        """
        self.coef_angular = self.mmq_nivel_area.coef_
        return float(round(self.coef_angular[0][0], 3))

    def obter_variaveis_estimadas_de_area(self, var_independente) -> np.ndarray:
        """
        Realiza as previsões de acordo com a reta ajustada
        """
        self.var_independente_nivel = var_independente
        self.var_estimada = self.mmq_nivel_area.predict(self.var_independente_nivel)
        return self.var_estimada

    def plotar_grafico_do_ajuste_nivel_area(self, eixo_x, eixo_y, estimados) -> None:
        """
        Plota o gráfico do ajuste linear
        :param - eixo_x = variavel independente
               - eixo_y = variavel dependente
               - estimados = variaveis estimadas atraves do ajuste da reta
        :return - None
        """
        self.eixo_x = eixo_x
        self.eixo_y = eixo_y
        self.coef_cor = self.mmq_nivel_area.score(self.eixo_x, self.eixo_y)
        self.eixo_x = eixo_x.ravel()
        self.eixo_y = eixo_y.ravel()
        self.estimados = estimados.ravel()

        self.grafico = px.scatter(
            x=self.eixo_x,
            y=self.eixo_y,
            title=f"Área(m²) = {round(self.coef_angular[0][0],3)} * nível(m) + {round(self.coef_linear[0],3)} R² = {round(self.coef_cor, 3)} ",
        )
        self.grafico.add_scatter(
            x=self.eixo_x,
            y=self.estimados,
            name="Reta Ajustada",
        )
        self.grafico.update_layout(xaxis_title="Nível (m)", yaxis_title="Área (m²)")
        self.grafico.show()

    def plotar_grafico_residuais_nivel_area(self, eixo_x, eixo_y) -> None:
        """
        Plota o gráfico de visualização residual da relação entre os dados e a reta ajustada.
        :param - eixo_x = variavel independente
               - eixo_y = variavel dependente
        :return - None
        """
        self.eixo_x = eixo_x
        self.eixo_y = eixo_y

        self.visualizador = ResidualsPlot(self.mmq_nivel_area)
        self.visualizador.fit(self.eixo_x, self.eixo_y)
        self.visualizador.poof()
