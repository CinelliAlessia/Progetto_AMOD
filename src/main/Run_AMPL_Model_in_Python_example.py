import subprocess
import os


ampl_model = 'VRP_Andrea.mod'
ampl_data = '../resources/vrplib/DATs/A-n32-k5.dat'


def solve_ampl_model(ampl_model, ampl_data):
    """
    Esegue un modello AMPL specificato su un file di dati.

    Parameters:
    - ampl_model (str): Il percorso al file del modello AMPL (.mod).
    - ampl_data (str): Il percorso al file dei dati AMPL (.dat).

    Returns:
    - str: Uscita del risolutore AMPL.
    """
    if not os.path.exists(ampl_model):
        raise FileNotFoundError(f"Il file del modello {ampl_model} non esiste.")

    if not os.path.exists(ampl_data):
        raise FileNotFoundError(f"Il file dei dati {ampl_data} non esiste.")

    # Comando per eseguire AMPL
    ampl_command = "ampl"

    try:
        # Creare il file .run temporaneo con i comandi necessari
        run_file_content = f"""
        model {ampl_model};
        data {ampl_data};
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


# Esempio di utilizzo
output = solve_ampl_model(ampl_model, ampl_data)
print(output)
