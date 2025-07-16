import wfdb

def load_annotations(atr_file_path: str):
    print(atr_file_path)
    """
    Carga las anotaciones desde un archivo .atr del MIT-BIH.

    Parámetros:
    - atr_file_path (str): Ruta base al archivo sin extensión (ej: 'AfiB/08405/08405')

    Retorna:
    - wfdb.Annotation: Objeto con los samples y aux_note del archivo .atr
    """
    try:
        annotation = wfdb.rdann(atr_file_path, 'atr')
        return annotation
    except Exception as e:
        print(f"[ERROR] No se pudo leer el archivo de anotaciones: {e}")
        return None


def extract_afib_segments(annotation, accepted_labels=None):
    """
    Filtra los segmentos de anotación que coincidan con etiquetas específicas.

    Parámetros:
    - annotation (wfdb.Annotation): Anotaciones cargadas
    - accepted_labels (list): Lista de etiquetas a conservar (default ['(AFIB', '(N'])

    Retorna:
    - List[Tuple[int, str]]: Lista de tuplas (sample_index, label)
    """
    if accepted_labels is None:
        accepted_labels = ['(AFIB', '(N']

    filtered = []
    for i in range(len(annotation.sample)):
        label = annotation.aux_note[i].strip()
        if label in accepted_labels:
            filtered.append((annotation.sample[i], label))

    return filtered
