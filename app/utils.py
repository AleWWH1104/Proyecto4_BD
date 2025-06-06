# app/utils.py
import pandas as pd
import os

def export_dataframe_to_csv(dataframe: pd.DataFrame, filename: str, directory: str = "reports_output"):
    """
    Exporta un DataFrame de pandas a un archivo CSV.

    Args:
        dataframe (pd.DataFrame): El DataFrame a exportar.
        filename (str): El nombre del archivo CSV (ej. "mi_reporte.csv").
        directory (str): El directorio donde se guardará el archivo CSV.
                         Por defecto, "reports_output".
    Returns:
        str: La ruta completa del archivo CSV exportado.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filepath = os.path.join(directory, filename)
    dataframe.to_csv(filepath, index=False)
    print(f"Reporte exportado exitosamente a: {filepath}")
    return filepath