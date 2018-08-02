# sample pytorch recipie
intelligent service sample which can be onboarded on ML Framework.

## Commands to build:

```
git clone [[GITHUB BASE URL]]:ml/samples-tensorflow.git

cd samples-tensorflow/samples/pytorch/cifar10

docker login --username sdkutil --password <> [[DOCKER ML RUNTIME BASE URL]]
docker build -t [[DOCKER ML RUNTIME BASE URL]]/tf-sample:<version> .
Docker push [[DOCKER ML RUNTIME BASE URL]]/tf-sample:<version>
```
We use a package called
``torchvision``, that has data loaders for common datasets such as
Imagenet, CIFAR10, MNIST, etc. and data transformers for images, viz.,
``torchvision.datasets`` and ``torch.utils.data.DataLoader``.

This provides a huge convenience and avoids writing boilerplate code.

In this model, we will use the CIFAR10 dataset.
It has the classes: ‘airplane’, ‘automobile’, ‘bird’, ‘cat’, ‘deer’,
‘dog’, ‘frog’, ‘horse’, ‘ship’, ‘truck’. The images in CIFAR-10 are of
size 3x32x32, i.e. 3-channel color images of 32x32 pixels in size.

.. figure:: /_static/img/cifar10.png
   :alt: cifar10

   cifar10


Training an image classifier
----------------------------

We will do the following steps in order:

1. Load and normalizing the CIFAR10 training and test datasets using
   ``torchvision``
2. Define a Convolution Neural Network
3. Define a loss function
4. Train the network on the training data and dump the weights (training.py)
5. Load the trained weights and Test the network on the test data (scorer.py)
