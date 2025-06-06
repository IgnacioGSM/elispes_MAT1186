import customtkinter as ctk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from elipse import Elipse  

# Configuración de estilo
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Ventana principal
app = ctk.CTk()
app.geometry("1000x700")
app.title("Simulador de Trayectorias de Drones")

# Secciones de la ventana
frame = ctk.CTkFrame(app)
frame.pack(side="left", fill="y", padx=10, pady=10)

canvas_frame = ctk.CTkFrame(app)
canvas_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

# Widgets de entrada y texto
label_title = ctk.CTkLabel(frame, text="Simulador de Drones", font=ctk.CTkFont(size=20, weight="bold"))
label_title.pack(pady=10)

entry_rut1 = ctk.CTkEntry(frame, placeholder_text="RUT 1 (ej: 12.345.678-9)", width=250)
entry_rut1.pack(pady=5)

entry_rut2 = ctk.CTkEntry(frame, placeholder_text="RUT 2 (ej: 20.123.456-7)", width=250)
entry_rut2.pack(pady=5)

text_resultado = ctk.CTkTextbox(frame, height=200, width=250)
text_resultado.pack(pady=10)

# Área de gráficos
fig = plt.Figure(figsize=(6, 5), dpi=100)
plot_type = "2D"
canvas_widget = None

