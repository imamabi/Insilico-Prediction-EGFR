# Workflow for Insilico Prediction for Drug Resistance in EGFR
## Overview

This project focuses on predicting drug resistance in Epidermal Growth Factor Receptor (EGFR) using in-silico methods. The workflow encompasses protein structure prediction, molecular dynamics simulations, clustering analysis, virtual screening, enrichment analysis, and experimental verification. The ultimate goal is to identify top hit compounds that could potentially overcome drug resistance in EGFR.

## Workflow
### 1. Prediction of Wild-Type and Mutant EGFR Structures
Tool: AlphaFold

Description: Predict the structures of Wild-Type (WT) EGFR and its mutants (T790M, L858R, and Del19).

Output: Predicted 3D structures of WT and mutant EGFR proteins.

### 2. Molecular Dynamics Simulations
Tool: GROMACS

Description: Run molecular dynamics simulations to sample conformations of the predicted EGFR structures.

Output: Trajectories of EGFR structures in various conformational states.

### 3. Clustering Analysis
Tool: GROMOS

Description: Perform clustering based on the root-mean-square deviation (RMSD) of the binding pocket residues.

Output: Representative structures of EGFR binding pockets.

### 4. Virtual Screening
Tool: Vina MPI

Description: Conduct structure-based virtual screening using the DUD-E dataset and the representative structures from clustering.

Output: Docking scores and poses of potential drug compounds.

### 5. Enrichment Analysis
Tool: Custom Scripts

Description: Perform enrichment analysis to identify the top hit compounds from the virtual screening results.

Output: List of top hit compounds with their respective docking scores.

### 6. Experimental Verification
Description: Validate the top hit compounds through experimental assays to confirm their efficacy against drug-resistant EGFR.
