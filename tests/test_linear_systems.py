import numpy as np
import pytest

from custos_nuvem import eliminacao_gauss, resolver_lu, decomposicao_lu


def _sistema():
    rng = np.random.default_rng(0)
    A = rng.uniform(1, 10, size=(5, 5))
    x_real = np.array([0.5, 2.0, 1.25, 0.1, 3.0])
    return A, x_real, A @ x_real


def test_gauss_recupera_solucao():
    A, x_real, b = _sistema()
    assert np.allclose(eliminacao_gauss(A, b), x_real)


def test_lu_recupera_solucao():
    A, x_real, b = _sistema()
    assert np.allclose(resolver_lu(A, b), x_real)


def test_lu_reconstroi_matriz():
    A, _, _ = _sistema()
    P, L, U = decomposicao_lu(A)
    assert np.allclose(L @ U, A[P])


def test_pivoteamento_necessario():
    A = np.array([[0.0, 2.0], [1.0, 1.0]])
    b = np.array([4.0, 3.0])
    assert np.allclose(eliminacao_gauss(A, b), [1.0, 2.0])


def test_matriz_singular():
    A = np.array([[1.0, 2.0], [2.0, 4.0]])
    with pytest.raises(ValueError):
        eliminacao_gauss(A, [1.0, 2.0])
