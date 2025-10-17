import tkinter as tk
from tkinter import messagebox, Toplevel
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER
import os
import re
from xml.sax.saxutils import escape
import random

# 🔹 Registrar fuentes
def registrar_fuentes():
    fuentes_encontradas = {}
    posibles = [
        (r"C:\Windows\Fonts\comicbd.ttf", "ComicSansMS-Bold"),
        (r"C:\Windows\Fonts\comic.ttf", "ComicSansMS")
    ]
    for ruta, nombre in posibles:
        if os.path.exists(ruta):
            try:
                pdfmetrics.registerFont(TTFont(nombre, ruta))
                fuentes_encontradas[nombre] = nombre
            except Exception:
                pass

    font_bold = fuentes_encontradas.get("ComicSansMS-Bold", "Helvetica-Bold")
    font_reg = fuentes_encontradas.get("ComicSansMS", "Helvetica")
    return font_reg, font_bold

FUENTE_REG, FUENTE_BOLD = registrar_fuentes()

# 🔹 Carpeta donde guardar los PDFs
CARPETA_DESTINO = r"C:\Users\Pablo\Desktop\Programa genera cuadros en ingles"

# 🔹 Generar nombre automático del PDF
def generar_nombre_pdf(prefijo):
    base = os.path.join(CARPETA_DESTINO, f"{prefijo}")
    contador = 1
    while os.path.exists(f"{base}_{contador}.pdf"):
        contador += 1
    return f"{base}_{contador}.pdf"

# 🔹 Formato del texto (solo para inglés)
def aplicar_formato_pronunciacion_y_mayus(texto, font_size_base):
    if not texto:
        return ""
    quoted_size = max(8, int(font_size_base * 0.85))
    pattern = re.compile(r'("([^"]+)"|“([^”]+)”)')
    result_parts = []
    last_pos = 0
    for m in pattern.finditer(texto):
        start, end = m.span()
        outside = texto[last_pos:start]
        if outside:
            result_parts.append(escape(outside.upper()))
        content = m.group(2) if m.group(2) else m.group(3)
        content_escaped = escape(content)
        wrapped = f'<br/><font color="red" size="{quoted_size}"><b>{content_escaped}</b></font>'
        result_parts.append(wrapped)
        last_pos = end
    tail = texto[last_pos:]
    if tail:
        result_parts.append(escape(tail.upper()))
    return "".join(result_parts)

# 🔹 Frases IA base
FRASES_IA = [
    '¿Puedes ayudarme?',
    'Disculpe / Perdón',
    'No entiendo',
    '¡Eso es genial!',
    'Estoy aprendiendo inglés',
    '¿Qué estás haciendo?',
    'Por favor repite',
    'Buenos días',
    '¿De dónde eres?',
    'Por esta razón'
]

# 🔹 Ventana emergente con sugerencias IA
def mostrar_sugerencias_ia():
    sugerencias = random.sample(FRASES_IA, 10)

    ventana = Toplevel(root)
    ventana.title("🧠 Sugerencias IA")
    ventana.geometry("550x550")
    ventana.configure(bg="#2E0249")
    ventana.resizable(False, False)

    tk.Label(
        ventana,
        text="✨ Frases sugeridas por IA",
        font=("Comic Sans MS", 16, "bold"),
        fg="#F7C8E0",
        bg="#2E0249"
    ).pack(pady=15)

    texto_box = tk.Text(
        ventana,
        font=("Comic Sans MS", 12),
        wrap="word",
        height=15,
        width=55,
        bg="#F8E8EE",
        fg="#3C096C",
        insertbackground="#3C096C",
        relief="flat",
        padx=10,
        pady=10
    )
    texto_box.pack(padx=15, pady=5)
    texto_box.insert("1.0", "\n".join(sugerencias))

    def pegar_en_principal():
        contenido = texto_box.get("1.0", tk.END).strip()
        lineas = [line.strip() for line in contenido.split("\n") if line.strip()]
        for i in range(10):
            entradas_ingles[i].delete(0, tk.END)
            if i < len(lineas):
                entradas_ingles[i].insert(0, lineas[i])
        messagebox.showinfo("✅ Listo", "Las frases se pegaron en las casillas de inglés.")
        ventana.destroy()

    tk.Button(
        ventana,
        text="📋 Pegar sugerencias en inglés",
        font=("Comic Sans MS", 11, "bold"),
        bg="#90EE90",
        fg="#2E0249",
        activebackground="#B6E2A1",
        relief="flat",
        command=pegar_en_principal
    ).pack(pady=15)

