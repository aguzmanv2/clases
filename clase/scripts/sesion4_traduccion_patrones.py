from Bio.Seq import Seq
from Bio import SeqIO
import re
from datetime import datetime
from pathlib import Path

USE_FASTA = True
FASTA_PATH = "ls_orchid.fasta"
ONLY_FIRST_RECORD = False

MOTIFS = ["ATG", "GCGG", "GGG"]
OUT_TXT = "resultados_traduccion_motivos.txt"

def sanitize_dna(s: str) -> str:
    s = re.sub(r"\s+", "", s.upper())
    return s.replace("U", "T")

def translate_dna(dna: str, frame: int = 0, table: int = 1, to_stop: bool = False) -> str:
    seq = Seq(dna[frame:])
    return str(seq.translate(table=table, to_stop=to_stop))

def find_all_overlapping(seq: str, motif: str):
    seq, motif = seq.upper(), motif.upper()
    if not motif:
        return []
    positions = []
    start = 0
    while True:
        idx = seq.find(motif, start)
        if idx == -1:
            break
        positions.append(idx + 1)
        start = idx + 1
    return positions

def analyze_one_sequence(dna_raw: str, name: str):
    dna = sanitize_dna(dna_raw)

    protein = translate_dna(dna, frame=0, table=1, to_stop=False)

    rows = []
    for motif in MOTIFS:
        pos = find_all_overlapping(dna, motif)
        rows.append((motif, len(pos), pos))

    title = f"== Secuencia: {name} =="
    head = f"{'Motivo':<10} {'Recuento':>8}  Posiciones (1-based)"
    sep = "-" * 60
    lines = [title, head, sep]
    for motif, count, pos in rows:
        pos_str = ", ".join(map(str, pos)) if pos else "—"
        lines.append(f"{motif:<10} {count:>8}  {pos_str}")
    lines.append("")
    lines.append(f"Proteína (frame 0, tabla 1, to_stop=False):")
    lines.append(protein)
    lines.append("")

    return "\n".join(lines), lines

def main():
    all_lines = []
    header = [
        f"# Resultados de traducción y búsqueda de motivos",
        f"# Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"# Motivos: {', '.join(MOTIFS)}",
        ""
    ]
    all_lines.extend(header)

    if USE_FASTA:
        count = 0
        for rec in SeqIO.parse(FASTA_PATH, "fasta"):
            count += 1
            summary, lines = analyze_one_sequence(str(rec.seq), rec.id)
            print(summary)
            all_lines.extend(lines)
            all_lines.append("")
            if ONLY_FIRST_RECORD:
                break
        if count == 0:
            print("[AVISO] No se encontraron secuencias en el FASTA.")
    else:
        summary, lines = analyze_one_sequence(DNA_STR, "cadena_proporcionada")
        print(summary)
        all_lines.extend(lines)

    Path(OUT_TXT).write_text("\n".join(all_lines), encoding="utf-8")
    print(f"Resultados guardados en: {OUT_TXT}")

if __name__ == "__main__":
    main()
