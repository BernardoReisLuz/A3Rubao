
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# --------------------------------------------------
# CONFIGURACAO
# --------------------------------------------------

ARQUIVO_IMAGEM = "passaro.jpg"

A_R = 1.0
A_G = 0.5
A_B = 1.5

LARGURA_TILE = 115
ALTURA_TILE = 90

FUNDO = "#f3f5f7"
AZUL = "#2878c8"
TEXTO = "#183153"

# --------------------------------------------------
# CARREGAR IMAGEM
# --------------------------------------------------

if not os.path.exists(ARQUIVO_IMAGEM):
    raise FileNotFoundError(
        f"Imagem nao encontrada: {ARQUIVO_IMAGEM}"
    )

imagem_original = Image.open(
    ARQUIVO_IMAGEM
).convert("RGB")

# Imagem colorida de referencia
imagem_referencia = imagem_original.copy()
imagem_referencia.thumbnail((230, 150))

# --------------------------------------------------
# DIVIDIR IMAGEM EM 9 PARTES
# --------------------------------------------------

def dividir_imagem(imagem):
    largura, altura = imagem.size
    partes = []

    for linha in range(3):
        for coluna in range(3):
            x1 = coluna * largura // 3
            y1 = linha * altura // 3
            x2 = (coluna + 1) * largura // 3
            y2 = (linha + 1) * altura // 3

            parte = imagem.crop((x1, y1, x2, y2))

            parte = parte.resize(
                (LARGURA_TILE, ALTURA_TILE),
                Image.Resampling.LANCZOS
            )

            partes.append(parte)

    return partes


partes = dividir_imagem(imagem_original)

# --------------------------------------------------
# CALCULAR RGB MEDIO
# --------------------------------------------------

def media_rgb(imagem):
    imagem_pequena = imagem.resize(
        (1, 1),
        Image.Resampling.BOX
    )
    return imagem_pequena.getpixel((0, 0))


def criar_desafio():
    posicao = random.randint(0, 8)

    r, g, b = media_rgb(partes[posicao])

    # Intensidade de cinza
    y = round(
        0.299 * r +
        0.587 * g +
        0.114 * b
    )

    # Respostas corretas
    b_r = r - A_R * y
    b_g = g - A_G * y
    b_b = b - A_B * y

    return posicao, y, (r, g, b), (b_r, b_g, b_b)


posicao_x, Y, cor_original, respostas = criar_desafio()

# --------------------------------------------------
# JANELA
# --------------------------------------------------

janela = tk.Tk()
janela.title("Desafio da Cor - Passaro")
janela.geometry("700x1000")
janela.minsize(620, 800)
janela.configure(bg=FUNDO)

tk.Label(
    janela,
    text="DESAFIO: RECUPERE A COR",
    font=("Arial", 20, "bold"),
    bg=FUNDO,
    fg=TEXTO
).pack(pady=(12, 5))

tk.Label(
    janela,
    text=(
        "Observe a imagem colorida e recupere os termos b.\n"
        "A regiao marcada com X foi convertida para cinza."
    ),
    font=("Arial", 11),
    bg=FUNDO,
    fg=TEXTO,
    justify="center"
).pack(pady=5)

# --------------------------------------------------
# IMAGEM COLORIDA DE REFERENCIA
# --------------------------------------------------

tk.Label(
    janela,
    text="VALORES RGB ORIGINAIS",
    font=("Arial", 13, "bold"),
    bg=FUNDO,
    fg=TEXTO
).pack(pady=(10, 3))

label_rgb = tk.Label(
    janela,
    text="",
    font=("Consolas", 14, "bold"),
    bg="#e8eef6",
    fg=TEXTO,
    padx=20,
    pady=10,
    relief="solid",
    bd=1
)
label_rgb.pack(pady=5)

# --------------------------------------------------
# MATRIZ 3x3
# --------------------------------------------------

quadro = tk.Frame(janela, bg=FUNDO)
quadro.pack(pady=8)

