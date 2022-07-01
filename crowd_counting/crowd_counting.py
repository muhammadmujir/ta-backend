# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 01:08:45 2022

@author: Admin
"""
from torchvision import datasets, transforms
from crowd_counting.inceptionresnetv2 import InceptionResNetV2
import torch

model = InceptionResNetV2().cpu()
checkpoint = torch.load("F:\\TA\\Dataset\\Result\\0model_best.pth.tar")
model.load_state_dict(checkpoint['state_dict'])
transform=transforms.Compose([
                      transforms.ToTensor(),transforms.Normalize(
                          mean=[0.485, 0.456, 0.406],
                          std=[0.229, 0.224, 0.225]),
                  ])