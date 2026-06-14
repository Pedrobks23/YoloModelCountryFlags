"""
Script de limpeza do dataset Country Flags
Remove as classes 0 e 1 (Afghanistan e Albania), reindexando as demais.
Cria uma cópia limpa em dataset_clean — nunca toca o original.
"""

import os
import shutil
import yaml

orig_base  = r"C:\Users\pedro\Downloads\ProjetoCienciaDeDados\dataset_original"
clean_base = r"C:\Users\pedro\Downloads\ProjetoCienciaDeDados\dataset_clean"

# ── 1. Copiar dataset completo ──────────────────────────────────────────────
if os.path.exists(clean_base):
    shutil.rmtree(clean_base)
shutil.copytree(orig_base, clean_base)
print(f"Cópia criada em: {clean_base}")

# ── 2. Ler yaml original ────────────────────────────────────────────────────
with open(os.path.join(orig_base, "data.yaml"), "r", encoding="utf-8") as f:
    original = yaml.safe_load(f)

original_names = original["names"]
original_nc    = original["nc"]

removed_names  = original_names[:2]   # Afghanistan, Albania
new_names      = original_names[2:]   # 86 classes restantes
new_nc         = len(new_names)

print(f"\n== ANTES ==")
print(f"nc    : {original_nc}")
print(f"names[0]: {original_names[0]}")
print(f"names[1]: {original_names[1]}")
print(f"\n== DEPOIS ==")
print(f"nc    : {new_nc}")
print(f"names[0]: {new_names[0]}")
print(f"names[1]: {new_names[1]}")
print(f"Removidos: {removed_names}")

# ── 3. Processar arquivos de label ──────────────────────────────────────────
stats = {"removed": 0, "kept": 0, "files": 0}

for split in ["train", "valid", "test"]:
    label_dir = os.path.join(clean_base, split, "labels")
    if not os.path.isdir(label_dir):
        continue
    for fname in os.listdir(label_dir):
        if not fname.endswith(".txt"):
            continue
        fpath = os.path.join(label_dir, fname)
        with open(fpath, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            cls_id = int(parts[0])
            if cls_id in (0, 1):
                stats["removed"] += 1
                continue
            new_cls = cls_id - 2        # reindexar: 2→0, 3→1, … 87→85
            new_lines.append(f"{new_cls} {' '.join(parts[1:])}\n")
            stats["kept"] += 1

        with open(fpath, "w") as f:
            f.writelines(new_lines)
        stats["files"] += 1

print(f"\nArquivos .txt processados : {stats['files']}")
print(f"BBoxes removidas (cls 0,1): {stats['removed']}")
print(f"BBoxes mantidas/reindexadas: {stats['kept']}")

# ── 4. Escrever novo data.yaml ──────────────────────────────────────────────
new_yaml = {
    "train": "train/images",
    "val"  : "valid/images",
    "test" : "test/images",
    "nc"   : new_nc,
    "names": new_names,
}

yaml_path = os.path.join(clean_base, "data.yaml")
with open(yaml_path, "w", encoding="utf-8") as f:
    yaml.dump(new_yaml, f, sort_keys=False, allow_unicode=True, default_flow_style=None)

print(f"\ndata.yaml atualizado em: {yaml_path}")
print("Limpeza concluída com sucesso!")
