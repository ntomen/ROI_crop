# Preamble
from __future__ import division, print_function
import argparse

import time
import os
import cv2
from PIL import Image
import numpy as np
#--------------------------------------------------------------------
# Parse input arguments
parser=argparse.ArgumentParser(description='Crop out ROIs annotated by '+\
                                 'red contours in QuPath')
parser.add_argument('--bg_opacity',type=bool,default=True,choices=[True,False],\
                    help='Set background opacity. When False, set background '+\
                    'alpha to 0. Default: True. Note: When set to False, '+\
                    'will save a tif file in RGBA format, instead of RGB.')
parser.add_argument('--contours_in_contours',type=bool,default=False,\
                    choices=[True,False],help='Choose the operation to be '+\
                    'performed. When False, will crop out ROIs disregarding '+\
                    'any other annotations/red contours inside of the ROIs.'+\
                    'When True, will scan for concentric contours and will '+\
                    'exclude annotated regions within the ROI. Default: False.')
parser.add_argument('--save_dir',type=str,default='cropped_images',
                    help='Name of the subdirectory which will be created '+\
                    'at the script location, where the cropped images will '+\
                    'be saved. Default: \'cropped_images\'.')
# currently working:
# bg opacity
# contours in contours
# save directory

# potential options:
# bg color: white/black/rgb
# keep inner contour or not (doesn't make sense when we already have the
#             contours_in_contours option)

args=parser.parse_args()
#--------------------------------------------------------------------
# Fetch tif files in directory
file_names=[]
for file in os.listdir():
    if file.endswith('.tif') or file.endswith('.tiff'):
        file_names.append(file)
#--------------------------------------------------------------------
# Create save directory
if not os.path.exists(args.save_dir):
    os.makedirs(args.save_dir)
#--------------------------------------------------------------------
# Load the image
im=Image.open(file_names[0])
imarray=np.array(im)
#--------------------------------------------------------------------
# Extract the red contour lines
# Encoding RGB, dim 0 = R
is_red=imarray[:,:,0]>245
is_not_green=imarray[:,:,1]<10
is_not_blue=imarray[:,:,2]<10
is_contour=np.logical_and(np.logical_and(is_red,is_not_green),is_not_blue)

mask_contour=np.zeros_like(imarray[:,:,0])
mask_contour[is_contour]=1
del is_contour
#--------------------------------------------------------------------
if args.contours_in_contours:
    colorThreshold = 5

    def pad_with(vector, pad_width, iaxis, kwargs):
        pad_value = kwargs.get('padder', 0)
        vector[:pad_width[0]] = pad_value
        vector[-pad_width[1]:] = pad_value
        return vector

    def justPad(img, backGroundColour):
        padImg = np.pad(img,1,pad_with,padder=backGroundColour)
        height, width = padImg.shape[:2]
        return padImg, height, width

    def cropAndReverse(img, height, width, backGroundColor, labelColor, fillColor, maskColor):
        croppedImg = np.delete((np.delete(img, [0, width-1], axis=1)), [0, height-1], axis=0)
        # label is the color that is temporarily used to fill exterior
        croppedImg[croppedImg==labelColor]=backGroundColor
        croppedImg[croppedImg==fillColor]=maskColor
        return croppedImg

    def cvFloodFill(img, height, width, seedPosition, fillColor):
        mask = np.zeros([height+2, width +2], np.uint8)
        cv2.floodFill(img, mask, seedPosition, newVal = fillColor, loDiff = 50, upDiff = 50, flags = 4)

    def holesInHoles(imgPath, backGroundColor, boundaryColor, labelColor, fillColor, maskColor):
        padImg, height, width = justPad(imgPath, backGroundColor)
        print('Done with padding.')
        seedPosition = (0, 0)
        cvFloodFill(padImg, height, width, seedPosition, labelColor)
        print('Done with first fill. Entering loop.')
        for x in range(height):
            if not np.any(padImg==backGroundColor):
                break
            y=np.argmax(padImg[x,:]<colorThreshold) # only works because BGclr=0
            if y>0:
                seedPosition=(y,x)
                i=np.argmax(np.abs(np.flip(padImg[x,:y])-boundaryColor)>=colorThreshold)
                if abs(padImg[x,y-i-1] - labelColor) < colorThreshold:
                    cvFloodFill(padImg, height, width, seedPosition, fillColor)
                else:
                    cvFloodFill(padImg, height, width, seedPosition, labelColor)

        resultImg=cropAndReverse(padImg, height, width, backGroundColor, labelColor, fillColor, maskColor)
        return resultImg
