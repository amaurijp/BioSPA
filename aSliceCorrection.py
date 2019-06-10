import skimage
from skimage import io
import numpy as np
import os
 
diretorio = os.getcwd()


def SliceCorrectionFunc(ImportstackRootName,
                        ExportPath,
                        stackNumber,
                        importFormat='.png'):

    Imglist=[]    
    
    if stackNumber <= 7:
        SliceRange1=list(range(1,54+1))
        for x in SliceRange1:
            if x < 10:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice00' + str(x) + importFormat)
                
            elif 10 <= x < 100:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice0' + str(x) + importFormat)

            elif 100 <= x < 1000:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice' + str(x) + importFormat)            
            
            width, height = a.shape
            
            Imglist.append(a)
            
        BlackImgs=[]
        for y in list(range(104-54)):
            BlackImgs.append(skimage.img_as_ubyte(np.zeros([height,width])))

        FinalImgStack=[]
        FinalImgStack.extend(BlackImgs)
        FinalImgStack.extend(Imglist)
        
        #print(len(Imglist))
        #print(len(BlackImgs))
        #print(len(FinalImgStack))
        
        if not os.path.exists(diretorio + ExportPath + '/t' + str(stackNumber)):
            os.makedirs(diretorio + ExportPath + '/t' + str(stackNumber))

        for SliceNumber in list(range(len(FinalImgStack))):
            if SliceNumber < 10-1:
                io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice00' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])
            
            elif 10-1 <= SliceNumber < 100-1:
                io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice0' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])

            elif 100-1 <= SliceNumber < 1000-1:
                io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])



    elif 8 <= stackNumber <= 11:
        SliceRange1=list(range(1,67+1))
        for x in SliceRange1:
            if x < 10:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice00' + str(x) + importFormat)
                
            elif 10 <= x < 100:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice0' + str(x) + importFormat)

            elif 100 <= x < 1000:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice' + str(x) + importFormat)            
            
            width, height = a.shape                
            
            Imglist.append(a)
                
            BlackImgs=[]
            for y in list(range(104-67)):
                BlackImgs.append(skimage.img_as_ubyte(np.zeros([height,width])))
    
            FinalImgStack=[]
            FinalImgStack.extend(BlackImgs)
            FinalImgStack.extend(Imglist)
            
            #print(len(Imglist))
            #print(len(BlackImgs))
            #print(len(FinalImgStack))
            
            if not os.path.exists(diretorio + ExportPath + '/t' + str(stackNumber)):
                os.makedirs(diretorio + ExportPath + '/t' + str(stackNumber))
    
            for SliceNumber in list(range(len(FinalImgStack))):
                if SliceNumber < 10-1:
                    io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice00' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])
            
                elif 10-1 <= SliceNumber < 100-1:
                    io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice0' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])
    
                elif 100-1 <= SliceNumber < 1000-1:
                    io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])


    elif 12 <= stackNumber <= 15:
        SliceRange1=list(range(1,91+1))
        for x in SliceRange1:
            if x < 10:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice00' + str(x) + importFormat)
                
            elif 10 <= x < 100:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice0' + str(x) + importFormat)

            elif 100 <= x < 1000:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice' + str(x) + importFormat)            
            
            width, height = a.shape                
            
            Imglist.append(a)
                
            BlackImgs=[]
            for y in list(range(104-91)):
                BlackImgs.append(skimage.img_as_ubyte(np.zeros([height,width])))
    
            FinalImgStack=[]
            FinalImgStack.extend(BlackImgs)
            FinalImgStack.extend(Imglist)
            
            #print(len(Imglist))
            #print(len(BlackImgs))
            #print(len(FinalImgStack))
            
            if not os.path.exists(diretorio + ExportPath + '/t' + str(stackNumber)):
                os.makedirs(diretorio + ExportPath + '/t' + str(stackNumber))
    
            for SliceNumber in list(range(len(FinalImgStack))):
                if SliceNumber < 10-1:
                    io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice00' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])
            
                elif 10-1 <= SliceNumber < 100-1:
                    io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice0' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])
    
                elif 100-1 <= SliceNumber < 1000-1:
                    io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])



    elif 16 <= stackNumber <= 25:
        SliceRange1=list(range(1,104+1))
        for x in SliceRange1:
            if x < 10:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice00' + str(x) + importFormat)
                
            elif 10 <= x < 100:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice0' + str(x) + importFormat)

            elif 100 <= x < 1000:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice' + str(x) + importFormat)            
            
            width, height = a.shape                
            
            Imglist.append(a)
                
            BlackImgs=[]
            for y in list(range(104-104)):
                BlackImgs.append(skimage.img_as_ubyte(np.zeros([height,width])))
    
            FinalImgStack=[]
            FinalImgStack.extend(BlackImgs)
            FinalImgStack.extend(Imglist)
            
            #print(len(Imglist))
            #print(len(BlackImgs))
            #print(len(FinalImgStack))
            
            if not os.path.exists(diretorio + ExportPath + '/t' + str(stackNumber)):
                os.makedirs(diretorio + ExportPath + '/t' + str(stackNumber))
    
            for SliceNumber in list(range(len(FinalImgStack))):
                if SliceNumber < 10-1:
                    io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice00' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])
            
                elif 10-1 <= SliceNumber < 100-1:
                    io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice0' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])
    
                elif 100-1 <= SliceNumber < 1000-1:
                    io.imsave(diretorio + ExportPath + '/t' + str(stackNumber) + '/Slice' + str(SliceNumber+1) + '.png', FinalImgStack[SliceNumber])


# Run Slice correction

stacklist=list(range(1,25+1))

for stack in stacklist:
    SliceCorrectionFunc('/Binarized/bac/ImageJ',
                        '/BinarizedCorr/bac',
                        stack) 

for stack in stacklist:
    SliceCorrectionFunc('/Binarized/EPS_THR10/ImageJ',
                        '/BinarizedCorr/EPS',
                        stack)            