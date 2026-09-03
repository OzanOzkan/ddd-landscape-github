import os
import yaml
import shutil
import utils.logger as logger

# Load job configuration YAML file
def load_config(config_path):
    with open(config_path, 'r') as stream:
        config = yaml.safe_load(stream)
    return config

# Create directory
def create_directory(path):
    try:
        # Check if the directory already exists
        if not os.path.exists(path):
            # Create the directory
            os.makedirs(path)
            logger.print_with_timestamp(f"Directory created: {path}")
        else:
            logger.print_with_timestamp(f"Directory already exists: {path}")
    except Exception as e:
        logger.print_with_timestamp(f"An error occurred while creating the directory: {e}")

# Delete directory
def delete_directory(dir):    
    # Delete the directory
    try:
        shutil.rmtree(dir)
        logger.print_with_timestamp(f"Deleted directory at: {dir}")
    except OSError as e:
        logger.print_with_timestamp(f"Error: {e.filename} - {e.strerror}.")