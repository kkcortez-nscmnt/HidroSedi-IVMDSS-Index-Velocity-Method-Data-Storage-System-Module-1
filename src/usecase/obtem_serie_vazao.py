import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from src.infra.repositories import MatEntityRepository


class ObtemSerieVazao(LinearRegression):
    """
    Método de obtenção de vazão Velocidade - Área
    """

    def __init__(self) -> None:

        self.mat_repository = MatEntityRepository()
        self.vmed_estimada = None
        self.area_estimada = None
        self.vazao_estimada = None
        self.vazao_observada = None
        self.cns = None

    def configura_var_vazao_observada(self) -> np.ndarray:
        """
        Retorna matriz da variavel vazões observadas.
        :return - matriz numpy
        """
        self.vazao_obs = self.mat_repository.select_flow_rate_from_mat_table()
        self.vazao_obs = np.array(self.vazao_obs)
        self.mtx_vazao_obs = self.vazao_obs.reshape(-1, 1)

        return self.mtx_vazao_obs

    def obter_serie_estimadas_de_vazao(
        self, vmed_estimada, area_estimada
    ) -> np.ndarray:
        """
        Aplica o método Velocidade - Área.
        :param - vel_estimada = serie estimada de velocidade media (m/s)
               - area_estimada = serie estimada de area (m²)
        """
        self.vmed_estimada = vmed_estimada
        self.area_estimada = area_estimada
        self.vazao_estimada = vmed_estimada * area_estimada
        return self.vazao_estimada

    def obter_coeficiente_de_nash_sutcliffe(self, vazao_obs, vazao_est) -> float:
        """
        Calcula o coeficiente de Nash Sutcliffe
        :params - vazao_obs = série de vazão observada..
                - vazao_est = sére de vazão estimada.
        :return - float
        """
        self.cns = 1 - (
            np.sum((vazao_obs - vazao_est) ** 2)
            / np.sum((vazao_obs - np.mean(vazao_obs)) ** 2)
        )
        return self.cns

    def plotar_grafico_vazao_observada_vazao_estimada(
        self, vazao_observada, vazao_estimada
    ) -> None:

        self.vazao_estimada = np.array(vazao_estimada)
        self.vazao_observada = np.array(vazao_observada)

        self.mmq_vazao_obs_vazao_est = LinearRegression()
        self.mmq_vazao_obs_vazao_est.fit(
            self.vazao_estimada.reshape(-1, 1), self.vazao_observada.reshape(-1, 1)
        )

        self.var_estimada = self.mmq_vazao_obs_vazao_est.predict(self.vazao_observada)
        self.eixo_x = self.vazao_observada.ravel()
        self.eixo_y = self.vazao_estimada.ravel()
        self.var_estimada = self.var_estimada.ravel()

        self.grafico = px.scatter(
            x=self.eixo_x,
            y=self.eixo_y,
            title=f" Relação Vazão observada (m³/s) - Vazão estimada (m³/s) CNS = {round(self.cns, 3)}",
        )

        self.grafico.add_scatter(x=self.eixo_x, y=self.var_estimada)

        self.grafico.update_layout(
            xaxis_title="Vazão Observada (m³/s)", yaxis_title="Vazão Estimada(m³/s)"
        )
        self.grafico.show()
