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
        A = self.b**2 if self.orientacio == 'Horizontal' else self.a**2
        B = self.a**2 if self.orientacio == 'Horizontal' else self.b**2

        expr = (
            f"{A}(x - {self.h})² + {B}(Y - {self.k})² = {A * B}"
        )
        return expr
if __name__ == "__main__":
    # Ejemplo de uso
    elipse1 = Elipse("12.345.678-9")
    elipse2 = Elipse("11.223.344-5")

    print("Ecuación canónica:", elipse1.ecuacion_canonica())
    print("Ecuación general:", elipse1.ecuacion_general())
    
        # Función añadida para detección de colisiones (Fase 3)
    def to_shapely(self):
        from shapely.geometry import Point
        from shapely.affinity import scale

        base = Point(self.h, self.k).buffer(1)
        if self.orientacio == 'Horizontal':
            return scale(base, self.a, self.b)
        else:
            return scale(base, self.b, self.a)
