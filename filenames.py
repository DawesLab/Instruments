def get_filename(root_path = "/home/photon/data/"):
    """
    Generate a filename for data files based on date and time
    """
    target_folder = datetime.datetime.now().strftime("%m-%d-%Y")
    if not os.path.exists(root_path + target_folder):
        os.makedirs(root_path + target_folder)
    os.chdir(root_path + target_folder)
    
    # based on time and date
    filename = datetime.datetime.now().strftime("%H-%M-%S")
    
    return filename
