
import numpy as np




class MI2P(self):

    def __init__(self, img, mask):
        self.N = 10
        self.W = 512
        self.ratio = 0.8
        self.attempts = 200
        self.img = img
        self.mask = mask
        self.patches = []
        self.patches = np.zeros((self.N, self.W, self.W, 2))

        self.run()

    
    def run(self):
        self.get_bbox()
        if self.blob != None:
            self.extract_tumor_patches()
        else:
            self.extract_healthy_patches()

    
    def get_bbox(mask):

        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            self.blob = None
            
        ymin, ymax = np.where(rows)[0][[0, -1]]
        xmin, xmax = np.where(cols)[0][[0, -1]]
        
        self.blob = (xmin, ymin, xmax, ymax)
    


    def extract_tumor_patches(self):
        x_min = self.blob.xmax - self.W
        x_max = self.blob.xmin

        y_min = self.blob.ymax - self.W
        y_max = self.blob.ymin

        xs = np.random.choice(np.arange(x_min, x_max), 
                                                size=self.N, replace=False)
        ys = np.random.choice(np.arange(y_min, y_max), 
                                                size=self.N, replace=False)

        patch = np.zeros((self.N, self.W, self.W, 2))
        for i in range(len(xs)):
            self.patches[i, :, :, 0] = self.img[xs[i]: xs[i] + self.W, 
                                                        ys[i]: ys[i] + self.W]
            self.patches[i, :, :, 1] = self.mask[xs[i]: xs[i] + self.W, 
                                                        ys[i]: ys[i] + self.W]

    
    def extract_healthy_patches(self):
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
                self.patches[idx, :, :, 0] =  candidate_area
                idx += 1
                n -= 1
            self.attempts -= 1
        
        self.patches = self.patches[:idx]

            

