#
# Copyright 2017 Adobe.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from ml.runtime.tensorflow.Interfaces.AbstractScorer import AbstractScorer
import tensorflow as tf
import numpy

import torch
import torchvision
import torchvision.transforms as transforms

import torch.nn as nn
import torch.nn.functional as F


class Scorer(AbstractScorer):

    def score(self, config={}):
        """loads trained weights and scores on test cofar-10 data

        load trained model using the weights,
        load the test dataset,
        score and compute accuracy

        :param config: passed on by ml-framework
        :return: None
        """
        print("Executed scorer 2")
        print(config["modelPATH"])
        print(config["logsPATH"])

        class Net(nn.Module):
            def __init__(self):
                super(Net, self).__init__()
                self.conv1 = nn.Conv2d(3, 6, 5)
                self.pool = nn.MaxPool2d(2, 2)
                self.conv2 = nn.Conv2d(6, 16, 5)
                self.fc1 = nn.Linear(16 * 5 * 5, 120)
                self.fc2 = nn.Linear(120, 84)
                self.fc3 = nn.Linear(84, 10)

            def forward(self, x):
                x = self.pool(F.relu(self.conv1(x)))
                x = self.pool(F.relu(self.conv2(x)))
                x = x.view(-1, 16 * 5 * 5)
                x = F.relu(self.fc1(x))
                x = F.relu(self.fc2(x))
                x = self.fc3(x)
                return x

        transform = transforms.Compose(
            [transforms.ToTensor(),
             transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

        testset = torchvision.datasets.CIFAR10(root='./data',
                                               train=False,
                                               download=True,
                                               transform=transform)
        testloader = torch.utils.data.DataLoader(testset,
                                                 batch_size=4,
                                                 shuffle=False,
                                                 num_workers=2)

        net = Net()
        state_dict = torch.load(config["modelPATH"] +
                                "/my_cifar_pytorch_model.dict")
        net.load_state_dict(state_dict)

        correct = 0
        total = 0
        with torch.no_grad():
            for data in testloader:
                images, labels = data
                outputs = net(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        print('Accuracy of the network on the 10000 test images: %d %%' % (
                100 * correct / total))
