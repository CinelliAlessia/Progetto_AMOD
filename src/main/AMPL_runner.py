import subprocess
import os

model_file = 'VRP_Andrea.mod'
data_dir = '../resources/vrplib/DATs'


def solve_ampl_model(model_file, data_file):
    """
    Esegue un modello AMPL con un file di dati specifico.

    Parameters:
    - model_file (str): Il percorso al file del modello AMPL (.mod).
    - data_file (str): Il percorso al file dei dati AMPL (.dat).

    Returns:
    - str: Output del risolutore AMPL.
    """
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Il file del modello {model_file} non esiste.")

    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Il file dei dati {data_file} non esiste.")

    ampl_command = "ampl"

    try:
        # Creare il file .run temporaneo con i comandi necessari
        run_file_content = f"""
        model {model_file};
        data {data_file};
        solve;
        display x, y, Total_Cost;
        """

        with open('temp.run', 'w') as run_file:
            run_file.write(run_file_content)

        # Eseguire AMPL con il file .run
        result = subprocess.run([ampl_command, 'temp.run'], capture_output=True, text=True)

        # Rimuovere il file temporaneo .run dopo l'esecuzione
        os.remove('temp.run')

        return result.stdout

    except Exception as e:
        raise RuntimeError(f"Errore durante l'esecuzione di AMPL: {e}")



# Funzione per risolvere più istanze
def solve_multiple_instances(model_file, data_dir):
    """
    Esegue un modello AMPL su tutti i file di dati in una directory specificata.

    Parameters:
    - model_file (str): Il percorso al file del modello AMPL (.mod).
    - data_dir (str): Il percorso alla directory contenente i file dei dati (.dat).
    """
    for filename in os.listdir(data_dir):
        if filename.endswith('.dat'):
            data_file = os.path.join(data_dir, filename)
            print(f"Solving for {data_file}")
            output = solve_ampl_model(model_file, data_file)
            print(output)


# Esempio di utilizzo per più istanze
solve_multiple_instances(model_file, data_dir)