# Función para graficar las elipses
def actualizar_grafico(e1, e2):
    global canvas_widget
    fig.clf()
    ax = fig.add_subplot(111, projection='3d' if plot_type == "3D" else None)

    # Graficar elipses
    for e, color in zip([e1, e2], ['blue', 'orange']):
        theta = np.linspace(0, 2 * np.pi, 400)
        if e.orientacio == 'Horizontal':
            x = e.h + e.a * np.cos(theta)
            y = e.k + e.b * np.sin(theta)
        else:
            x = e.h + e.b * np.cos(theta)
            y = e.k + e.a * np.sin(theta)
        z = np.zeros_like(x)
        if plot_type == "2D":
            ax.plot(x, y, color=color, label=f"RUT {e.rut}")
            ax.scatter(e.h, e.k, color=color)
        else:
            ax.plot(x, y, z, color=color, label=f"RUT {e.rut}")
            ax.scatter(e.h, e.k, 0, color=color)
            ax.set_zlabel("Z")

    ax.set_title(f"Vista {plot_type}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Calcular límites para mantener la misma escala
    xs, ys = [], []
    for e in [e1, e2]:
        if e.orientacio == 'Horizontal':
            xs.extend([e.h - e.a, e.h + e.a])
            ys.extend([e.k - e.b, e.k + e.b])
        else:
            xs.extend([e.h - e.b, e.h + e.b])
            ys.extend([e.k - e.a, e.k + e.a])
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    # Añadir margen
    dx = (max_x - min_x) * 0.1
    dy = (max_y - min_y) * 0.1
    min_x -= dx
    max_x += dx
    min_y -= dy
    max_y += dy

    # Mantener la misma escala en ambos ejes
    max_range = max(max_x - min_x, max_y - min_y)
    mid_x = (max_x + min_x) / 2
    mid_y = (max_y + min_y) / 2
    lim_x0 = np.floor(mid_x - max_range / 2)
    lim_x1 = np.ceil(mid_x + max_range / 2)
    lim_y0 = np.floor(mid_y - max_range / 2)
    lim_y1 = np.ceil(mid_y + max_range / 2)
    ax.set_xlim(lim_x0, lim_x1)
    ax.set_ylim(lim_y0, lim_y1)
    if plot_type == "3D":
        ax.set_zlim(-max_range / 2, max_range / 2)
    else:
        # Ejes avanzan de 1 en 1 y cuadriculado
        ax.set_xticks(np.arange(lim_x0, lim_x1 + 1, 1))
        ax.set_yticks(np.arange(lim_y0, lim_y1 + 1, 1))
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

    ax.legend()

    if canvas_widget:
        canvas_widget.get_tk_widget().destroy()

    canvas_widget = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(expand=True, fill="both")

# Lógica de comparación y detección de colisiones
def punto_en_elipse(x, y, elipse: Elipse):
    # Verifica si un punto (x, y) está dentro o fuera de la elipse
    # Entrega el valor de la ecuación de la elipse con el punto (x, y), si es menor a 1 está dentro, si es igual a 1 está en la frontera, y si es mayor a 1 está fuera.
    if elipse.orientacio == 'Horizontal':
        return ((x - elipse.h) ** 2) / (elipse.a ** 2) + ((y - elipse.k) ** 2) / (elipse.b ** 2)
    else:
        return ((x - elipse.h) ** 2) / (elipse.b ** 2) + ((y - elipse.k) ** 2) / (elipse.a ** 2)

def detectar_colision(e1: Elipse, e2: Elipse):
    # Detecta si dos elipses colisionan.
    # Primero se obtiene un gran rango de puntos en la elipse 1
    theta = np.linspace(0, 2 * np.pi, 360)
    if e1.orientacio == 'Horizontal':
        x1 = e1.h + e1.a * np.cos(theta)
        y1 = e1.k + e1.b * np.sin(theta)
    else:
        x1 = e1.h + e1.b * np.cos(theta)
        y1 = e1.k + e1.a * np.sin(theta)
    # Luego se verifica si hay puntos dentro y fuera de la elipse 2
    dentro = False
    fuera = False
    for x, y in zip(x1, y1):    # Recorre los puntos de la elipse 1
        valor = punto_en_elipse(x, y, e2)
        print(f"Valor de la elipse 2 en ({x}, {y}): {valor}")
        if valor < 1:  # Dentro de la elipse (incluyendo frontera)
            dentro = True
        elif valor > 1:  # Fuera de la elipse
            fuera = True

        elif valor == 1:  # En la frontera de la elipse
            # Colision si o si
            dentro = True
            fuera = True
        if dentro and fuera:
            return True  # Hay intersección

    return False    # No hay intersección

def comparar():
    global plot_type
    rut1 = entry_rut1.get()
    rut2 = entry_rut2.get()
    text_resultado.delete("0.0", "end")
    try:
        e1 = Elipse(rut1)
        e2 = Elipse(rut2)

        colision = detectar_colision(e1, e2)

        resultado = (
            f"[RUT 1: {rut1}]\n{e1.ecuacion_canonica()}\n{e1.ecuacion_general()}\n\n"
            f"[RUT 2: {rut2}]\n{e2.ecuacion_canonica()}\n{e2.ecuacion_general()}\n\n"
        )
        resultado += "⚠️ Intersección detectada!!" if colision else "✅ Trayectorias seguras: sin intersección."
        text_resultado.insert("0.0", resultado)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Cambia entre 2D y 3D
def cambiar_vista():
    global plot_type
    plot_type = "3D" if plot_type == "2D" else "2D"
    cargar_grafico()

def cargar_grafico():
    # Carga el gráfico inicial con los RUTs ingresados
    rut1 = entry_rut1.get()
    rut2 = entry_rut2.get()
    if rut1 and rut2:
        try:
            e1 = Elipse(rut1)
            e2 = Elipse(rut2)
            actualizar_grafico(e1, e2)

            # Texto de resultado
            text_resultado.delete("0.0", "end")

            resultado = (
                f"[RUT 1: {rut1}]\n{e1.ecuacion_canonica()}\n{e1.ecuacion_general()}\n\n"
                f"[RUT 2: {rut2}]\n{e2.ecuacion_canonica()}\n{e2.ecuacion_general()}\n\n"
                "✅ Trayectorias cargadas correctamente."
            )

            text_resultado.insert("0.0", resultado)
        except Exception as e:
            messagebox.showerror("Error", str(e))

# En caso de detectar colision
def alejar_centros(e1: Elipse, e2: Elipse, paso=0.5):   # Mientras menor el paso, más lento se alejan los centros, como son drones conviene que queden lejitos
    # Aleja los centros de las elipses para evitar colisiones
    dist_x = e2.h - e1.h
    dist_y = e2.k - e1.k
    distancia = np.sqrt(dist_x**2 + dist_y**2)  # Distancia entre los centros con el teorema de Pitágoras 

    if distancia == 0:
        # Están en el mismo punto, se aleja uno de los centros
        e2.h += paso
        e2.k += paso
    else:
        # Normaliza la distancia y aleja los centros
        # norm_x y norm_y forman un vector unitario
        norm_x = dist_x / distancia
        norm_y = dist_y / distancia
        e2.h += norm_x * paso
        e2.k += norm_y * paso

def corregir_colisiones():
    rut1 = entry_rut1.get()
    rut2 = entry_rut2.get()
    try:
        e1 = Elipse(rut1)
        e2 = Elipse(rut2)

        while detectar_colision(e1, e2):
            alejar_centros(e1, e2)
        
        # Una vez corregidas las trayectorias, se actualiza el gráfico y el texto de resultado
        actualizar_grafico(e1, e2)
        
        text_resultado.delete("0.0", "end")
        resultado = (
            f"[RUT 1: {rut1}]\n{e1.ecuacion_canonica()}\n{e1.ecuacion_general()}\n\n"
            f"[RUT 2: {rut2}]\n{e2.ecuacion_canonica()}\n{e2.ecuacion_general()}\n\n"
            "✅ Trayectorias corregidas: sin intersección."
        )
        text_resultado.insert("0.0", resultado)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Botones
btn_corregir = ctk.CTkButton(frame, text="Corregir Colisiones", command=corregir_colisiones)
btn_corregir.pack(pady=10)

btn_mostrar = ctk.CTkButton(frame, text="Mostrar Trayectorias", command=cargar_grafico)
btn_mostrar.pack(pady=5)

btn_colision = ctk.CTkButton(frame, text="Comparar Trayectorias", command=comparar)
btn_colision.pack(pady=5)

btn_cambiar = ctk.CTkButton(frame, text="Cambiar Vista 2D / 3D", command=cambiar_vista)
btn_cambiar.pack(pady=5)

# Ejecutar interfaz
app.mainloop()
