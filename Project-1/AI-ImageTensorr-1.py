
# first go to your command prompt and select the desired environment

# then run the command: 
# pip install torch torchvision matplotlib numpy

import os
import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

batch_size = 10
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

# Check if CIFAR-10 is already downloaded
data_dir = './data/cifar-10-batches-py'
download = not os.path.exists(data_dir)

print("Downloading training data..." if download else "Training data already downloaded.")
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=download, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=1)


print("Downloading testing data..." if download else "Testing data already downloaded.")
testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=download, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=1)

classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


print(__name__)
if __name__ == '__main__':
    print("Running as main program")

    dataiter = iter(trainloader)
    images, labels = next(dataiter)

    for i in range(batch_size):
        plt.subplot(2,int(batch_size/2), i + 1)
        img = images[i]
        img = img / 2 + 0.5
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.axis('off')
        plt.title(classes[labels[i]])

    plt.suptitle('Preview of Training Data', size=20)
    plt.show()
    
    
    # # Step 2: Configure the neural network
    
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Define a convolutional neural network
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
net = Net()

# Define a loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

print("Your network is ready for training!")


# # Step 3: Train the network and save model

from tqdm import tqdm
print("# # Step 3:  Train the network and save model")
print(__name__)
if __name__ == '__main__':
    EPOCHS = 2
    print("Training...")
    for epoch in range(EPOCHS):
        running_loss = 0.0
        for i, data in enumerate(tqdm(trainloader, desc=f"Epoch {epoch + 1} of {EPOCHS}", leave=True, ncols=80)):
            inputs, labels = data

            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

    # Save our trained model
    PATH = './cifar_net.pth'
    torch.save(net.state_dict(), PATH)
    print("# # Step 3:  Train the network and save model-- DONE")
