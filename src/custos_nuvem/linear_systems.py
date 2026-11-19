"""Métodos numéricos para sistemas lineares A·x = b (implementação própria).

Responsável: Gilberto.
Nenhuma função pronta de resolução de sistemas (ex.: numpy.linalg.solve) é usada.
"""

import numpy as np


def _validar(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).reshape(-1)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A deve ser uma matriz quadrada.")
    if A.shape[0] != b.shape[0]:
        raise ValueError("A e b devem ter o mesmo número de linhas.")
    return A, b


def substituicao_regressiva(U, y):
    """Resolve U·x = y, com U triangular superior."""
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]
    return x


def substituicao_progressiva(L, b):
    """Resolve L·y = b, com L triangular inferior."""
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]
    return y


def eliminacao_gauss(A, b, tol=1e-12):
    """Resolve A·x = b por eliminação de Gauss com pivoteamento parcial."""
    A, b = _validar(A, b)
    n = len(b)
    for k in range(n - 1):
        p = k + int(np.argmax(np.abs(A[k:, k])))
        if abs(A[p, k]) < tol:
            raise ValueError("Matriz singular ou quase singular.")
        if p != k:
            A[[k, p], :] = A[[p, k], :]
            b[[k, p]] = b[[p, k]]
        for i in range(k + 1, n):
            m = A[i, k] / A[k, k]
            A[i, k:] -= m * A[k, k:]
            b[i] -= m * b[k]
    if abs(A[n - 1, n - 1]) < tol:
        raise ValueError("Matriz singular ou quase singular.")
    return substituicao_regressiva(A, b)


def decomposicao_lu(A, tol=1e-12):
    """Decomposição LU com pivoteamento parcial: A[P] = L·U.

    Retorna (P, L, U), onde P é o vetor de permutação das linhas.
    """
    A = np.array(A, dtype=float)
    n = A.shape[0]
    P = np.arange(n)
    L = np.eye(n)
    U = A.copy()
    for k in range(n - 1):
        p = k + int(np.argmax(np.abs(U[k:, k])))
        if abs(U[p, k]) < tol:
            raise ValueError("Matriz singular ou quase singular.")
        if p != k:
            U[[k, p], :] = U[[p, k], :]
            P[[k, p]] = P[[p, k]]
            L[[k, p], :k] = L[[p, k], :k]
        for i in range(k + 1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]
    if abs(U[n - 1, n - 1]) < tol:
        raise ValueError("Matriz singular ou quase singular.")
    return P, L, U


def resolver_lu(A, b):
    """Resolve A·x = b usando a decomposição LU."""
    A, b = _validar(A, b)
    P, L, U = decomposicao_lu(A)
    y = substituicao_progressiva(L, b[P])
    return substituicao_regressiva(U, y)
