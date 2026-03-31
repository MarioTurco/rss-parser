from typing import  Dict, Any
def read_query(file_path: str, params: Dict[str, Any]=None) -> str:
    """Reads and parametrizes a SQL query from a file and returns it as a string.
    Args:
        file_path (str): The path to the SQL file.
        params (Dict[str, Any]): The dictionary of parameters for the SQL query.
    Returns:
        str: The SQL query as a string.
    """
    if params is None:
        params = {}

    with open(file_path, 'r') as file:
        return file.read().format(**params)
    

def read_config_file(file_path: str) -> Dict[str, Any]:
    """Reads a configuration file and returns its contents as a dictionary.
    Args:
        file_path (str): The path to the configuration file.
    Returns:
        Dict[str, Any]: The contents of the configuration file as a dictionary.
    """
    pass 
    #TODO