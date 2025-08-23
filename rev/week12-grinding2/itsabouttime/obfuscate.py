import zlib
import base64

def obfuscate(filepath: str, output: str, layers: int = 49):
    with open(filepath, "rb") as f:
        data = f.read()

    wrapper = (
        "import paramiko\n"
        "import io\n"
        "import tkinter as tk\n"
        "from tkinter import messagebox\n\n"
        "_ = lambda __ : __import__(\"zlib\").decompress(__import__(\"base64\").b64decode(__[::-1]));"
    )

    for _ in range(layers):
        data = zlib.compress(data)
        data = base64.b64encode(data)
        data = data[::-1]
        # Wrap in exec structure with underscore lambda
        wrapped = f"{wrapper}exec((_)(b'{data.decode('latin1')}'))"
        data = wrapped.encode("latin1")

    with open(output, "wb") as f:
        f.write(data)

    print(f"Obfuscation complete. {layers} layers written to {output}")
    
obfuscate("tes.py", "chall.py")
