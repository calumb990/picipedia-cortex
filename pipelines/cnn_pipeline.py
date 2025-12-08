import kfp.dsl as dsl

@dsl.component(base_image="calumb990/kcomp:0.0.0")
def preprocess(train_loader_output: dsl.Output[dsl.Dataset], test_loader_output: dsl.Output[dsl.Dataset]):

    import torch
    import torchvision
    import torch.utils.data as data
    import torchvision.datasets as datasets
    import torchvision.transforms as transforms

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
    torch.save(train_loader, train_loader_output.path)
    torch.save(test_loader, test_loader_output.path)

@dsl.component(base_image="calumb990/kcomp:0.0.0")
def train(train_loader_input: dsl.Input[dsl.Dataset], model_state_output: dsl.Output[dsl.Model]):
    
    import torch
    import torch.nn as nn
    import models.cnn as cnn
    import torch.optim as optim
    import torch.utils as utils

    train_loader: utils.data.DataLoader = torch.load(train_loader_input.path)
    
    cnn = cnn.CNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(cnn.parameters(), lr=0.001)

    for epoch in range(10):

        running_loss = 0.0
        for i, data in enumerate(train_loader):
            inputs: torch.Tensor
            labels: torch.Tensor
            inputs, labels = data

            optimizer.zero_grad()
            outputs = cnn(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 2000 == 1999:
                print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
                running_loss = 0.0

    torch.save(cnn.state_dict(), model_state_output.path)

@dsl.component(base_image="calumb990/kcomp:0.0.0")
def test(test_loader_input: dsl.Input[dsl.Dataset], model_state_input: dsl.Input[dsl.Model]):

    import torch
    import models.cnn as cnn
    import torch.utils as utils

    cnn = cnn.CNN()
    test_loader: utils.data.DataLoader = torch.load(test_loader_input.path)
    cnn.load_state_dict(torch.load(model_state_input.path, weights_only=True))

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

@dsl.pipeline
def cnn_pipeline():
    preprocess_task = preprocess()
    train_task = train(train_loader_input=preprocess_task.outputs["train_loader_output"])
    test(test_loader_input=preprocess_task.outputs["test_loader_output"], model_state_input=train_task.outputs["model_state_output"])
