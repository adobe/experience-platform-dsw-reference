# Sample PyTorch Recipe
Intelligent service sample which can be onboarded on the DSW ML Framework.

## Steps:

git clone this repository

Navigate the directory to the one containing `build.sh` file and run

```
sh ./login.sh
sh ./build.sh
```

Please note the `login.sh` script should only need to be run once.


## Information

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
