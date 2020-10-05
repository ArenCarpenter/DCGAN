# Deep Convolutional Generative Adversarial Network (DCGAN)

**Aren Carpenter**

October 2020

## Background on Project

Testing workflow with PyCharm and GitHub Desktop while exploring a new feature of my previous project on detecting leukemia with a CNN. I want to implement a GAN model to create synthetic images of leukemia cells.

## On DCGANs

Deep convolutional generative adversarial networks are a subset of GANs allowing for unsupervised learning for image classification problems by generating artificially generated labeled data. This process allows users to create synthetic data to better train models or to create new realistic samples for cases where getting labeled data is expensive or impossible. This model is basically a traditional CNN that attempts to classify the image. The Generator's loss function is tied to its outputs being accepted by the Discriminator.

GANs are distinguised by two adversarial models trying to convince each other that an image, or datapoint, is real or not. The Generator model works to create artificial images similar enough to real labeled data to pass to the Discriminator model. 

Here is an example GAN architecture:

![](Images/DCGAN%20Architecture.png)
Image courtesy of Paul Lukowicz "Generative Oversampling Method for Imbalanced Data on Bearing Fault Detection and Diagnosis" under CC-BY 4.0 license.