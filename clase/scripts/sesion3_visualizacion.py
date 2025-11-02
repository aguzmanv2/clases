from Bio import SeqIO
import matplotlib.pyplot as plt
from collections import Counter
import os, re

FASTA_PATH = "ls_orchid.fasta"
OUT_DIR = "graficos"

def contar_atgc(seq):
    s = str(seq).upper().replace('U', 'T')
    c = Counter(b for b in s if b in "ATGC")
    for b in "ATGC":
        c.setdefault(b, 0)
    return c

def grafico_pastel(counts, titulo, outfile):
    labels = ["A", "T", "G", "C"]
    sizes = [counts[l] for l in labels]
    total = sum(sizes)
    if total == 0:
        print(f"[AVISO] {titulo}: sin A/T/G/C válidas, no se genera imagen.")
        return
    fig, ax = plt.subplots()
    autopct = lambda p: f"{p:.1f}%\n({int(round(p*total/100))})"
    ax.pie(sizes, labels=labels, autopct=autopct, startangle=90)
    ax.axis('equal')  # pastel circular
    ax.set_title(titulo)
    plt.tight_layout()
    plt.savefig(outfile, dpi=200, bbox_inches="tight")
    plt.close(fig)

def safe_name(text):
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', text)[:60]

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    records = list(SeqIO.parse(FASTA_PATH, "fasta"))
    if not records:
        print("No se encontraron secuencias en el FASTA.")
        return
    for rec in records:
        counts = contar_atgc(rec.seq)
        fname = f"{OUT_DIR}/{safe_name(rec.id)}.png"
        grafico_pastel(counts, f"Composición A/T/G/C — {rec.id}", fname)
    total_counts = Counter()
    for rec in records:
        total_counts.update(contar_atgc(rec.seq))
    grafico_pastel(total_counts, "Composición total A/T/G/C (todas las secuencias)", f"{OUT_DIR}/_total.png")

if __name__ == "__main__":
    main()
