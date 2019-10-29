# *************************** BioSPA Settings ***************************

''' Root Folder setup '''
#--------------------------------
#Insert the name (between quotation marks) of the folder which contains the set of image stacks
# INPUT TYPE = text string
FolderName = 'example_Smutans_time_lapse'


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
TOPOFolderName = 'example_Surface_Profile'

#Insert the number of images in the stack with topographical information
# INPUT TYPE = integer number
TOPOSliceNumber = 89

#Insert the (between quotation marks) image format
# INPUT TYPE = text string
TOPOimageFormat = 'png'

#Insert the Z-step of the stack with the topography profile (in microns)
# INPUT TYPE = float number
TOPOZstep = 0.41






''' defining the settings configuration (do not change information bellow) '''
#--------------------------------

def Settings():

    SettingsDic = {}
    
    SettingsDic['FolderName'] = '/' + FolderName
    SettingsDic['tp_ref_to_crop'] = '/' + FolderName + '/t' + str(timePoints)
    SettingsDic['timePoints'] = timePoints
    SettingsDic['ImageBaseName'] = ImageBaseName
    SettingsDic['SliceNumber'] = SliceNumber
    SettingsDic['timeinterval'] = timeinterval
    SettingsDic['Zstep'] = Zstep
    SettingsDic['Microorganism_Radius'] = Microorganism_Radius
    SettingsDic['imageFormat'] = '.' + imageFormat
    SettingsDic['width'] = width -1
    SettingsDic['width_field'] = width_field
    SettingsDic['height'] = height - 1
    SettingsDic['height_field'] = height_field
    SettingsDic['TopoMODE_input'] = TopoMODE_input
    SettingsDic['TOPOFolderName'] = '/' + TOPOFolderName
    SettingsDic['TOPOSliceNumber'] = TOPOSliceNumber
    SettingsDic['TOPOimageFormat'] = '.' + TOPOimageFormat    
    SettingsDic['TOPOZstep'] = TOPOZstep
    
    return SettingsDic
