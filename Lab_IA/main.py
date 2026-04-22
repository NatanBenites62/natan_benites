import json
import os
import pandas as pd
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from src.le_nome_prova import extrair_nome_da_imagem
from src.leitor_pdf import pdf_para_imagens
from src.leitor_qr import ler_qr_code, parse_qr_data
from src.ocr_respostas import extrair_respostas
from src.correcao import calcular_acertos_por_area
from src.relatorio import gerar_graficos, gerar_grafico_por_aluno
from ia_helper import ia_gerar_texto


# 1) Carregar gabarito do JSON
caminho_gabarito = os.path.join(os.path.dirname(__file__), "gabarito_oficial.json")

with open(caminho_gabarito, "r", encoding="utf-8") as f:
    dados = json.load(f)

GABARITO = {int(k): v for k, v in dados["gabarito"].items()}
AREAS = dados["areas"]


# 2) Configurar pastas e checar o PDF
data_path = os.path.join(os.path.dirname(__file__), "data", "Image_101.pdf")
if not os.path.exists(data_path):
    raise FileNotFoundError(
        "Coloque o arquivo Image_101.pdf na pasta data/"
    )


# 3) Lista para guardar resultados (mais eficiente que DataFrame incremental)
resultados = []


print("Convertendo PDF para imagens...")
caminhos_imagens = pdf_para_imagens(data_path, "imagens")


print("Processando cada aluno...")

# verifica o QR da primeira página (opcional, para teste)
print("Verificando leitura de QR Code na primeira página...")
if caminhos_imagens:
    caminho_teste = caminhos_imagens[0]
    print("Caminho da imagem de teste:", caminho_teste)

    qr_raw = ler_qr_code(caminho_teste)
    print("Raw QR lido (repr):", repr(qr_raw))

    infos = parse_qr_data(qr_raw)
    print("Infos parseadas:", infos)
else:
    print("Nenhuma imagem foi gerada. Verifique o PDF.")


for i, caminho_img in enumerate(caminhos_imagens):
    print(f"Processando página {i+1}...")

    # 2.1) Ler QR Code
    qr_text = ler_qr_code(caminho_img)
    infos = parse_qr_data(qr_text)

    # 2.2) Escolher coordenadas do campo "NOME" (cursivo na página 18, outros padrão)
    # As coordenadas mudam quando a página é 18
    # Se você já tiver ajustado para condição por nome de arquivo, pode usar:
    if "pagina_18" in caminho_img.lower():
        x_nome = 328
        y_nome = 724
        w_nome = 1121   # 1449 - 328
        h_nome = 133    # 857 - 724
    else:
        x_nome = 302
        y_nome = 680
        w_nome = 450
        h_nome = 40

    # Tenta ler o nome do aluno via OCR
    nome_ocr = extrair_nome_da_imagem(caminho_img, x_nome, y_nome, w_nome, h_nome)

    # Se o OCR não conseguiu ler um nome válido, usa o nome do QR
    if nome_ocr.strip():
        nome = nome_ocr.strip()
    else:
        nome = infos.get("nome", "Aluno_Desconhecido")

    matricula = infos.get("matricula", "XXXX")
    ano       = infos.get("ano",       "N/A")
    bimestre  = infos.get("bimestre",  "N/A")
    turma     = infos.get("turma",     "N/A")
    escola    = infos.get("escola",    "N/A")

    # 3.2) Extrair respostas do aluno
    respostas = extrair_respostas(caminho_img)

    # 3.3) Calcular acertos por área
    acertos, totais = calcular_acertos_por_area(respostas, GABARITO, AREAS)

    # 3.4) Se quiser, calcular a taxa_geral já no loop
    taxa_geral = (
        sum(acertos.values()) / sum(totais.values()) * 100
        if sum(totais.values()) > 0 else 0.0
    )

    # 3.5) Criar linha de resultado e guardar na lista
    nova_linha = {
        "nome": nome,
        "matricula": matricula,
        "escola": escola,
        "turma": turma,
        "acertos_portugues": acertos["Português"],
        "total_portugues": totais["Português"],
        "acertos_matematica": acertos["Matemática"],
        "total_matematica": totais["Matemática"],
        "acertos_ciencias_n": acertos["Ciências da Natureza"],
        "total_ciencias_n": totais["Ciências da Natureza"],
        "acertos_ciencias_h": acertos["Ciências Humanas"],
        "total_ciencias_h": totais["Ciências Humanas"],
        "acertos_total": sum(acertos.values()),
        "total_questoes": sum(totais.values()),
        "taxa_geral": taxa_geral
    }
    resultados.append(nova_linha)


print("Cálculo de acertos concluído.")


# Criar DataFrame a partir da lista de resultados
df = pd.DataFrame(resultados)


# 4) Gerar gráficos e salvar PNG
# 4) Gerar gráficos e salvar PNG
print("Gerando gráficos...")
gerar_graficos(df, output_path="graficos_acertos.png")
gerar_grafico_por_aluno(df, output_path="grafico_acertos_por_aluno.png")


# 5) Gerar gráficos de análise e relatório em texto
print("Encontrando melhores alunos...")
# encontrar_melhores_alunos(df)   # se você ainda tiver essa função


# 6) Salvar relatório em CSV
relatorio_csv = os.path.join(os.path.dirname(__file__), "relatorio_desempenho.csv")
df.to_csv(relatorio_csv, index=False)
print(f"Relatório salvo em '{relatorio_csv}'.")


# 7) (Opcional) Chamar Mistral para gerar comentário textual
try:
    relatorio_texto = df.to_string()
    prompt = (
        "Sou professor de um curso de Sistemas de Informação. "
        "Este é o relatório de desempenho de uma prova com 24 questões, divididas em 4 áreas. "
        "Por favor, escreva um comentário em português, explicando o desempenho geral e por área, "
        "e sugira o que os alunos poderiam melhorar. "
        f"Relatório:\n{relatorio_texto}"
    )
    comentario = ia_gerar_texto(prompt)

    # Salva o comentário do Mistral em arquivo para o app web
    relatorio_ia_path = os.path.join(os.path.dirname(__file__), "relatorio_ia.txt")
    with open(relatorio_ia_path, "w", encoding="utf-8") as f:
        f.write(comentario)

    print("\nComentário do modelo Mistral:")
    print(comentario)

except Exception as e:
    print("Erro ao chamar o modelo Mistral (verifique a chave API e a conexão):", str(e))