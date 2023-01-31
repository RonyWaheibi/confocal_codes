from readlif.reader import LifFile
import os, json
# This script creates a folder that breaks a LIF file into image sequences of TIF files and their metadata.
# 
# REQUIREMENTS:
# Must install PYTHON 3.10 (or newer) and the readlif module.
# Readlif module installation and documentation can be found here:
#       INSTALLATION AND OVERVIEW: https://pypi.org/project/readlif/
#       DOCUMENTATION: https://readlif.readthedocs.io/en/latest/
# 
# HOW TO USE
# Paste the file path on line 17. Leave the r in front, this is a raw string format.
# If metadata is undesired, comment out line 32.
# If any error occurs, you need to go into the file explorer to delete the folder that is created.

# Path to object
lif_path = r"C:\Users\Rony\Downloads\donuts_phi020_c08_xy.lif"

def SaveMetadata(metadata, naming_convention):
    # Save image metadata as .json 
    with open(naming_convention + '.json', mode = 'x') as outfile:
        json.dump(metadata, outfile)

def ImageSequence(LifImage, naming_convention):
    # Create folders with image sequences from .LIF files
    os.mkdir(naming_convention)
    os.chdir(naming_convention)
    SaveMetadata(metadata = LifImage.info, naming_convention = naming_convention)
        
    if LifImage.settings['ScanMode'] == 'xyz':
        for frame, slice_z in enumerate(LifImage.get_iter_z()):
            frame_name = naming_convention + '_' + f'{frame:03d}' + '.tif'
            slice_z.save(frame_name, format = 'TIFF')

    elif LifImage.settings['ScanMode'] == 'xyt':
        for frame, slice_t in enumerate(LifImage.get_iter_t()):
            frame_name = naming_convention + '_' + f'{frame:03d}' + '.tif'
            slice_t.save(frame_name, format = 'TIFF')
            
    os.chdir('..')

def image_reader(file_path):
    img_info = LifFile(file_path)

    rename_file_status = input("Do you want to automatically rename files? (Yes or no)")
    autoname = True if rename_file_status.lower() == 'yes' else False
    
    #print(img_info.get_image(0)) # Testing line. Use if curious about different methods
    
    # Store files in their own directory. This avoids cluttering!
    folder_name = img_info.get_image(0).path.removesuffix(r'/')
    os.mkdir(folder_name)
    os.chdir(folder_name)
    file_prefix = folder_name + '_'
    
    for index, img in enumerate(img_info.get_iter_image()):
        filename = file_prefix + img.settings.get('ScanMode') + f'{index:03d}' if autoname == True else file_prefix + img.name
        ImageSequence(LifImage = img, naming_convention = filename)
                
if __name__ == '__main__':
    image_reader(lif_path)
