from abc import ABC, abstractmethod
from mi2p import MI2P
import os
import csv
import glob
import random
import pydicom
import matplotlib.pyplot as plt
from inbreastxmlparser.annotation import INbreastAnnotation



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
        self.xml_path = os.path.join(root, "AllXML")
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


    def get_dicom_path(self, path, file_id):
        pattern = os.path.join(path, f"{file_id}*.dcm")
        matches = glob.glob(pattern)
        return matches[0] if matches else None


    def load_img_mask(self, filename):
        dcm_path = self.get_dicom_path(self.dcm_path, filename)
        if dcm_path == None:
            return None
        ds = pydicom.dcmread(dcm_path)
        img = ds.pixel_array

        mask_path = os.path.join(self.xml_path, f"{filename}.xml")
        mask_obj = INbreastAnnotation(self.xml_path, filename, img.shape)
        mask = mask_obj.mask[:, :, 0]

        return img, mask


    def load_images(self, file_list):

        # random.shuffle(self.meta_list)
        # for item in self.meta_list:
            item = self.meta_list[4]
            data = self.load_img_mask(item["filename"])
            # if data == None:
            #     continue

            img, mask = data
            print("Data: ", img.shape, mask.shape)


            plt.figure()
            plt.imshow(img, cmap='gray')
            plt.savefig(f'test.png')

            plt.close()
            
            m = MI2P(img, mask)
            print(len(m.patches))
            for p in range(len(m.patches)):

                plt.figure()
                plt.imshow(m.patches[p, :, :, 0], cmap='gray')
                plt.savefig(f'test{p}.png')

                plt.close()
                plt.figure()
                plt.imshow(m.patches[p, :, :, 1], cmap='gray')
                plt.savefig(f'test_mask{p}.png')
                plt.close()

                plt.figure()
                plt.imshow(m.patches[p, :, :, 0], cmap='gray')
                plt.imshow(m.patches[p, :, :, 1], alpha=0.3)
                plt.savefig(f'test_mask_hover{p}.png')
                plt.close()

            
            # break


    def load_masks(self, file_list):
        pass

    

    
