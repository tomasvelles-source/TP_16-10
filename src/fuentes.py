import csv
import json
from abc import ABC, abstractmethod

class FuenteDatos(ABC):
    @abstractmethod
    def cargar(self, ruta):
        pass

class FuenteCSV(FuenteDatos):
    def cargar(self, ruta):
        with open(ruta, mode='r', encoding='utf-8', newline='') as archivo:
            lector = csv.DictReader(archivo)
            return list(lector)

class FuenteJSON(FuenteDatos):
    def cargar(self, ruta):
        with open(ruta, mode='r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            if not isinstance(datos, list):
                raise ValueError("El contenido del JSON no es una lista.")
            return datos
