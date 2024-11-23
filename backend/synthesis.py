import subprocess
import csv
import os

# Votre logique de synthèse de programme ici
# Importez les modules nécessaires (ProgSynth, etc.)

def create_dataset(dsl_name, path):
    command =["python3", path + dsl_name+"/convert_" + dsl_name + ".py", research_file_dataset(dsl_name, path), "-o", "synth_file/"+dsl_name + ".pickle" ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("La commande create_dataset s'est exécutée avec succès.")
    else:
        print(f"Erreur lors de l'exécution de la commande create_dataset: {result.stderr}")


def read_file(file):
    with open(file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for line in reader: 
            if line[1] != '':
                return line
    

def research_file_dataset(dsl_name, path):
    repertoire = path + dsl_name + "/dataset"

    for nom_fichier in os.listdir(repertoire):
        chemin_fichier = os.path.join(repertoire, nom_fichier)
        if os.path.isfile(chemin_fichier) and nom_fichier.endswith('.json'):
            return chemin_fichier

def run_synth(dsl_name, algo, solver, timeout):
    # Chargez le DSL, le dataset, le modèle et le PCFG en utilisant les chemins fournis
    # Créez une tâche à partir de la représentation de tâche donnée
    # Utilisez ProgSynth pour synthétiser le programme
    
    file = ""

    path = "../ProgSynth/examples/pbe/"

    create_dataset(dsl_name, path)
    
    command = ["python3", path + "solve.py", "--dsl", dsl_name, "--dataset", "synth_file/"  + dsl_name + ".pickle", "--search", algo, "--solver", solver, "--timeout", str(timeout)]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("La commande solve s'est exécutée avec succès.")
        file = dsl_name + "_" + algo + "_uniform_" + solver + ".csv"
        print(file)
    else:
        print(f"Erreur lors de l'exécution de la commande solve: {result.stderr}")

    # Retournez la solution synthétisée
    solution = read_file(file)
    return solution

