import numpy as np

#Eliminação de Gauss

def _validar_sistema(A, b):
    """Garante que A seja quadrada e compatível com b."""
    M = np.array(A, dtype=float)
    v = np.array(b, dtype=float).reshape(-1)
    
    if M.ndim != 2 or M.shape[0] != M.shape[1]:
        raise ValueError("A matriz A precisa ser quadrada.")
    if M.shape[0] != v.shape[0]:
        raise ValueError("A e b devem ter a mesma quantidade de linhas.")
    
    return M, v

def substituicao_regressiva(U, y):
    """Resolve o sistema triangular superior (U * x = y) de baixo para cima."""
    n = len(y)
    x = np.zeros(n, dtype=float)
    
    for i in range(n-1, -1, -1):
        soma = 0.0
        for j in range(i+1, n):
            soma += U[i, j] * x[j]
        x[i] = (y[i] - soma) / U[i, i]
    
    return x


def eliminacao_gauss(A, b, tol=1e-12):
    M, v = _validar_sistema(A, b)
    n = len(v)
    
    for k in range(n - 1):
        #Pivoteamento parcial: 
        linha_pivo = k
        maior_valor = abs(M[k,k])
        
        for i in range(k + 1, n):
            if abs(M[i, k]) > maior_valor:
                maior_valor = abs(M[i, k])
                linha_pivo = i

        if maior_valor < tol:
            raise ValueError("Sistema singular ou quase singular.")
        if linha_pivo != k:
            M[[k, linha_pivo]] = M[[linha_pivo, k]]
            v[k], v[linha_pivo] = v[linha_pivo], v[k]
            
        for i in range(k + 1, n):
            multiplicador = M[i,k] / M[k,k]
            for j in range(k, n):
                M[i, j] -= multiplicador * M[k, j]
            v[i] -= multiplicador * v[k]
    
    if abs(M[n-1, n-1]) < tol:
        raise ValueError("Sistema singular ou quase singular.")
    
    return substituicao_regressiva(M, v)

# Fatoração LU: 

def substituicao_progressiva(L, b):
    """Resolve L * y = b de cima para baixo (L triangular inferior)."""
    n = len(b)
    y = np.zeros(n, dtype=float)

    for i in range(n):
        soma = 0.0
        for j in range(i):
            soma += L[i, j] * y[j]
        y[i] = (b[i] - soma) / L[i, i]

    return y


def decomposicao_lu(A, tol=1e-12):
    """Fatora A em P, L, U tais que A[P] = L * U."""
    M = np.array(A, dtype=float)
    if M.ndim != 2 or M.shape[0] != M.shape[1]:
        raise ValueError("A matriz A precisa ser quadrada.")

    n = M.shape[0]
    P = np.arange(n)
    L = np.eye(n, dtype=float)
    U = M.copy()

    for k in range(n - 1):
        linha_pivo = k
        maior_valor = abs(U[k, k])
        for i in range(k + 1, n):
            if abs(U[i, k]) > maior_valor:
                maior_valor = abs(U[i, k])
                linha_pivo = i

        if maior_valor < tol:
            raise ValueError("Sistema singular ou quase singular.")

        if linha_pivo != k:
            U[[k, linha_pivo], :] = U[[linha_pivo, k], :]
            P[k], P[linha_pivo] = P[linha_pivo], P[k]
            for j in range(k):
                L[k, j], L[linha_pivo, j] = L[linha_pivo, j], L[k, j]

        for i in range(k + 1, n):
            multiplicador = U[i, k] / U[k, k]
            L[i, k] = multiplicador
            for j in range(k, n):
                U[i, j] -= multiplicador * U[k, j]

    if abs(U[n - 1, n - 1]) < tol:
        raise ValueError("Sistema singular ou quase singular.")

    return P, L, U


def resolver_lu(A, b):
    """Resolve A * x = b usando a decomposição LU."""
    M, v = _validar_sistema(A, b)
    P, L, U = decomposicao_lu(M)
    y = substituicao_progressiva(L, v[P])
    return substituicao_regressiva(U, y)