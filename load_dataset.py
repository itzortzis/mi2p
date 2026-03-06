from abc import ABC, abstractmethod
import os
import csv
import glob
import pydicom
import matplotlib.pyplot as plt


class LoadDataset(ABC):




    @abstractmethod
    def load_metadata(self, path):
        pass

    @abstractmethod
    def load_images(self, file_list):
        pass

    @abstractmethod
    def load_masks(self, file_list):
        pass



class INbreastLoader(LoadDataset):

    def __init__(self, root):
        self.csv_path = os.path.join(root, "INbreast.csv")
        self.dcm_path = os.path.join(root, "AllDICOMs")
        self.xml_path = os.path.join(root, "AllDICOMs")
        self.meta_list = []

        self.load_metadata(self.csv_path)
        self.load_images("")


    def load_metadata(self, path):
        
        with open(path) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            header = next(reader)

            for row in reader:
            
                self.meta_list.append({
                    "filename": row[5],
                    "acr": row[6],
                    "birads": row[7]
                })


    def get_path(self, path, file_id):
        pattern = os.path.join(path, f"{file_id}*.dcm")
        matches = glob.glob(pattern)
        return matches[0] if matches else None


    def load_images(self, file_list):
        for item in self.meta_list:
            dcm_path = self.get_path(self.dcm_path, item['filename'])
            if dcm_path == None:
                continue
            ds = pydicom.dcmread(dcm_path)
            img = ds.pixel_array

            plt.figure()
            plt.imshow(img, cmap='gray')
            plt.savefig('test.png')
            break


    def load_masks(self, file_list):
        pass

    

    
