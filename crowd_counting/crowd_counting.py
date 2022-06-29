# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 01:08:45 2022

@author: Admin
"""
from torchvision import datasets, transforms
from crowd_counting.inceptionresnetv2 import InceptionResNetV2
from crowd_counting.vgg16_inception import CSRNet
import torch

# model = InceptionResNetV2().cpu()
model = CSRNet().cpu()
# checkpoint = torch.load("C:\\Users\\Admin\\Desktop\\TA\\Dataset\\0model_best.pth.tar")
checkpoint = torch.load("C:\\Users\\Admin\\Desktop\\TA\\Model\\model_best.pth.tar", map_location=torch.device('cpu'))
model.load_state_dict(checkpoint['state_dict'])
transform=transforms.Compose([
                      transforms.ToTensor(),transforms.Normalize(
                          mean=[0.485, 0.456, 0.406],
                          std=[0.229, 0.224, 0.225]),
                  ])