# 🔹 Función genérica para crear un PDF (usada por inglés y español)
def crear_pdf(nombre_pdf, frases, aplicar_formato):
    os.makedirs(CARPETA_DESTINO, exist_ok=True)
    c = canvas.Canvas(nombre_pdf, pagesize=A4)
    ancho, alto = A4
    margen_x = 0.8 * cm
    margen_y = 1.0 * cm
    cuadro_ancho = (ancho - (2.2 * margen_x)) / 2
    cuadro_alto = (alto - (2.0 * margen_y)) / 5

    font_size = 22
    leading = int(font_size * 1.25)
    style = ParagraphStyle(
        name="CajaStyle",
        fontName=FUENTE_BOLD,
        fontSize=font_size,
        leading=leading,
        alignment=TA_CENTER
    )

    padding_x = 8
    padding_y = 8
    c.setLineWidth(2)

    index = 0
    for fila in range(5):
        for col in range(2):
            if index >= len(frases):
                break
            x = margen_x + col * (cuadro_ancho + margen_x / 2)
            y = alto - margen_y - (fila + 1) * cuadro_alto - fila * (margen_y / 5)
            c.rect(x, y, cuadro_ancho, cuadro_alto)
            texto = frases[index]
            if texto:
                texto_formateado = aplicar_formato(texto, font_size)
                max_w = cuadro_ancho - 2 * padding_x
                max_h = cuadro_alto - 2 * padding_y
                p = Paragraph(texto_formateado, style)
                w, h = p.wrap(max_w, max_h)
                if h > max_h:
                    fs = font_size
                    while h > max_h and fs >= 8:
                        fs -= 1
                        style.fontSize = fs
                        style.leading = int(fs * 1.25)
                        texto_formateado = aplicar_formato(texto, fs)
                        p = Paragraph(texto_formateado, style)
                        w, h = p.wrap(max_w, max_h)
                draw_x = x + padding_x
                draw_y = y + (cuadro_alto - h) / 2
                p.drawOn(c, draw_x, draw_y)
            index += 1
    c.save()

# 🔹 Exportar ambos PDFs (inglés + español)
def exportar_doble_pdf():
    frases_ing = [e.get().strip() for e in entradas_ingles]
    frases_esp = [e.get().strip() for e in entradas_espanol]

    nombre_ing = generar_nombre_pdf("cuadros_ingles")
    nombre_esp = generar_nombre_pdf("cuadros_espanol")

    crear_pdf(nombre_ing, frases_ing, aplicar_formato_pronunciacion_y_mayus)
    crear_pdf(nombre_esp, frases_esp, lambda t, s: escape(t))  # texto normal sin mayúsculas

    messagebox.showinfo("Éxito", f"PDFs generados:\n\n{nombre_ing}\n{nombre_esp}")

# 🔹 Interfaz principal
root = tk.Tk()
root.title("🌸 Creador de cuadros inglés/español 🌸")
root.configure(bg="#3C096C")

tk.Label(
    root,
    text="✏️ Escribí tus frases en inglés y su traducción en español:",
    font=("Comic Sans MS", 15, "bold"),
    fg="#F7C8E0",
    bg="#3C096C"
).pack(pady=15)

frame = tk.Frame(root, bg="#3C096C")
frame.pack()

entradas_ingles = []
entradas_espanol = []

for i in range(10):
    tk.Label(
        frame,
        text=f"Frase {i+1}:",
        font=("Comic Sans MS", 11, "bold"),
        fg="#E0AAFF",
        bg="#3C096C"
    ).grid(row=i, column=0, sticky="e", padx=5, pady=3)

    e_ing = tk.Entry(frame, width=35, font=("Comic Sans MS", 11), bg="#F8E8EE", fg="#3C096C", relief="flat")
    e_ing.grid(row=i, column=1, padx=5, pady=3)
    entradas_ingles.append(e_ing)

    e_esp = tk.Entry(frame, width=35, font=("Comic Sans MS", 11), bg="#F8E8EE", fg="#3C096C", relief="flat")
    e_esp.grid(row=i, column=2, padx=5, pady=3)
    entradas_espanol.append(e_esp)

# 🔹 Botones
botones_frame = tk.Frame(root, bg="#3C096C")
botones_frame.pack(pady=20)

tk.Button(
    botones_frame,
    text="🧠 Obtener sugerencias IA",
    font=("Comic Sans MS", 12, "bold"),
    bg="#0AB5E9",
    fg="white",
    activebackground="#E0AAFF",
    relief="flat",
    command=mostrar_sugerencias_ia
).grid(row=0, column=0, padx=10)

tk.Button(
    botones_frame,
    text="📄 Exportar ambos PDF",
    font=("Comic Sans MS", 12, "bold"),
    bg="#90EE90",
    fg="#3C096C",
    activebackground="#B6E2A1",
    relief="flat",
    command=exportar_doble_pdf
).grid(row=0, column=1, padx=10)

root.mainloop()

