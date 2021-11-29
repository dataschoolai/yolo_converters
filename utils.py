#Import library for handling files and directories
from pathlib import Path
import shutil

#Define the function to create output directory
def make_output_dir(output_dir: str):
    """
    This function creates the output directory if it does not exist
    """
    #Create path object for output directory
    output_dir_path = Path(output_dir)
    #Check if output directory exists
    if output_dir_path.exists():
        #If it exists, delete it
        shutil.rmtree(output_dir_path)
    #Create output directory
    for path in output_dir_path, output_dir_path/'images', output_dir_path/'labels':
        #Create path object for each subdirectory
        path.mkdir(parents=True, exist_ok=True)
   #Return the output directory path
    return output_dir_path