# testar_nome_18.py

import cv2
import pytesseract


# Caminho do Tesseract (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extrair_nome_da_imagem(imagem_path, x, y, w, h):
    img = cv2.imread(imagem_path)
    if img is None:
        print(f"[ERRO] Não consegui abrir a imagem: {imagem_path}")
        return ""

    h_img, w_img = img.shape[:2]

    # Ajusta limites
    x = max(0, x)
    y = max(0, y)
    x = min(x, w_img)
    y = min(y, h_img)
    w = min(w, w_img - x)
    h = min(h, h_img - y)

    if w <= 0 or h <= 0:
        print(f"[ERRO] Região inválida: x={x}, y={y}, w={w}, h={h}")
        return ""

    roi = img[y:y+h, x:x+w]

    # 1) Escala de cinza
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # 2) Aumenta contraste usando CLAHE (muito bom para texto fino/borrado)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # 3) Limiar adaptativo (bom para texto fino / cursivo)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15, 2
    )

    # 4) Inverte se o texto for claro em fundo escuro
    # (descomente se o nome estiver claro)
    # thresh = 255 - thresh

    # 5) Fechar pequenos buracos na letra
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # 6) Aumentar resolução bem mais
    scale = 3  # tenta 3, 4, 5
    thresh = cv2.resize(thresh, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # 7) OCR com foco em linhas de texto, português
    config = "--oem 3 --psm 7 -l por --psm 6"
    texto = pytesseract.image_to_string(thresh, config=config).strip()

    # 8) Limpeza mínima
    texto = "".join(c if c.isalpha() or c.isspace() else " " for c in texto)
    texto = " ".join(texto.split())

    # 9) Salva a ROI tratada para você ver
    cv2.imwrite("roi_nome_18.png", thresh)

    return texto


# ================================
#   TESTE DA PÁGINA 18
# ================================

x = 340
y = 724
w = 1121
h = 150

caminho_18 = r"C:\Projetos\Lab_IA\imagens\pagina_18.jpg"

print(f"Lendo nome da imagem: {caminho_18}")
print(f"Região: x={x}, y={y}, w={w}, h={h}")

nome = extrair_nome_da_imagem(caminho_18, x, y, w, h)
print(f"Nome extraído (repr): {repr(nome)}")