from collections import Counter

secuencia = "AAGTGGTGTGAATTGCAAGATCCCGTGAACCATCGAGTCTTTTGAACGCAAGTTGCGCCCGA"
def longitud(secuencia: str):
    s = ''.join(ch for ch in secuencia.upper() if not ch.isspace())
    longitud = len(s)

    freq = Counter(s)
    A = freq.get('A', 0)
    T = freq.get('T', 0)
    C = freq.get('C', 0)
    G = freq.get('G', 0)

    bases_validas = A + T + C + G
    otros = longitud - bases_validas

    porcentaje_gc = ((G + C) / bases_validas * 100) if bases_validas else 0.0

    return {
        "longitud": longitud,
        "conteos": {"A": A, "T": T, "C": C, "G": G},
        "otros": otros,
        "porcentaje_GC": round(porcentaje_gc, 2)
    }

resultado = longitud(secuencia)
print(resultado)