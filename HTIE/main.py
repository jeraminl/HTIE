import subprocess
import os
from pathlib import Path
from threading import Thread
from threading import Semaphore

cmdPath = Path("./command_set")
maxthread = 12
sema = Semaphore(value = maxthread)


def crop(x, y, offsetX, offsetY, inputPath, outputPath, filename):
    fullInputPath = os.path.join(inputPath, filename)
    fullOutputPath = os.path.join(outputPath, filename)
    command = ["convert", str(fullInputPath), "-crop", str(x)+'x'+str(y)+'+'+str(offsetX)+'+'+str(offsetY), str(fullOutputPath)]
    subprocess.check_output(command)

def rotate(degree, inputPath, outputPath, filename):
    fullInputPath = os.path.join(inputPath, filename)
    fullOutputPath = os.path.join(outputPath, filename)
    command = ["convert", str(fullInputPath), "-rotate", str(degree), str(fullOutputPath)]
    subprocess.check_output(command)

def flip(inputPath, outputPath, filename):
    fullInputPath = os.path.join(inputPath, filename)
    fullOutputPath = os.path.join(outputPath, filename)
    command = ["convert", str(fullInputPath), "-flip", str(fullOutputPath)]
    subprocess.check_output(command)


def setupTempFolders(numCmd,setNum):
    for i in range(1,numCmd):
        subprocess.check_output(['mkdir','temp'+str(setNum)+'-'+str(i)])

def parseCommands(setNum, cmdPath):
    inputPath = Path("./input")
    outputPath = Path("./temp"+str(setNum)+"-1")

    file = open('./command_set/commands'+str(setNum), 'r')
    cmds = file.readlines()
    setupTempFolders(len(cmds), setNum)
    cmdNum = 1
    for cmd in cmds:
        if cmdNum > 1:
            inputPath = Path('./temp'+str(setNum)+'-'+str(cmdNum-1))
            outputPath = Path('./temp'+str(setNum)+'-'+str(cmdNum))
            if cmdNum == len(cmds):
                outputPath = Path('./output/'+str(setNum))

        threads = list()
        for filename in os.listdir(inputPath):
            thread = Thread(target = chooseCommands, args = (cmd,inputPath,outputPath,filename))
            threads.append(thread)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        cmdNum += 1
    print('all operations completed')
    subprocess.check_output(['rm','-rf','temp'+str(setNum)+'*'])



def chooseCommands(cmd, inputPath, outputPath, filename):
    sema.acquire()
    if cmd.split()[0] == 'crop':
        crop(cmd.split()[1], cmd.split()[2], cmd.split()[3], cmd.split()[4], inputPath, outputPath, filename)
    elif cmd.split()[0] == 'rotate':
        rotate(cmd.split()[1],inputPath,outputPath, filename)
    elif cmd.split()[0] == 'rotate':
        flip(cmd.split()[1],inputPath,outputPath,filename)
    sema.release()

def start():
    setNum = 1
    for filename in os.listdir(cmdPath):
        thread = Thread(target=parseCommands, args = (setNum, cmdPath))
        thread.start()
        setNum+=1
    subprocess.check_output(['rm','-rf','temp*'])




if __name__=="__main__":
    #setupTempFolders(7)
    try:
        start()
        subprocess.check_output(['rm','-rf','temp*'])

    except:
        subprocess.check_output(['rm','-rf','temp*'])
