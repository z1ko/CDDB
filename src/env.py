
import os

# Carica variabile se presente altrimenti esce con panic
def get_env_panic(name: str) -> str:

    result = os.getenv(name)
    if result != None:
        return result

    print("[E] La variabile " + name + " non è stata trovata, termino.")
    exit(1)
