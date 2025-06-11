import numpy as np
import matplotlib.pyplot as plt

class Elipse:
    def __init__(self, rut: str):
        self.rut = rut
        self.digitos = self._extraer_digitos()
        self.verificador = int(rut[-1]) if rut[-1].isdigit() else 10  # 'K' se convierte en 10
        self.h, self.k = self.digitos[0], self.digitos[1]
        self._calcular_parametros()

    def _extraer_digitos(self):
        # Extrae dígitos numéricos del RUT
        numeros = ''.join(c for c in self.rut if c.isdigit())
        if len(numeros) < 8:
            raise ValueError("El RUT debe contener al menos 8 dígitos numéricos.")
        return list(map(int, numeros[:8]))

    def _calcular_parametros(self):
        d = self.digitos

        if self.verificador % 2 == 0:
            self.a = d[5] + d[6]
            self.b = d[7] + d[2]
            self.orientacio = 'Horizontal' if d[3] % 2 == 0 else 'Vertical'
        else:
            self.a = d[2] + d[3]
            self.b = d[4] + d[5]
            self.orientacio = 'Horizontal' if d[7] % 2 == 0 else 'Vertical'

        # Validación adicional: a y b no deben ser cero
        if self.a == 0 or self.b == 0:
            raise ValueError("Los parámetros 'a' y 'b' no pueden ser cero. Verifique el RUT ingresado.")

    def ecuacion_canonica(self):
        if self.orientacio == 'Horizontal':
            return f"((X - {self.h})² / {self.a**2}) + ((Y - {self.k})² / {self.b**2}) = 1"
        else:
            return f"((X - {self.h})² / {self.b**2}) + ((Y - {self.k})² / {self.a**2}) = 1"

    def ecuacion_general(self):
        if self.orientacio == 'Horizontal':
            A = self.b**2
            B = self.a**2
        else:
            A = self.a**2
            B = self.b**2

        D = -2 * A * self.h
        E = -2 * B * self.k
        F = A * self.h**2 + B * self.k**2 - (A * B)

        return f"{A}x² + {B}y² {D:+}x {E:+}y {F:+} = 0"

    def to_shapely(self):
        from shapely.geometry import Point
        from shapely.affinity import scale

        base = Point(self.h, self.k).buffer(1)
        return scale(base, self.a, self.b) if self.orientacio == 'Horizontal' else scale(base, self.b, self.a)


# Prueba de ejecución
if __name__ == "__main__":
    try:
        elipse1 = Elipse("12.345.678-9")
        print("Ecuación canónica:", elipse1.ecuacion_canonica())
        print("Ecuación general:", elipse1.ecuacion_general())
    except ValueError as e:
        print("Error:", e)
