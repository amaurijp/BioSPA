Copyright (c) 2019 Amauri Jardim de Paula, Hyun Koo, Geelsu Hwang
#------------------------------------------#

* Software Version *

BioSPA v0.1

#------------------------------------------#

* Software Description *

BioSPA (Biofilm Spatiotemporal Population Analysis) software uses a set of images stacks containing (each) three-dimensional (3D) information of the microorganisms presence in a certain volume. Thus, each set of image stacks represents the 3D information of the microorganisms in a certain time point. A set of image stacks represent spacial occupation of microorganisms in time (4D information). A common method to obtain such data is the time-lapse laser-scanning confocal optical microscopy (tl-LCSM). To this data, BioSPA software perform a population analysis of the microorganisms to evaluate their growth dynamics.

The concept of the population analysis applied to microorganisms growth dynamics begins by (i) recognizing independently microorganisms (i.e., the primary elements), the extracellular polymeric substances (EPS), and surface topography (i.e., the terrain). BioSPA identifies all microorganisms attached to a surface (the colonizers) and their surface-attachment sites (topographical profiles). (ii) The biofilm development on the surface, including the EPS production at individual colony level is then analyzed by performing 3D reconstruction of time-resolved LSCM image stacks (time-lapse experiment), thus resulting in 4D data. With time resolved image stacks (4D data), each surface colonizer have its evolution tracked in terms of number, colony size and shape. 

After importing image stacks, BioSPA performs (i) microorganisms labeling (elements labeling), (ii) elements convex hull determination, (iii) determination of the elements volumes, and (iv) fitting of the growth curves (i.e., volumes X time). These sequential processing is performed on each image stack of the 4D data.

#------------------------------------------#

* Software Dependencies *

- python v3.4 (or superior)
- numpy v1.14 (or superior)
- scikit-image v0.14 (or superior)
- scipy v1.1 (or superior)
- matplotlib v3.0 (or superior)
- pillow v5.0 (or superior)

(Python distributions such as Anaconda and Enthought Canopy contain all dependencies)

#------------------------------------------#

* Image processing requirements *

BioSPA uses binarized images (.jpg, .jpeg, .tif, or .tiff formats). When the user will binarize image stacks such as those obtained from LSCM, it is highly recommended to apply a blur filtering (ex: gaussian filter) before binarization. This initial image processing can be performed in open-source softwares such as Image J (and its distribution; ex: FIJI) and GIMP - GNU Image Manipulation Program. If the topographical mode will be used, the user must use a CLSM image stack containing the topographical profile. This image stack must be provided in grayscale (.jpg, .jpeg, .tif, or .tiff formats). The use of a blur filter on the grayscale LCSM image stack containing the topographical information is highly recommended.

#------------------------------------------#

* BioSPA: HOW TO USE *

1. After downloading BioSPA.zip, extract all files to a specific folder containing. File BioSPA.zip contains the folder 'Modules' (with all software routines), and files README.txt, License.txt, main.py and Settings.py.

2. To the same folder in which BioSPA software was extracted, paste the set of image stacks (hyperstack) in binary format. BioSPA uses binarized images only to perform all calculations. 

3. Insert the all setup inputs in the file Settings.py.

4. Inside the folder in which BioSPA.zip was extract, run the file main.py. To do this, in the terminal (MACOS or LINUX) or CMD (Windows) type "python main.py".

#------------------------------------------#

* Settings Description *

In the file Settings.py the user will define the setup for runing BioSPA. Inputs for runing the software includes:

''' Root Folder setup '''
#--------------------------------
#Insert the name (between quotation marks) of the folder which contains the set of image stacks
# INPUT TYPE = text string
FolderName = 'Smutans_time_lapse'


''' Experiment details '''
#--------------------------------
#Insert the number of image stacks to be processed (time points)
# INPUT TYPE = integer number
timePoints = 5

#Insert the number of images in the stacks
# INPUT TYPE = integer number
SliceNumber = 123

#Insert the time interval between measuremnts (in minutes)
# INPUT TYPE = integer number
timeinterval = 30

#Insert the Z-step of the stack (in microns)
# INPUT TYPE = float number
Zstep = 0.3

#Insert the average radius of the microorganism (in microns)
# INPUT TYPE = float number
Microorganism_Radius = 0.44


''' images properties '''
#--------------------------------
#Insert base name of the images. 
#Example: if images are named Slice001.png, Slice002.png, etc, the ImageBaseName is 'Slice'
# INPUT TYPE = text string
ImageBaseName = 'Slice'

#Insert the (between quotation marks) image format
# INPUT TYPE = text string
imageFormat = 'png'

#Insert the image width in number of pixels
# INPUT TYPE = integer number
width = 1024

#Insert the image width in microns
# INPUT TYPE = float number
width_field = 319.5

#Insert the image height in number of pixels
# INPUT TYPE = integer number
height = 1024

#Insert the image height in microns
# INPUT TYPE = float number
height_field = 319.5


''' Topographical mode '''
#--------------------------------
#Do you want to use the topographical mode (TOPO mode)?
# INPUT TYPE = text string ('YES' or 'NO')
TopoMODE_input = 'YES'

#If 'yes', insert the name (between quotation marks) of the folder which contains the image stack with the surface profile information
# INPUT TYPE = text string
TOPOFolderName = 'Surface_Profile'

#Insert the number of images in the stack with topographical information
# INPUT TYPE = integer number
TOPOSliceNumber = 89

#Insert the (between quotation marks) image format
# INPUT TYPE = text string
TOPOimageFormat = 'png'

#Insert the Z-step of the stack with the topography profile (in microns)
# INPUT TYPE = float number
TOPOZstep = 0.41
