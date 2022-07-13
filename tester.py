# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:39:40 2022
@author: Admin
"""

# ====================================================================
# prediction on single image
# ====================================================================
import h5py
import PIL.Image as Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm as c
import torch
from torchvision import transforms
from model.inceptionresnetv2 import InceptionResNetV2

model = InceptionResNetV2()
model = model.cpu()
#loading the trained weights
checkpoint = torch.load("G:\\Dataset\\Result\\0model_best.pth.tar")
model.load_state_dict(checkpoint['state_dict'])
transform=transforms.Compose([
                      transforms.ToTensor(),transforms.Normalize(
                          mean=[0.485, 0.456, 0.406],
                          std=[0.229, 0.224, 0.225]),
                  ])

fileName = "IMG_1"
img = transform(Image.open('G:\\Dataset\\ShanghaiTech\\part_B\\test_data\\images\\'+fileName+'.jpg').convert('RGB')).cpu()
gt_file = h5py.File("G:\\Dataset\\ShanghaiTech\\part_B\\test_data\\ground-truth\\"+fileName+".h5",'r')
groundtruth = np.asarray(gt_file['density'])

output = model(img.unsqueeze(0))
prediction = output.detach().cpu()
print("Original Count : ", int(np.sum(groundtruth)))
print("Predicted Count : ",int(prediction.sum().numpy()))
pred_count = np.asarray(prediction.reshape(prediction.shape[2],prediction.shape[3]))
fig = plt.figure()
fig_ground = fig.add_subplot(121)  # left side
fig_estimate = fig.add_subplot(122) # right side
fig_ground.imshow(groundtruth, cmap = c.jet)
fig_estimate.imshow(pred_count, cmap = c.jet)
plt.show()