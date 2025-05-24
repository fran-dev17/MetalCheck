import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import matplotlib.pyplot as plt

fecha = datetime.date.today()
nombre_archivo = f"reporte_agua_{fecha}.txt"

# Límites (OMS / EPA)
limites = {
    "Plomo (Pb)": 0.01,
    "Mercurio (Hg)": 0.001,
    "Cadmio (Cd)": 0.003,
    "Arsénico (As)": 0.01
}

# Análisis y clasificación
def analizar_calidad_agua(valores):
    indice = sum(valores[metal] / limites[metal] for metal in limites)
    clasificacion = (
        "Buena" if indice <= 1 else
        "Aceptable" if indice <= 3 else
        "Contaminada" if indice <= 5 else
        "Muy Contaminada"
    )
    return indice, clasificacion

# Guardar resultados en un archivo .txt
def guardar_en_txt(valores, indice, clasificacion):
    with open(nombre_archivo, "a+", encoding="utf-8") as f:
        f.write("Reporte de Calidad del Agua\n")
        f.write("-" * 30 + "\n")
        for metal, valor in valores.items():
            f.write(f"{metal}: {valor:.6f} mg/L\n")
        f.write(f"\nÍndice de Contaminación: {indice:.2f}\n")
        f.write(f"Clasificación: {clasificacion}\n")
        f.write(f"Fecha: {fecha}\n\n")

# Muestra el gráfico de comparación
def mostrar_grafica(valores):
    metales = list(valores.keys())
    concentraciones = list(valores.values())
    limites_referencia = [limites[metal] for metal in metales]

    x = range(len(metales))
    plt.figure(figsize=(8, 5))
    plt.bar(x, concentraciones, width=0.4, label='Ingresado', align='center', color='skyblue')
    plt.bar([i + 0.4 for i in x], limites_referencia, width=0.4, label='Límite', align='center', color='orange')

    plt.xticks([i + 0.2 for i in x], metales)
    plt.ylabel("Concentración (mg/L)")
    plt.title("Comparación de Metales Pesados con Límites")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Procesar análisis desde la GUI
def procesar_datos():
    try:
        valores = {metal: float(entradas[metal].get()) for metal in limites}
        for v in valores.values():
            if v < 0:
                raise ValueError("Valor negativo detectado.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos y no negativos.")
        return

    indice, clasificacion = analizar_calidad_agua(valores)
    resultado_var.set(f"Índice de Contaminación: {indice:.2f}\nClasificación: {clasificacion}\nFecha: {fecha}")
    ventana.valores_actuales = valores
    ventana.indice_actual = indice
    ventana.clasificacion_actual = clasificacion
    boton_guardar.config(state="normal")
    boton_grafica.config(state="normal")

def guardar_resultado():
    guardar_en_txt(ventana.valores_actuales, ventana.indice_actual, ventana.clasificacion_actual)
    messagebox.showinfo("Guardado", f"El reporte se ha guardado en '{nombre_archivo}'.")

def mostrar_grafica_interfaz():
    mostrar_grafica(ventana.valores_actuales)

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("MetalCheck - Calidad del Agua")
ventana.geometry("520x520")
ventana.configure(bg="#03003C")
ventana.resizable(False, False)

# Estilos
estilo = ttk.Style(ventana)
estilo.theme_use("clam")
estilo.configure("TLabel", font=("Segoe UI", 11, "bold"), foreground="white", background="#03003C")
estilo.configure("TEntry", font=("Segoe UI", 11), padding=5)
estilo.configure("TButton", font=("Segoe UI", 11, "bold"), padding=8, background="#03003C", foreground="white")
estilo.map("TButton", background=[("active", "green")])

# Componentes
ttk.Label(ventana, text="Ingrese las concentraciones (mg/L)", font=("Segoe UI", 12, "bold")).pack(pady=10)

entradas = {}
for metal in limites:
    frame = ttk.Frame(ventana)
    frame.pack(pady=5, fill="x", padx=20)
    ttk.Label(frame, text=metal, width=20).pack(side="left")
    entrada = ttk.Entry(frame, width=45)
    entrada.pack(side="left")
    entradas[metal] = entrada

ttk.Button(ventana, text="Analizar", command=procesar_datos).pack(pady=15)

resultado_var = tk.StringVar()
ttk.Label(ventana, textvariable=resultado_var, justify="center").pack(pady=10)

boton_guardar = ttk.Button(ventana, text="Guardar reporte", command=guardar_resultado, state="disabled")
boton_guardar.pack(pady=5)

boton_grafica = ttk.Button(ventana, text="Mostrar gráfica", command=mostrar_grafica_interfaz, state="disabled")
boton_grafica.pack(pady=5)

ventana.mainloop()