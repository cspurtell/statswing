import pandas as pd

def load_data(file_path):
    """Loads the player data from a CSV file"""
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f'Error: The file {file_path} could not be found.')
        return
    
def find_player(data, name):
    return data[data["Name"] == name]