from readlif.reader import LifFile
import readlif
import os, json
import numpy as np
from tqdm import tqdm

lif_path = r"C:\Users\rwahe\Downloads\UkT06_phi020.lif" # Path to object

def ImageStack(LifImage, naming_convention):
    image_array = []
    if LifImage.settings['ScanMode'] == 'xyz':
        for frame, slice_z in enumerate(LifImage.get_iter_z()):
            frame_name = naming_convention + '_' + f'{frame:03d}'
            slice_array = np.array(slice_z)
            image_array.append(slice_array)

    elif LifImage.settings['ScanMode'] == 'xyt':
        for frame, slice_t in enumerate(LifImage.get_iter_t()):
            frame_name = naming_convention + '_' + f'{frame:03d}'
            slice_array = np.array(slice_t)
            image_array.append(slice_array)

def testcase(file_path):
    img_info = LifFile(file_path)
    pillow_object = img_info.get_image(0).get_frame(0)
    for image in tqdm(img_info.get_iter_image()):
        image_array = []
        if image.settings['ScanMode'] == 'xyz':
            for slice in image.get_iter_z():
                image_array.append(np.array(slice))
        if image.settings['ScanMode'] == 'xyt':
            for slice in image.get_iter_t():
                image_array.append(np.array(slice))
        print(image_array)

######### Begin non-work-in-progress functions #########

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
    
    print(img_info.get_image(0)) # Testing line
    
    # Store files in their own directory. This avoids cluttering!
    folder_name = img_info.get_image(0).path.removesuffix(r'/')
    
    # Rename if needed
    folder_name = folder_name if folder_name != 'Project' else input('This project was not named. Please name the file. \n')

    os.mkdir(folder_name)
    os.chdir(folder_name)
    file_prefix = folder_name + '_'
    
    for index, img in enumerate(img_info.get_iter_image()):
        filename = file_prefix + img.settings.get('ScanMode') + f'{index:03d}' if autoname == True else file_prefix + img.name
        ImageSequence(LifImage = img, naming_convention = filename)
        # ImageStack(LifImage = img, naming_convention = filename)
            
        #print(index, img)
    


if __name__ == '__main__':
    image_reader(lif_path)
    #testcase(lif_path)
