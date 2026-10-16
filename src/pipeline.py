import re
import csv
from modelo import Paciente

PATRON_CODIGO = re.compile(r"PAC-\d{3}")

RANGOS = {
    "edad": (18, 100),
    "imc": (12, 60),
    "presion_sistolica": (70, 250)
}
GRUPOS_VALIDOS = {"A", "B"}

def convertir_numero(valor):
    if valor is None or (isinstance(valor, str) and valor.strip() == ""):
        return None
    return float(valor)

def validar_registro(registro):
    motivos = []
    
    if not PATRON_CODIGO.fullmatch(str(registro.get("codigo", ""))):
        motivos.append("código con formato inválido")
        
    for campo in ["edad", "imc", "presion_sistolica"]:
        valor_bruto = registro.get(campo)
        try:
            valor_num = convertir_numero(valor_bruto)
            if valor_num is None:
                motivos.append(f"{campo} faltante")
            else:
                min_val, max_val = RANGOS[campo]
                if not (min_val <= valor_num <= max_val):
                    motivos.append(f"{campo} fuera de rango")
        except ValueError:
            motivos.append(f"{campo} no numérico")
            
    if registro.get("grupo") not in GRUPOS_VALIDOS:
        motivos.append("grupo inválido")
        
    return motivos

def limpiar(registros):
    validos = []
    rechazos = []
    codigos_aceptados = set()
    
    for indice, registro in enumerate(registros, start=1):
        motivos = validar_registro(registro)
        codigo = str(registro.get("codigo", ""))
        
        if not motivos and codigo in codigos_aceptados:
            motivos.append("código duplicado")
            
        if motivos:
            rechazos.append({
                "fila": indice,
                "codigo": codigo,
                "motivo": "; ".join(motivos)
            })
        else:
            codigos_aceptados.add(codigo)
            paciente = Paciente(
                codigo=codigo,
                edad=convertir_numero(registro["edad"]),
                imc=convertir_numero(registro["imc"]),
                presion=convertir_numero(registro["presion_sistolica"]),
                grupo=registro["grupo"]
            )
            validos.append(paciente)
            
    return validos, rechazos

def generar_reporte(pacientes):
    reporte = []
    for grupo in ["A", "B"]:
        pacientes_grupo = [p for p in pacientes if p.grupo == grupo]
        cantidad = len(pacientes_grupo)
        
        if cantidad > 0:
            presion_media = round(sum(p.presion for p in pacientes_grupo) / cantidad, 2)
            hipertensos = sum(1 for p in pacientes_grupo if p.es_hipertenso())
            proporcion = round(hipertensos / cantidad, 3)
        else:
            presion_media = 0.0
            proporcion = 0.0
            
        reporte.append({
            "grupo": grupo,
            "cantidad": cantidad,
            "presion_media": presion_media,
            "proporcion_hipertensos": proporcion
        })
        
    return reporte

def guardar_csv(filas, ruta):
    if not filas:
        return
        
    claves = list(filas[0].keys())
    with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=claves)
        escritor.writeheader()
        escritor.writerows(filas)
