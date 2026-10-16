# Pipeline de control de presión arterial

**Integrantes:** Armas Netri Ignacio, Bogado Viscarra Tomás, Velles Aguirre Tomás

## Problema y usuario
Un equipo de salud recibe mediciones de presión arterial en CSV y JSON con errores de carga.
El programa descarta los registros inválidos, informa el motivo de cada rechazo y resume
la presión sistólica por grupo del estudio.

## Datos
Ver `data/README.md`. Cada fila corresponde a un paciente con una medición.

## Ejecución
No requiere bibliotecas externas (Python 3.10 o superior).
```bash
python src/main.py data/mediciones.csv
```

## Pruebas
```bash
python tests/test_pipeline.py
```

## Reglas de limpieza
- Código con formato `PAC-` y tres dígitos (expresión regular `PAC-\d{3}`).
- Edad entre 18 y 100 años.
- IMC entre 12 y 60 kg/m².
- Presión sistólica entre 70 y 250 mmHg.
- Grupo válido: solo "A" o "B".
- Valores faltantes, no numéricos o fuera de rango son rechazados.
- Se conservan las primeras apariciones de códigos duplicados.

## Resultado de ejemplo
Leídos: 58 | válidos: 50 | rechazados: 8
{'grupo': 'A', 'cantidad': 27, 'presion_media': 127.26, 'proporcion_hipertensos': 0.185}
{'grupo': 'B', 'cantidad': 23, 'presion_media': 118.61, 'proporcion_hipertensos': 0.13}

## Limitaciones
El umbral de hipertensión (>= 140 mmHg) es simplificado por motivos didácticos y no constituye un diagnóstico clínico real.
