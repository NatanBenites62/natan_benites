# mostra_coordenadas.py

import cv2
import matplotlib.pyplot as plt
import numpy as np

def on_click(event):
    if event.inaxes is not None:
        x, y = int(event.xdata), int(event.ydata)
        print(f"Coordenada: x={x}, y={y}")

# Caminho da imagem da prova
caminho_img = "imagens/pagina_18.jpg"

# Carrega a imagem com OpenCV
img = cv2.imread(caminho_img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Abre a imagem com matplotlib
fig, ax = plt.subplots(figsize=(10, 8))
ax.imshow(img)
ax.set_title("Clique com o botão esquerdo para ver coordenadas")

# Conecta o clique
fig.canvas.mpl_connect('button_press_event', on_click)

# Permite zoom e panning com o mouse
ax.axis('on')

plt.show()