from Bio import SeqIO
from statistics import mean
from pathlib import Path

FASTA_PATH = "ls_orchid.fasta"
SAVE_TXT = True
OUT_TXT = "resumen_longitudes.txt"

def main():
    ids = []
    longitudes = []

    for record in SeqIO.parse(FASTA_PATH, "fasta"):
        ids.append(record.id)
        longitudes.append(len(record.seq))

    if not longitudes:
        print(f"[AVISO] No se encontraron secuencias en: {FASTA_PATH}")
        return

    n = len(longitudes)
    promedio = mean(longitudes)
    max_len = max(longitudes)
    idx_max = [i for i, L in enumerate(longitudes) if L == max_len]
    id_max = ids[idx_max[0]]
    empates = len(idx_max) - 1

    print(f"Resumen estadístico — {FASTA_PATH}")
    print("-" * 50)
    print(f"Número total de secuencias: {n}")
    print(f"Longitud promedio: {promedio:.2f} bases")
    print(
        f"Secuencia más larga: {id_max} ({max_len} bases)"
        + (f"  (+{empates} con igual longitud)" if empates > 0 else "")
    )
    print("\nLongitudes (en orden de archivo):")
    for i, (id_, L) in enumerate(zip(ids, longitudes), start=1):
        print(f"{i:>3}. {id_}: {L}")

    if SAVE_TXT:
        lineas = [
            f"Resumen estadístico — {FASTA_PATH}",
            "-" * 50,
            f"Número total de secuencias: {n}",
            f"Longitud promedio: {promedio:.2f} bases",
            f"Secuencia más larga: {id_max} ({max_len} bases)"
            + (f"  (+{empates} con igual longitud)" if empates > 0 else ""),
            "",
            "Longitudes (en orden de archivo):",
            *[f"{i:>3}. {id_}: {L}" for i, (id_, L) in enumerate(zip(ids, longitudes), start=1)],
        ]
        Path(OUT_TXT).write_text("\n".join(lineas), encoding="utf-8")
        print(f"\nResumen guardado en: {OUT_TXT}")

if __name__ == "__main__":
    main()
