"""Itens (a) a (d) do Problema 1 - Análise de Custos de Serviços em Nuvem.

Verificação (b): Crystal. Previsão e economia (c) e (d): Eduardo.
"""

import numpy as np
import pandas as pd

from .linear_systems import eliminacao_gauss


def montar_sistema(df, servicos, coluna_total):
    """Monta A (quantidades consumidas) e b (total pago por mês)."""
    A = df[servicos].to_numpy(dtype=float)
    b = df[coluna_total].to_numpy(dtype=float)
    return A, b


def custos_unitarios(A, b, metodo=eliminacao_gauss):
    """(a) Custo unitário de cada serviço: resolve A·x = b."""
    return metodo(A, b)


def verificar_totais(A, x, b):
    """(b) Recalcula os totais mensais com os custos unitários e compara com os originais."""
    calculado = A @ x
    erro_abs = np.abs(calculado - b)
    return pd.DataFrame(
        {
            "mes": np.arange(1, len(b) + 1),
            "total_calculado": calculado,
            "total_original": b,
            "erro_absoluto": erro_abs,
            "erro_relativo": erro_abs / np.abs(b),
        }
    )


def custo_previsto(q_previsto, x):
    """(c) Custo total estimado do próximo mês."""
    return float(np.dot(q_previsto, x))


def melhor_reducao(q_previsto, x, servicos, reducao=0.20, meses=12):
    """(d) Reduz em `reducao` o uso de UM serviço; escolhe o de maior economia.

    Retorna dicionário com economias por serviço, serviço escolhido,
    economia mensal, novo custo total e economia acumulada em `meses` meses.
    """
    custos = np.asarray(q_previsto, dtype=float) * np.asarray(x, dtype=float)
    economias = reducao * custos
    i = int(np.argmax(economias))
    total = float(custos.sum())
    return {
        "economias": pd.Series(economias, index=servicos),
        "servico": servicos[i],
        "economia_mensal": float(economias[i]),
        "custo_atual": total,
        "novo_total": total - float(economias[i]),
        "economia_acumulada": float(economias[i]) * meses,
    }
