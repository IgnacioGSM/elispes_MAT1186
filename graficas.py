from elipse import Elipse
import matplotlib.pyplot as plt
import numpy as np

def graficar_elipse(elipse: Elipse):
    # Crea un circulo de puntos para graficar la elipse
    theta = np.linspace(0, 2 * np.pi, 100)
    # Calcula los puntos de la elipse en función de su orientación
    if elipse.orientacio == 'Horizontal':
        x = elipse.h + elipse.a * np.cos(theta)
        y = elipse.k + elipse.b * np.sin(theta)
    else:
        x = elipse.h + elipse.b * np.cos(theta)
        y = elipse.k + elipse.a * np.sin(theta)

    plt.plot(x, y)
    plt.scatter([elipse.h], [elipse.k], color='red')  # Centro de la elipse
    plt.xlim(elipse.h - elipse.a - 1, elipse.h + elipse.a + 1)
    plt.ylim(elipse.k - elipse.b - 1, elipse.k + elipse.b + 1)
    plt.axhline(0, color='black',linewidth=0.5, ls='--')
    plt.axvline(0, color='black',linewidth=0.5, ls='--')
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.title("Gráfica de la Elipse, RUT: " + elipse.rut)
    plt.xlabel("Eje X")
    plt.ylabel("Eje Y")
    plt.show()

if __name__ == "__main__":
    # Ejemplo de uso
    elipse1 = Elipse("12.345.678-9")
    elipse2 = Elipse("11.223.344-5")

    print("Ecuación canónica:", elipse1.ecuacion_canonica())
    print("Ecuación general:", elipse1.ecuacion_general())
    
    graficar_elipse(elipse1)