import numpy as np
from core.exceptions import ExecutionError, ValidationError


class LinearAlgebraExecutor:
    """
    Executors for matrix operations and linear system solvers.
    """

    def run(self, instance):
        mode = instance.calculation_mode

        dispatch = {
            # Matrix operations
            "determinant": lambda: self.determinant(instance),
            "inverse": lambda: self.inverse(instance),
            "norm": lambda: self.norm(instance),
            "condition_number": lambda: self.condition_number(instance),
            "transpose": lambda: self.transpose(instance),
            "rank": lambda: self.rank(instance),

            # System solvers
            "gauss": lambda: self.gauss(instance),
            "gauss_jordan": lambda: self.gauss_jordan(instance),
            "lu": lambda: self.lu(instance),
            "cholesky": lambda: self.cholesky(instance),
            "qr": lambda: self.qr(instance),
            "jacobi": lambda: self.jacobi(instance),
            "gauss_seidel": lambda: self.gauss_seidel(instance),
        }

        if mode not in dispatch:
            raise ValidationError(f"Executor not implemented for calculation_mode '{mode}'.")

        return dispatch[mode]()

    # ============================================================
    # MATRIX OPERATIONS
    # ============================================================

    def determinant(self, instance):
        return {"value": float(np.linalg.det(instance.A))}

    def inverse(self, instance):
        return {"value": np.linalg.inv(instance.A)}

    def norm(self, instance):
        return {"value": float(np.linalg.norm(instance.A))}

    def condition_number(self, instance):
        return {"value": float(np.linalg.cond(instance.A))}

    def transpose(self, instance):
        return {"value": instance.A.T}

    def rank(self, instance):
        return {"value": int(np.linalg.matrix_rank(instance.A))}

    # ============================================================
    # LINEAR SYSTEM SOLVERS
    # ============================================================

    def gauss(self, instance):
        A = instance.A.copy()
        b = instance.b.copy()
        n = len(b)

        for i in range(n):
            pivot_row = np.argmax(np.abs(A[i:, i])) + i
            if A[pivot_row, i] == 0:
                raise ExecutionError("Zero pivot encountered in Gauss elimination.")

            if pivot_row != i:
                A[[i, pivot_row]] = A[[pivot_row, i]]
                b[[i, pivot_row]] = b[[pivot_row, i]]

            for j in range(i + 1, n):
                factor = A[j, i] / A[i, i]
                A[j, i:] -= factor * A[i, i:]
                b[j] -= factor * b[i]

        x = np.zeros(n)
        for i in reversed(range(n)):
            x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

        return {"solution": x}

    def gauss_jordan(self, instance):
        A = instance.A.copy()
        b = instance.b.copy()
        n = len(b)

        M = np.hstack([A, b.reshape(-1, 1)])

        for i in range(n):
            pivot_row = np.argmax(np.abs(M[i:, i])) + i
            if M[pivot_row, i] == 0:
                raise ExecutionError("Zero pivot encountered in Gauss-Jordan.")

            if pivot_row != i:
                M[[i, pivot_row]] = M[[pivot_row, i]]

            M[i] = M[i] / M[i, i]

            for j in range(n):
                if j != i:
                    M[j] -= M[j, i] * M[i]

        return {"solution": M[:, -1]}

    def lu(self, instance):
        P, L, U = self._lu_decomposition(instance.A.copy())
        y = np.linalg.solve(L, instance.b)
        x = np.linalg.solve(U, y)
        return {"solution": x, "L": L, "U": U, "P": P}

    def _lu_decomposition(self, A):
        A = A.copy().astype(float)
        n = A.shape[0]

        P = np.eye(n)
        L = np.zeros((n, n))
        U = A.copy()

        for k in range(n):
            pivot_row = np.argmax(np.abs(U[k:, k])) + k
            if U[pivot_row, k] == 0:
                raise ExecutionError("Matrix is singular during LU decomposition.")

            if pivot_row != k:
                U[[k, pivot_row], :] = U[[pivot_row, k], :]
                P[[k, pivot_row], :] = P[[pivot_row, k], :]
                if k > 0:
                    L[[k, pivot_row], :k] = L[[pivot_row, k], :k]

            for i in range(k + 1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, :] -= L[i, k] * U[k, :]

        np.fill_diagonal(L, 1)
        return P, L, U

    def cholesky(self, instance):
        L = np.linalg.cholesky(instance.A)
        y = np.linalg.solve(L, instance.b)
        x = np.linalg.solve(L.T, y)
        return {"solution": x, "L": L}

    def qr(self, instance):
        Q, R = np.linalg.qr(instance.A)
        y = np.dot(Q.T, instance.b)
        x = np.linalg.solve(R, y)
        return {"solution": x, "Q": Q, "R": R}

    def jacobi(self, instance, tol=1e-10, max_iter=1000):
        A = instance.A
        b = instance.b
        n = len(b)
        x = np.zeros(n)

        for _ in range(max_iter):
            x_new = np.zeros(n)
            for i in range(n):
                s = np.dot(A[i, :], x) - A[i, i] * x[i]
                x_new[i] = (b[i] - s) / A[i, i]

            if np.linalg.norm(x_new - x) < tol:
                return {"solution": x_new}

            x = x_new

        raise ExecutionError("Jacobi did not converge.")

    def gauss_seidel(self, instance, tol=1e-10, max_iter=1000):
        A = instance.A
        b = instance.b
        n = len(b)
        x = np.zeros(n)

        for _ in range(max_iter):
            x_old = x.copy()
            for i in range(n):
                s1 = np.dot(A[i, :i], x[:i])
                s2 = np.dot(A[i, i + 1:], x_old[i + 1:])
                x[i] = (b[i] - s1 - s2) / A[i, i]

            if np.linalg.norm(x - x_old) < tol:
                return {"solution": x}

        raise ExecutionError("Gauss-Seidel did not converge.")
