"""
Token Extractor and Payment Processor
Extractor de token para acceso API Servicios Banco XXX (versión 1.2)

(c) UADER-FCyT-IS2©2024 todos los derechos reservados
"""

import json
import sys
from typing import Optional, List, Dict, Any


class TokenExtractor:
    _instance = None
    _version = "1.2"

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


class Payment:
    def __init__(self, order_id: int, token: str, amount: float) -> None:
        self.order_id = order_id
        self.token = token
        self.amount = amount


class PaymentIterator:
    def __init__(self, payments: List[Payment]) -> None:
        self._payments = payments
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._payments):
            result = self._payments[self._index]
            self._index += 1
            return result
        raise StopIteration


class PaymentProcessor:
    def __init__(self, jsonfile: str) -> None:
        self.extractor = TokenExtractor(jsonfile)
        self.balances = {
            "token1": 1000.0,
            "token2": 2000.0
        }
        self.payments: List[Payment] = []

    def process_payment(self, order_id: int, amount: float) -> str:
        if self.balances["token1"] >= amount:
            token = "token1"
        elif self.balances["token2"] >= amount:
            token = "token2"
        else:
            return "Error: Fondos insuficientes en ambas cuentas."

        self.balances[token] -= amount
        payment = Payment(order_id, token, amount)
        self.payments.append(payment)
        token_key = self.extractor.extract_token()
        return f"Orden {order_id}: Pago de ${amount} realizado usando {token} ({token_key})"

    def list_payments(self) -> None:
        iterator = PaymentIterator(self.payments)
        for payment in iterator:
            print(f"Orden {payment.order_id}: ${payment.amount} - {payment.token}")


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] == "-v":
        TokenExtractor.print_version()
        sys.exit(0)
    elif len(sys.argv) < 3 or len(sys.argv) > 3:
        TokenExtractor.print_help()
        sys.exit(1)

    jsonfile = sys.argv[1]
    amount = 500.0  # Monto fijo para los pagos en este ejemplo
    processor = PaymentProcessor(jsonfile)

    # Procesar algunos pagos como ejemplo
    print(processor.process_payment(1, amount))
    print(processor.process_payment(2, amount))
    print(processor.process_payment(3, amount))

    # Listar todos los pagos realizados
    processor.list_payments()


if __name__ == "__main__":
    main()
