import numpy as np
import matplotlib.pyplot as plt

class Elipse:
    def __init__(self, rut:str):
        self.rut = rut
        self.digitos = self._extraer_digitos()
        self.verificador = int(rut[-1]) if rut[-1].isdigit() else 10    # Guarda como entero el ultimo caracter, si es K lo guarda como 10
        self.h, self.k = self.digitos[0], self.digitos[1]
        self._calcular_parametros()

    def _extraer_digitos(self):
        # Extrae todos los digitos del RUT y los convierte en una lista de enteros
        numeros = ''.join(c for c in self.rut if c.isdigit())
        if len(numeros) < 8:
            raise ValueError("El rut debe tener 8 digitos")
        return list(map(int, numeros[:8]))
    
    def _calcular_parametros(self):     # Calcula los parametros a, b y orientacion de la elipse de acuerdo al RUT
        d = self.digitos
        if self.verificador % 2 == 0:
            self.a = d[5] + d[6]
            self.b = d[7] + d[2]
            self.orientacio = 'Horizontal' if d[3] % 2 == 0 else 'Vertical'
        else:
            self.a = d[2] + d[3]
            self.b = d[4] + d[5]
            self.orientacio = 'Horizontal' if d[7] % 2 == 0 else 'Vertical'

    def ecuacion_canonica(self):
        return f"((X - {self.h})² / {self.a**2}) + ((Y - {self.k})² / {self.b**2}) = 1" \
        if self.orientacio == 'Horizontal' else \
            f"((X - {self.h})² / {self.b**2}) + ((Y - {self.k})² / {self.a**2}) = 1"
        
    def ecuacion_general(self):
        # Ecuación general: A(x-h)^2 + B(y-k)^2 = A*B
        if self.orientacio == 'Horizontal':
            A = self.b**2
            B = self.a**2
        else:
            A = self.a**2
            B = self.b**2

        # Expande la ecuación: Ax^2 + By^2 + Dx + Ey + F = 0
        # (x-h)^2 = x^2 - 2hx + h^2
        # (y-k)^2 = y^2 - 2ky + k^2
        D = -2 * A * self.h
        E = -2 * B * self.k
        F = A * self.h**2 + B * self.k**2 - (A * B)

        expr = f"{A}x² + {B}y² {D:+}x {E:+}y {F:+} = 0"
        return expr
if __name__ == "__main__":
    # Ejemplo de uso
    elipse1 = Elipse("12.345.678-9")
    elipse2 = Elipse("11.223.344-5")