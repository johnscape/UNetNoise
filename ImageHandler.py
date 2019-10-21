import PIL
from PIL import Image
import os.path
from os.path import isfile, join
import os, shutil
from os import listdir
import random
import numpy as np

class ImageGenerator:
    def __init__(self, mask_path, noise_path, generated_path, image_size = 512):
        self.__MasksPath = mask_path
        self.__NoisePath = noise_path
        self.__GeneratedPath = generated_path
        self.__ImageSize = image_size

        self.RotationEnabled = True
        self.PlaceBehindEnabled = True
        self.DeleteWithoutAsking = False
        self.SkipImageCheck = True

    def GenerateImages(self, num = 5000, max_noise_count = 10, auto_save = True):
        #check folders
        if os.path.exists(self.__GeneratedPath + "/generated") or os.path.exists(self.__GeneratedPath + "/original"):
            if not self.DeleteWithoutAsking:
                print("The target folders are already exists. Do you want to delete them? Y/n")
                answer = input()
                if answer == "Y":
                    self.DeleteFiles(self.__GeneratedPath + "/generated")
                    self.DeleteFiles(self.__GeneratedPath + "/original")
                else:
                    return
            else:
                self.DeleteFiles(self.__GeneratedPath + "/generated")
                self.DeleteFiles(self.__GeneratedPath + "/original")
        else:
            os.mkdir(self.__GeneratedPath + "/generated")
            os.mkdir(self.__GeneratedPath + "/original")
        #get list of mask images
        masks = [f for f in listdir(self.__MasksPath) if isfile(join(self.__MasksPath, f))]
        noises = [f for f in listdir(self.__NoisePath) if isfile(join(self.__NoisePath, f))]

        #check images for size
        maskOk = self.CheckFiles(masks, self.__ImageSize, self.SkipImageCheck)
        if not maskOk:
            print("Error while checking images. Do you want to continue? Y/n")
            answer = input()
            if answer != "Y":
                return
        #generate images
        final_images = []
        original_images = []
        for _ in range(num):
            selected_image = Image.open(self.__MasksPath + "/" + random.choice(masks))
            noise_count = random.randint(1, max_noise_count)
            base_array = np.array(selected_image)
            original_images.append(selected_image)
            for _ in range(noise_count):
                selected_noise = Image.open(self.__NoisePath + "/" + random.choice(noises))
                if self.RotationEnabled:
                    selected_image = selected_image.rotate(random.randint(0, 359))
                    selected_noise = selected_noise.rotate(random.randint(0, 359))
                placeBehind = bool(random.getrandbits(1)) if self.PlaceBehindEnabled else False
                startX = random.randint(0, self.__ImageSize)
                startY = random.randint(0, self.__ImageSize)

                noise_array = np.array(selected_noise)

                for x in range(noise_array.shape[1]):
                    for y in range(noise_array.shape[0]):
                        if startX + x < base_array.shape[1] and startY + y < base_array.shape[0]:
                            if placeBehind: #if we cannot overwrite non-black pixels, check if it is a good pixel
                                #check if pixel is black
                                isBlack = True
                                for rgb in range(3):
                                    if base_array[startX + x][startY + y][rgb] != 0:
                                        isBlack = False
                                        break
                                if not isBlack:
                                    continue

                            #if noise pixel is black, we can skip
                            isBlack = True
                            for rgb in range(3):
                                if noise_array[x][y][rgb] != 0:
                                    isBlack = False
                                    break
                                    
                            if isBlack:
                                continue

                            #if black or we can overwrite, start the procedure
                            for rgb in range(3):
                                base_array[startX + x][startY + y][rgb] = noise_array[x][y][rgb]
                
            final_img = Image.fromarray(base_array.astype('uint8'), 'RGB')
            final_images.append(final_img)

        for img in range(len(final_images)):
            file_name = str((img + 1)).zfill(3)
            final_images[img].save(self.__GeneratedPath + "/generated/" + file_name + ".png", format="png")
            original_images[img].save(self.__GeneratedPath + "/original/" + file_name + ".png", format="png")
        return final_images

    def DeleteFiles(self, path):
        for the_file in os.listdir(path):
            file_path = os.path.join(path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    def CheckFiles(self, files, desired_size, skip = False):
        if skip:
            return True
        
        allGood = True
        for image in files:
            im = Image.open(image)
            width, height = im.size
            if width > desired_size or height > desired_size:
                print("Image " + image + " is larger than desired: " + width + ", " + height)
                allGood = False
        return allGood


class ImageSeperator:

    def __init__(self, target_size = 512, step_size = 10):
        self.__TargetSize = target_size
        self.__StepSize = step_size

    def Seperate(self, imagePath, savePath):
        if savePath[-1] != '/':
            savePath += '/'
        original = Image.open(imagePath)
        current_X = 0
        current_Y = 0
        counter = 1
        while True:
            if current_X + self.__TargetSize < original.size[0] and current_Y + self.__TargetSize < original.size[1]:
                part = original.crop((current_X, current_Y, current_X + self.__TargetSize, current_Y + self.__TargetSize))
                part.save(savePath + str(counter).zfill(4) + ".png", format="png")
            else:
                newimg = Image.new(mode='RGB', size=(self.__TargetSize, self.__TargetSize))
                part = None
                if current_X + self.__TargetSize >= original.size[0] and not (current_Y + self.__TargetSize >= original.size[1]):
                    part = original.crop((current_X, current_Y, original.size[0], current_Y + self.__TargetSize))
                elif not (current_X + self.__TargetSize >= original.size[0]) and current_Y + self.__TargetSize >= original.size[1]:
                    part = original.crop((current_X, current_Y, current_X + self.__TargetSize, original.size[1]))
                else:
                    part = original.crop((current_X, current_Y, original.size[0], original.size[1]))
                newimg.paste(part, (0, 0, part.size[0], part.size[1]))
                newimg.save(savePath + str(counter).zfill(4) + ".png", format="png")
            current_X += self.__StepSize
            if current_X >= original.size[0]:
                current_Y += self.__StepSize
                current_X = 0
                if current_Y >= original.size[1]:
                    break
            counter += 1
        print("Finished")