#--------------------------------------------------------------------
if args.contours_in_contours:
    boundaryColor=255
    fillColor=128
    labelColor=80
    backGroundColor=0 # has to be 0, don't change
    maskColor=255

    start=time.clock()
    mask_filled=holesInHoles(mask_contour*boundaryColor,backGroundColor,\
                             boundaryColor,labelColor,fillColor,maskColor)
    elapsed=(time.clock()-start)
    print(elapsed)
else:
    _,_,mask_filled,_=cv2.floodFill(mask_contour,np.zeros((\
                      mask_contour.shape[0]+2,mask_contour.shape[1]+2),\
                      np.uint8),(0,0),None)
    mask_filled=(-mask_filled[1:-1,1:-1]+1)*255
#--------------------------------------------------------------------
# Find connected components
n_components,comp_filled,component_stats,_=cv2.connectedComponentsWithStats(\
                                     mask_filled,connectivity=8)
#--------------------------------------------------------------------
# Set contour pixels to background color
smooth_mask_contour=cv2.blur(mask_contour.astype(np.float),(3,3))
smooth_mask_contour[smooth_mask_contour>0]=1
smooth_mask_contour=smooth_mask_contour.astype(np.bool)
if args.bg_opacity:
    for j in range(imarray.shape[-1]):
        imarray[smooth_mask_contour,j]=255
#--------------------------------------------------------------------
# Set background to white/transparent and save
for i in range(1,n_components):
    if args.bg_opacity:
        # Setting color ch's
        hc_filled=comp_filled.copy().astype(np.uint8)
        hc_filled[hc_filled!=i]=0
        
        src_mask=np.zeros((hc_filled.shape[0],hc_filled.shape[1],3))
        for j in range(src_mask.shape[-1]):
            src_mask[:,:,j]=hc_filled # mask to 3 ch image
        
        imarray_extract=imarray.copy()
        imarray_extract[src_mask==0]=255
    else:
        # Setting alpha
        # Create image with alpha channel
        imarray_extract=cv2.cvtColor(imarray,cv2.COLOR_RGB2RGBA)
        
        hc_filled=comp_filled.copy().astype(np.uint8)
        hc_filled[hc_filled!=i]=0
        hc_filled[hc_filled==i]=1
        
        imarray_extract[:,:,3]=hc_filled
        imarray_extract[:,:,3]*=(-smooth_mask_contour.astype(np.uint8)+1)
        imarray_extract[:,:,3]*=255
    # Crop
    b=5 # white border pixel width
    crop_save=imarray_extract[component_stats[i,1]-b:component_stats[i,1]+\
                      component_stats[i,3]+b,\
                      component_stats[i,0]-b:component_stats[i,0]+\
                      component_stats[i,2]+b,:]

    if args.bg_opacity:
        crop_save=Image.fromarray(crop_save,'RGB')
    else:
        crop_save=Image.fromarray(crop_save,'RGBA')
        
    save_fname=file_names[0][:-4]+'_'+str(i)+'.tif'
    save_path=os.path.join(os.getcwd(),args.save_dir,save_fname)
    
    crop_save.save(save_path)
#--------------------------------------------------------------------
#plt.imshow(imarray_extract[500:1500,1750:2800,:])
#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------