import numpy as np
import cv2


class MI2P():

    def __init__(self, img, mask):
        self.N = 10
        self.W = 1024
        self.ratio = 0.8
        self.attempts = 200
        self.img = img
        self.mask = mask
        self.patches = []
        self.p_size = 256
        self.patches = np.zeros((self.N, self.p_size, self.p_size, 2))


        self.run()

    
    def run(self):
        self.get_bbox(self.mask)
        if self.blob != None:
            self.extract_tumor_patches()
        else:
            self.extract_healthy_patches()

    
    def get_bbox(self, mask):

        rows = np.any(mask, axis=0)
        cols = np.any(mask, axis=1)
        
        if not np.any(rows) or not np.any(cols):
            self.blob = None
            return
            
        ymin, ymax = np.where(rows)[0][[0, -1]]
        xmin, xmax = np.where(cols)[0][[0, -1]]
        
        self.blob = (xmin, ymin, xmax, ymax)
    


    def extract_tumor_patches(self):
        print("tumor", self.blob)
        x_min = max(self.blob[2] - self.W, 0)
        x_max = self.blob[0]

        y_min = max(self.blob[3] - self.W, 0)
        y_max = self.blob[1]

        print(x_min, x_max, y_min, y_max)

        x_space = np.arange(x_min, x_max)
        if len(x_space) < self.N:
            x_max = self.N + 1
            x_space = np.arange(x_min, x_max)
        y_space = np.arange(y_min, y_max)
        if len(y_space) < self.N:
            y_max = self.N + 1
            y_space = np.arange(y_min, y_max)
        
        xs = np.random.choice(x_space, size=self.N, replace=False)
        ys = np.random.choice(y_space, size=self.N, replace=False)

        patch = np.zeros((self.N, self.W, self.W, 2))
        for i in range(len(xs)):
             
            
            patch = self.img[xs[i]: xs[i] + self.W, ys[i]: ys[i] + self.W]
            patch = cv2.resize(patch, dsize=(self.p_size, self.p_size), interpolation=cv2.INTER_CUBIC)
            self.patches[i, :, :, 0] = patch
            
            patch_mask = self.mask[xs[i]: xs[i] + self.W, 
                                                        ys[i]: ys[i] + self.W]
            patch_mask = cv2.resize(patch_mask, 
                dsize=(self.p_size, self.p_size), interpolation=cv2.INTER_CUBIC)
            self.patches[i, :, :, 1] = patch_mask

    
    def extract_healthy_patches(self):
        print("healthy")
        n = self.N - 1

        idx = 0
        while n > 0 and self.attempts > 0:
            y0 = np.random.randint(0, self.img.shape[1] - self.W)
            x0 = np.random.randint(0, self.img.shape[0] - self.W)

            candidate_area = self.img[x0: x0+self.W, y0: y0+self.W]
            
            tissue_area  = np.count_nonzero(candidate_area)
            patch_area = candidate_area.shape[0] ** 2

            ratio = tissue_area / patch_area
            
            if ratio >= self.ratio:
                patch = cv2.resize(candidate_area, 
                                dsize=(self.p_size, self.p_size), 
                                        interpolation=cv2.INTER_CUBIC)
                self.patches[idx, :, :, 0] =  patch
                idx += 1
                n -= 1
            self.attempts -= 1
        
        self.patches = self.patches[:idx]

            

