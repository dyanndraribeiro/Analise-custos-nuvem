"""Leitura dos arquivos CSV do problema (consumo_servicos.csv e previsao.csv)."""

import numpy as np
import pandas as pd


def carregar_csv(caminho, **kwargs):
    """Lê um CSV. Use kwargs se necessário (ex.: sep=";", decimal=",")."""
    return pd.read_csv(caminho, **kwargs)


def vetor_previsao(df, servicos):
    """Extrai o vetor de consumo previsto (1ª linha) na ordem de `servicos`."""
    return df[servicos].iloc[0].to_numpy(dtype=float)
