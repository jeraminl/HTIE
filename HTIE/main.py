import subprocess
import os
from pathlib import Path

inputPath = Path("../input")
outputPath = Path("../output")
'''
    path = path to the folder containing the files
    x = width
    y = height

'''


def crop(x, y, offsetX=0, offsetY=0):
   for filename in os.listdir(inputPath):
       if filename.endswith(".jpg"):
           fullInputPath = os.path.join(inputPath, filename)
           fullOutputPath = os.path.join(outputPath, filename)
           command = ["convert", str(fullInputPath), "-crop", str(x)+'x'+str(y)+'+'+str(offsetX)+'+'+str(offsetY), str(fullOutputPath)]
           subprocess.check_output(command)

def rotate(degree):
   for filename in os.listdir(inputPath):
       if filename.endswith(".jpg"):
           fullInputPath = os.path.join(inputPath, filename)
           fullOutputPath = os.path.join(outputPath, filename)
           command = ["convert", str(fullInputPath), "-rotate", str(degree), str(fullOutputPath)]
           subprocess.check_output(command)




if __name__=="__main__":
    rotate(45)
