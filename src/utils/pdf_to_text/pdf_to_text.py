from typing import Dict
from PyPDF2 import PdfReader

def extraer_pdf_como_hashmap(ruta_pdf: str) -> Dict[str, str]:
    #Lee un PDF y regresa un diccionario con el titulo y la descripcion

    reader = PdfReader(ruta_pdf)

    texto_paginas = []
    for page in reader.pages:
        pagina_texto = page.extract_text() or ""
        texto_paginas.append(pagina_texto)

    texto_completo = "\n".join(texto_paginas).strip()

    if not texto_completo:
        return {
            "titulo": "",
            "descripcion": ""
        }
    
    titulo=""
    if reader.metadata and reader.metadata.title:
        titulo = reader.metadata.title.strip()

    lineas = [linea.strip() for linea in texto_completo.splitlines()]
    lineas_no_vacias = [l for l in lineas if l]

    if not titulo:
        if lineas_no_vacias:
            titulo = lineas_no_vacias[0]
        else:
            titulo= ""

    

    descripacion = texto_completo
    if lineas_no_vacias and titulo == lineas_no_vacias[0]:

        usado = False 
        nuevas_lineas= []
        for l in lineas:
            if not usado and l == titulo:
                usado = True
                continue
            nuevas_lineas.append(l)
        descripacion = "\n".join(nuevas_lineas).strip()

    
    return {
        "titulo": titulo,
        "descripcion": descripacion
    }

if __name__ == "__main__":
    ruta = "INVESTMENT DECISION ANALYSIS ASSESSMENT OF.pdf"
    resultado = extraer_pdf_como_hashmap(ruta)
    print("TÍTULO:\n", resultado["titulo"])
    print("\nDESCRIPCIÓN (primeros 500 caracteres):\n")
    print(resultado["descripcion"][:500])



    