from kfp.dsl import component, Input, Dataset, Model

from torch.utils.data import DataLoader

from .train import CNN

from typing import Tuple

import torch

@component
def test(test_loader: Input[Dataset], model_state: Input[Model]):
    test_loader: DataLoader  = torch.load(test_loader.path)

    cnn = CNN()
    cnn.load_state_dict(torch.load(model_state.path, weights_only=True))

    total = 0
    correct = 0

    with torch.no_grad():
        for data in test_loader:
            images: torch.Tensor
            labels: torch.Tensor
            images, labels = data

            outputs: torch.Tensor
            outputs = cnn(images)

            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    # Output the ratio of correct predictions to total predictions giving the accurracy
    print(f'Accuracy of the network on the 10000 test images: {100 * correct // total} %')