tiles = []
imagens_tk = []


def atualizar_matriz():
    imagens_tk.clear()

    for i, parte in enumerate(partes):
        if i == posicao_x:
            exibicao = parte.convert("L").convert("RGB")
            texto = "X"
        else:
            exibicao = parte.copy()
            texto = str(i + 1)

        foto = ImageTk.PhotoImage(exibicao)
        imagens_tk.append(foto)

        tiles[i].config(
            image=foto,
            text=texto,
            compound="center",
            fg="white",
            font=("Arial", 20, "bold"),
            bd=2,
            relief="solid"
        )


for i in range(9):
    tile = tk.Label(quadro, bd=2, relief="solid")

    tile.grid(
        row=i // 3,
        column=i % 3,
        padx=2,
        pady=2
    )

    tiles.append(tile)

atualizar_matriz()

# --------------------------------------------------
# EQUACOES
# --------------------------------------------------

label_y = tk.Label(
    janela,
    text="",
    font=("Arial", 12, "bold"),
    bg=FUNDO,
    fg=TEXTO
)
label_y.pack(pady=5)

tk.Label(
    janela,
    text=(
        "R = 1.0 x Y + bR\n"
        "G = 0.5 x Y + bG\n"
        "B = 1.5 x Y + bB"
    ),
    font=("Consolas", 12),
    bg="#e8eef6",
    fg=TEXTO,
    padx=18,
    pady=8,
    relief="solid",
    bd=1
).pack(pady=5)

tk.Label(
    janela,
    text="Digite os valores encontrados: ( use . para decimal )",
    font=("Arial", 11),
    bg=FUNDO,
    fg=TEXTO
).pack(pady=5)

# --------------------------------------------------
# ENTRADAS
# --------------------------------------------------

formulario = tk.Frame(janela, bg=FUNDO)
formulario.pack()

entradas = {}

for linha, canal in enumerate(["R", "G", "B"]):
    tk.Label(
        formulario,
        text=f"b{canal}:",
        font=("Arial", 11),
        bg=FUNDO,
        fg=TEXTO
    ).grid(row=linha, column=0, padx=8, pady=3)

    entrada = tk.Entry(
        formulario,
        width=14,
        justify="center",
        font=("Arial", 11)
    )
    entrada.grid(row=linha, column=1, padx=8, pady=3)

    entradas[canal] = entrada

# --------------------------------------------------
# AREA DE RESULTADO E RESOLUCAO
# --------------------------------------------------

resultado = tk.Label(
    janela,
    text="Resolva as tres equacoes.",
    font=("Arial", 11, "bold"),
    bg=FUNDO,
    fg=TEXTO,
    wraplength=620,
    justify="center"
)
resultado.pack(pady=8)

quadro_resolucao = tk.Frame(
    janela,
    bg="white",
    bd=1,
    relief="solid"
)
quadro_resolucao.pack(
    fill="x",
    padx=18,
    pady=5
)

resolucao = tk.Label(
    quadro_resolucao,
    text="A resolucao aparecera aqui apos verificar.",
    font=("Consolas", 10),
    bg="white",
    fg=TEXTO,
    justify="left",
    anchor="w",
    wraplength=620,
    padx=10,
    pady=10
)
resolucao.pack(fill="x")


def atualizar_informacoes():
    r, g, b = cor_original

    label_y.config(
        text=f"Intensidade de cinza: Y = {Y}"
    )

    label_rgb.config(
        text=f"R = {r}    G = {g}    B = {b}"
    )


atualizar_informacoes()

# --------------------------------------------------
# FORMATAR NUMEROS
# --------------------------------------------------

def numero(valor):
    if abs(valor - round(valor)) < 1e-9:
        return str(int(round(valor)))
    return f"{valor:.2f}".rstrip("0").rstrip(".")


# --------------------------------------------------
# VERIFICAR E MOSTRAR PASSO A PASSO
# --------------------------------------------------

