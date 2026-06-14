# Dataset — Country Flags

O dataset **não é versionado** neste repositório (≈200 MB). Baixe-o pela fonte original:

- **Roboflow Universe:** https://universe.roboflow.com/phamdata/country-flags-2t33e/dataset/4
- **Formato:** YOLOv8
- **Licença:** CC BY 4.0
- **Classes originais:** 88 → **86 após limpeza** (remoção de `Afghanistan` e `Albania`,
  que tinham anotações corrompidas)

## Como obter o dataset limpo

1. Baixe o dataset do Roboflow no formato **YOLOv8** (arquivo `.zip`).
2. Extraia e rode o script de limpeza:

   ```bash
   pip install pyyaml
   python ../scripts/limpar_dataset.py
   ```

   > Ajuste os caminhos `orig_base` e `clean_base` no início do script conforme a sua máquina.

3. O script gera uma pasta `dataset_clean/` com:
   - bounding boxes das classes 0 e 1 removidas (167 caixas);
   - 86 classes reindexadas (0–85);
   - `data.yaml` atualizado (`nc: 86`).

4. Compacte essa pasta em `dataset_clean.zip` e faça o upload no Colab quando o notebook pedir.
