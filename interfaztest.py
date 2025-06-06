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
    ax.legend()
    ax.grid(True)

    if canvas_widget:
        canvas_widget.get_tk_widget().destroy()

    canvas_widget = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(expand=True, fill="both")

# Lógica de comparación y detección de colisiones
def comparar():
    global plot_type
    rut1 = entry_rut1.get()
    rut2 = entry_rut2.get()
    text_resultado.delete("0.0", "end")
    try:
        e1 = Elipse(rut1)
        e2 = Elipse(rut2)
        actualizar_grafico(e1, e2)

        colision = e1.to_shapely().intersects(e2.to_shapely())

        resultado = (
            f"[RUT 1: {rut1}]\n{e1.ecuacion_canonica()}\n{e1.ecuacion_general()}\n\n"
            f"[RUT 2: {rut2}]\n{e2.ecuacion_canonica()}\n{e2.ecuacion_general()}\n\n"
        )
        resultado += "⚠️ Intersección detectada." if colision else "✅ Trayectorias seguras: sin intersección."
        text_resultado.insert("0.0", resultado)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Cambia entre 2D y 3D
def cambiar_vista():
    global plot_type
    plot_type = "3D" if plot_type == "2D" else "2D"
    comparar()

# Botones
btn_comparar = ctk.CTkButton(frame, text="Comparar Trayectorias", command=comparar)
btn_comparar.pack(pady=10)

btn_cambiar = ctk.CTkButton(frame, text="Cambiar Vista 2D / 3D", command=cambiar_vista)
btn_cambiar.pack(pady=5)

# Ejecutar interfaz
app.mainloop()
