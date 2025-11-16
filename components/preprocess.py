from kfp.dsl import component, Output, Dataset

import torch
import torchvision
import torch.utils.data as data
import torchvision.datasets as datasets
import torchvision.transforms as transforms

@component
def preprocess(train_loader: Output[Dataset], test_loader: Output[Dataset]):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    # Load the CIFAR10 dataset temporarily until the AWS S3 data lake has been set up
    train_set = datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
    train_loader = data.DataLoader(train_set, batch_size=4, shuffle=True, num_workers=2)
    test_set = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=4, shuffle=False, num_workers=2)

    # Save datasets to KFP output paths
    torch.save(train_loader, train_loader.path)
    torch.save(test_loader, test_loader.path)
