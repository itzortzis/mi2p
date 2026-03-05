from abc import ABC, abstractmethod



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

    def __init__(self):
        pass

    
