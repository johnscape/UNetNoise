from PIL import Image
from ImageHandler import ImageGenerator, ImageSeperator

'''generator = ImageGenerator("masks", "noise", "gen", 100)
generator.RotationEnabled = False
generator.PlaceBehindEnabled = False

white = Image.new(mode='RGB', size=(100, 100), color=(255, 255, 255))
black = Image.new(mode='RGB', size=(5, 5), color=(1, 1, 1))

white.save("masks/white.png", format="png")
black.save("noise/black.png", format="png")

generator.GenerateImages(10, 30)'''

seperate = ImageSeperator(100, 100)
seperate.Seperate("seperate/road.jpg", "seperate")