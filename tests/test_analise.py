import numpy as np
import pytest

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


# ---- Itens (c) e (d) com os dados reais do Problema 1 ----------------------

SERVICOS_REAIS = ["cpu", "armazenamento", "banco", "transferencia", "funcoes"]
Q_REAL = np.array([200.0, 45.0, 130.0, 320.0, 280.0])   # previsao.csv (mes 6)
X_REAL = np.array([2.5, 15.0, 4.0, 0.8, 1.5])           # custos unitarios do item (a)


def test_custo_previsto_problema1():
    assert np.isclose(custo_previsto(Q_REAL, X_REAL), 2371.0)


def test_melhor_reducao_problema1():
    r = melhor_reducao(Q_REAL, X_REAL, SERVICOS_REAIS)
    assert r["servico"] == "armazenamento"
    assert np.isclose(r["economia_mensal"], 135.0)
    assert np.isclose(r["novo_total"], 2236.0)
    assert np.isclose(r["economia_acumulada"], 1620.0)


def test_novo_total_confere_recalculando():
    """Verificação independente: reduz 20% da quantidade e recalcula o custo."""
    r = melhor_reducao(Q_REAL, X_REAL, SERVICOS_REAIS)
    q = Q_REAL.copy()
    q[SERVICOS_REAIS.index(r["servico"])] *= 0.8
    assert np.isclose(custo_previsto(q, X_REAL), r["novo_total"])


def test_cenarios_cobrem_todos_os_servicos():
    r = melhor_reducao(Q_REAL, X_REAL, SERVICOS_REAIS)
    c = r["cenarios"]
    assert set(c.index) == set(SERVICOS_REAIS)
    assert c.index[0] == "armazenamento"          # ordenado do maior para o menor
    assert np.isclose(c.loc["transferencia", "economia_mensal"], 51.2)
    assert np.isclose(c.loc["cpu", "novo_total"], 2271.0)


def test_economia_acumulada_respeita_numero_de_meses():
    r = melhor_reducao(Q_REAL, X_REAL, SERVICOS_REAIS, meses=6)
    assert np.isclose(r["economia_acumulada"], 6 * 135.0)


def test_reducao_invalida():
    with pytest.raises(ValueError):
        melhor_reducao(Q_REAL, X_REAL, SERVICOS_REAIS, reducao=1.5)
    with pytest.raises(ValueError):
        melhor_reducao(Q_REAL, X_REAL, SERVICOS_REAIS, reducao=-0.1)


def test_tamanhos_incompativeis():
    with pytest.raises(ValueError):
        melhor_reducao(Q_REAL, X_REAL, SERVICOS_REAIS[:3])
    with pytest.raises(ValueError):
        custo_previsto(Q_REAL, X_REAL[:3])
