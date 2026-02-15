#!/bin/bash
# ============================================================================
# CASE STUDY: Sistema di Bike Sharing Europeo (Dataset Reale)
# Parte 1: Download del Dataset
# ============================================================================
# Descrizione: Script per scaricare il dataset reale da GitHub

echo "============================================================================"
echo "DOWNLOAD EUROPEAN BIKE SHARING DATASET"
echo "============================================================================"

# Crea directory per i dati

# BASE_DIR="/home/corrado/Documenti/its/python.1/case_study_bikesharing/case_study_bikesharing_real/data"
BASE_DIR="/home/ITS_IA/IA_4/Bikesharing/data"


mkdir -p "$BASE_DIR"
cd "$BASE_DIR" || exit 1

echo ""
echo "1. Clonazione del repository GitHub..."
git clone https://github.com/TUMFTM/european-bike-sharing-dataset.git

echo ""
echo "2. Copia dei file sample nella directory di lavoro..."
cd european-bike-sharing-dataset
cp -r sample/* "$BASE_DIR/"

echo ""
echo "============================================================================"
echo "✓ DOWNLOAD COMPLETATO!"
echo "============================================================================"
echo ""
echo "I file sample (1000 righe) sono stati copiati in: $BASE_DIR"
echo ""
echo "File disponibili: $BASE_DIR"
echo ""
echo "Per usare il dataset completo (2.3 GB):"
echo "  cd european-bike-sharing-dataset/full"
echo "  unzip dataset.zip"
echo ""
