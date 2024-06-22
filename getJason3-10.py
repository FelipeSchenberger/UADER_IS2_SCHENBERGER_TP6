import json, sys

def print_help():
    print("Uso: getJason.py {path archivo JSON}/{nombre archivo JSON}.json [clave JSON]")
    print("Clave JSON por defecto: token1")

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print_help()
    sys.exit(1)

jsonfile = sys.argv[1]
jsonkey = "token1" if len(sys.argv) == 2 else sys.argv[2]
jsonkey = "token2" if len(sys.argv) == 2 else sys.argv[2]

try:
    with open(jsonfile, "r") as myfile:
        data = myfile.read()
    obj = json.loads(data)
    print(f"{{1.0}}{str(obj[jsonkey])}")
except Exception as e:
    print(f"Error: {str(e)}")
