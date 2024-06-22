"""
Token Extractor
Extractor de token para acceso API Servicios Banco XXX (versión 1.1)

Este programa permite extraer la clave de acceso API para utilizar los servicios del 
Banco XXX.

El programa operará como un microservicio invocado mediante:

        {path ejecutable}/getJason.py {path archivo JSON}/{nombre archivo JSON}.json [clave JSON]

ej.
        ./getJason.py ./sitedata.json

El token podrá recuperarse mediante el standard output de ejecución en el formato

       {1.0}XXXX-XXXX-XXXX-XXXX

Para obtener un mensaje de ayuda detallado ejecutar

       ./getJason.py -h

Para obtener la versión del programa ejecutar

       ./getJason.py -v

Excepciones

Todas las condiciones de error del programa deben producir un mensaje de error bajo su control antes de
terminar.

(c) UADER-FCyT-IS2©2024 todos los derechos reservados
"""

import json
import sys
from typing import Optional


class TokenExtractor:
    _instance = None
    _version = "1.1"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TokenExtractor, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, jsonfile: Optional[str] = None, jsonkey: str = "token1") -> None:
        self.jsonfile = jsonfile
        self.jsonkey = jsonkey

    def extract_token(self) -> str:
        try:
            with open(self.jsonfile, "r", encoding="utf-8") as myfile:
                data = myfile.read()
            obj = json.loads(data)
            return f"{{1.0}}{str(obj[self.jsonkey])}"
        except KeyError:
            return "Error: Clave no encontrada en el archivo JSON."
        except FileNotFoundError:
            return "Error: Archivo JSON no encontrado."
        except json.JSONDecodeError:
            return "Error: Archivo JSON con formato inválido."
        except Exception as e:
            return f"Error inesperado: {str(e)}"

    @staticmethod
    def print_help() -> None:
        print("Uso: getJason.py {path archivo JSON}/{nombre archivo JSON}.json [clave JSON]")
        print("Clave JSON por defecto: token1")
        print("Uso para ver la versión: getJason.py -v")

    @staticmethod
    def print_version() -> None:
        print(f"versión {TokenExtractor._version}")


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] == "-v":
        TokenExtractor.print_version()
        sys.exit(0)
    elif len(sys.argv) < 2 or len(sys.argv) > 3:
        TokenExtractor.print_help()
        sys.exit(1)

    jsonfile = sys.argv[1]
    jsonkey = "token1" if len(sys.argv) == 2 else sys.argv[2]
    jsonkey = "token2" if len(sys.argv) == 2 else sys.argv[2]

    extractor = TokenExtractor(jsonfile, jsonkey)
    result = extractor.extract_token()
    print(result)


if __name__ == "__main__":
    main()