def verificar():
    try:
        b_r = float(
            entradas["R"].get().replace(",", ".")
        )
        b_g = float(
            entradas["G"].get().replace(",", ".")
        )
        b_b = float(
            entradas["B"].get().replace(",", ".")
        )

    except ValueError:
        messagebox.showerror(
            "Entrada invalida",
            "Digite numeros validos nos tres campos."
        )
        return

    r, g, b = cor_original
    resposta_r, resposta_g, resposta_b = respostas

    # RGB reconstruido com as respostas digitadas
    tentativa = (
        round(A_R * Y + b_r),
        round(A_G * Y + b_g),
        round(A_B * Y + b_b)
    )

    acertou = tentativa == cor_original

    if acertou:
        resultado.config(
            text="CORRETO! Voce recuperou a cor original.",
            fg="#16803c"
        )
    else:
        resultado.config(
            text=(
                "RESPOSTA INCORRETA. Veja abaixo "
                "o calculo correto."
            ),
            fg="#c62828"
        )

    # Exibir a conta de cada canal
    texto_resolucao = (
        "COR ORIGINAL (RGB)\n"
        f"R = {r} | G = {g} | B = {b}\n\n"

        "1. CANAL VERMELHO\n"
        f"R = 1.0 x {Y} + bR\n"
        f"{r} = {numero(A_R * Y)} + bR\n"
        f"bR = {r} - {numero(A_R * Y)}\n"
        f"bR correto = {numero(resposta_r)}\n"
        f"Seu valor = {numero(b_r)}\n\n"

        "2. CANAL VERDE\n"
        f"G = 0.5 x {Y} + bG\n"
        f"{g} = {numero(A_G * Y)} + bG\n"
        f"bG = {g} - {numero(A_G * Y)}\n"
        f"bG correto = {numero(resposta_g)}\n"
        f"Seu valor = {numero(b_g)}\n\n"

        "3. CANAL AZUL\n"
        f"B = 1.5 x {Y} + bB\n"
        f"{b} = {numero(A_B * Y)} + bB\n"
        f"bB = {b} - {numero(A_B * Y)}\n"
        f"bB correto = {numero(resposta_b)}\n"
        f"Seu valor = {numero(b_b)}\n\n"

        "4. RGB RECONSTRUIDO COM SUA RESPOSTA\n"
        f"R = 1.0 x {Y} + ({numero(b_r)})"
        f" = {tentativa[0]}\n"
        f"G = 0.5 x {Y} + ({numero(b_g)})"
        f" = {tentativa[1]}\n"
        f"B = 1.5 x {Y} + ({numero(b_b)})"
        f" = {tentativa[2]}\n\n"

        f"RGB esperado: {cor_original}\n"
        f"RGB obtido:   {tentativa}"
    )

    resolucao.config(text=texto_resolucao)


# --------------------------------------------------
# NOVO DESAFIO
# --------------------------------------------------

def novo_desafio():
    global posicao_x, Y, cor_original, respostas

    posicao_x, Y, cor_original, respostas = criar_desafio()

    for entrada in entradas.values():
        entrada.delete(0, tk.END)

    resultado.config(
        text="Resolva as tres equacoes.",
        fg=TEXTO
    )

    resolucao.config(
        text="A resolucao aparecera aqui apos verificar."
    )

    atualizar_informacoes()
    atualizar_matriz()


# --------------------------------------------------
# BOTOES
# --------------------------------------------------

tk.Button(
    janela,
    text="Verificar resposta",
    command=verificar,
    font=("Arial", 11, "bold"),
    bg=AZUL,
    fg="white",
    activebackground="#1c5fa3",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=25,
    pady=6
).pack(pady=4)

tk.Button(
    janela,
    text="Novo desafio",
    command=novo_desafio,
    font=("Arial", 11),
    bg="#dce3ec",
    fg=TEXTO,
    relief="flat",
    cursor="hand2",
    width=25,
    pady=6
).pack(pady=(2, 12))

janela.mainloop()
