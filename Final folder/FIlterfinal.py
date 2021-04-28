import os.path
import PIL
import PIL.ImageDraw
import PIL.ImageOps
import numpy as np              

#change the working directory to the folder with the code before calling the finale() function
def negatify(original_image):
    #checks if the image has an alpha value. If it does, converts it to regular RGB and then inverts the RGB without affecting the alpha value
    if original_image.mode=='RGBA':
        original_image=original_image.convert('RGB')
        inverted=PIL.ImageOps.invert(original_image)
    
    else:
        #if the image is just RGB, inverts the RGB values of the images
        inverted=PIL.ImageOps.invert(original_image)
        
    #override the original image with the inverted pixel values and pasted it on like a mask'''    
    result = PIL.Image.new('RGBA', original_image.size, (0,0,0,0))
    result.paste(inverted, (0,0))
    #search the directory the code is saved in for the image
    directory = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(directory, 'illuminati.png')
    triangle=PIL.Image.open(filepath)
    #sets the dimensions of the triangle to be a percentage of the original image's dimensions
    triwidth=int(original_image.width*float(0.2))
    triheight=int(original_image.height*float(0.2))
    #resizes the triangles
    smalltri=triangle.resize((int(triwidth),int(triheight)))
    #pastes the small triangle into the corners of the inverted image
    position1=((original_image.width-triwidth,original_image.height-triheight))
    position2=((0,0))
    position3=((original_image.width-triwidth,0))
    position4=((0,original_image.height-triheight))
    result.paste(smalltri,position1,smalltri)
    result.paste(smalltri,position2,smalltri)
    result.paste(smalltri,position3,smalltri)
    result.paste(smalltri,position4,smalltri)

    #searches the directory again for another image and opens it as a PIL image
    directory1 = os.path.dirname(os.path.abspath(__file__))
    filepath1 = os.path.join(directory1, 'creep.png')
    creepy=PIL.Image.open(filepath1)
    #sets the dimension of the background
    creepwidth=int(result.width*float(1.25))
    creepheight=int(result.height*float(1.25))
    #resizes the background image
    bgbig=creepy.resize((creepwidth,creepheight))
    #pastes the inverted image onto the center of the background image, making it seem like a border
    bgposition=((int(0.5*(creepwidth-result.width))),int(0.5*(creepheight-result.height)))
    bgbig.paste(result,bgposition)
    return bgbig
    
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def finale(directory=None):
    """ Saves a modfied version of each image in directory.
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and are of negative colors.
    """
    
    if directory == None:
        #change directory to the 'before' folder
        os.chdir("before")
        directory = os.getcwd()# Use working directory if unspecified
        os.chdir("..")
        
    # Create a new directory 'after' folder in the same parent folder as the before 'folder'
    new_directory = os.path.join(os.getcwd(), 'after')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    #load all the images
    image_list, file_list = get_images(directory)  

    #go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        filename, filetype = os.path.splitext(file_list[n])
        
        # apply the filter function and store as new images
        new_image = negatify(image_list[n])
        #save the altered image, using PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)    