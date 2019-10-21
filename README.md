# U-Net Noise Generator
This project aims to create an "auto-noiser" feature, for automatic mask and input image generation for U-Nets.
## Contents
1. [Introduction](#introduction)
2. [Summary](#summary)
   - [U-Net](#u-net)
   - [Image Handler](#image-handler)
     - [Image Generator](#image-generator)
	   - [Generate Images](#generate-images)
	 - [Image Seperator](#image-seperator)
   - [The File System](#the-file-system)
3. [Test Results](#test-results)

## Introduction
As stated in the top of this file, the goal of this project, to train a U-Net network, with the following constrains:
- The input data has minimal of zero noise
- The input data only contains the required pixels
  - Everything else have to be black
- Have several pictures of "noise"
  - Anything that can be used to reduce the quality of the image

## Summary
Let's take a look on the code. We'll have two main files:
- unet.py
- ImageHandler.py

I'll start with the ImageHandler.

### Image Handler
The Image Handler contains two classes:
- ImageGenerator
- ImageSeperator
Both of them has similar purpose, that I'll talk about in detail in the following sections.

####Image Generator
The Image Generator handles the process of creating the training set, from the clean images/masks and the noise images.
The constructor requires 3 string inputs, and an optional integer.
- `mask_path` requires the path or folder name of the folder with the clean images or masks.
- `noise_path` is similar to the `mask_path`, it contains the path to the folder, containing the noise pictures
- `generated_path` is where the generated pictures will be saved. More about it in the [The File System](#the-file-system) section.
- `image_size` is the optional value for the pictures. Since the U-Net only works on images with the size of NxN, we only need one value for the size.

There are several optional boolean values, which modifies the behaviour of the generator.
- `RotationEnabled`: If this boolean is set to true, the generator will rotate the mask and noise with a random value
- `PlaceBehindEnabled`: If it's true, the noise will be placed "*behind*" the non-black pixels, meaning, it won't be visible
- `DeleteWithoutAsking`: When generating the images, the program rewrites old images. To avoid accidental data loss, the program deletes old images. If this value is set to true, it'll do it without asking for input.
- `SkipImageCheck`: The program checks the masks, if their size is correct. If this value is set to true, it'll skip this step.

#####Generate Images
This function creates the edited images. It requires the number of expected images, the maximum number of noise added to the added noise for a single picture.
If the `auto_save` value is set to false, the program **WILL NOT** save the generated images, only returns them.

TODO: add function describtion

####Image Seperator
TBA