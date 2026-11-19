import numpy as np

from custos_nuvem import (
    custos_unitarios,
    verificar_totais,
    custo_previsto,
    melhor_reducao,
)

SERVICOS = ["cpu", "armazenamento", "banco", "transferencia", "funcoes"]


def _dados():
    rng = np.random.default_rng(1)
    A = rng.uniform(10, 100, size=(5, 5))
    x_real = np.array([0.05, 0.02, 0.10, 0.08, 0.01])
    return A, x_real, A @ x_real


def test_custos_unitarios_e_verificacao():
    A, x_real, b = _dados()
    x = custos_unitarios(A, b)
    assert np.allclose(x, x_real)
    tabela = verificar_totais(A, x, b)
    assert (tabela["erro_relativo"] < 1e-9).all()


def test_custo_previsto():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    q = np.array([10.0, 10.0, 10.0, 10.0, 10.0])
    assert custo_previsto(q, x) == 150.0


def test_melhor_reducao():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    q = np.array([10.0, 10.0, 10.0, 10.0, 10.0])
    r = melhor_reducao(q, x, SERVICOS)
    assert r["servico"] == "funcoes"
    assert np.isclose(r["economia_mensal"], 10.0)
    assert np.isclose(r["novo_total"], 140.0)
    assert np.isclose(r["economia_acumulada"], 120.0)
