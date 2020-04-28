# ROI crop
For cropping out annotated ROIs, especially in bioimaging data marked by red annotation lines in QuPath.

Generically, the script found here may be used to crop out parts of any tif image circled by solid red lines (multiple crop-outs in multiple images supported). However, this repository was started to help with cropping out exported ROI annotations in [QuPath, the open source software for bioimage analysis](https://github.com/qupath/qupath). Therefore, the script here is intended to be used to crop out ROIs annotated by red lines in biomedical images saved in .tif/.tiff format.

If you use the contents of this repository, please give credit to this github page and the authors.

## 1. Requirements
- Python installation (tested mainly on python 3, but should work with python 2)
- argparse
- OpenCV
- PIL/Pillow
- NumPy

## 2. How it works
The python script is meant to be placed in a directory with multiple annotated biomedical images in .tif/.tiff format, with red lines encircling regions of interest (ROIs). Running the script will crop out each ROI into its own .tif image against a white/transparent background.

An example of a crop with default options:

Original image                 |         Cropped ROI 1        |         Cropped ROI 2
:-----------------------------:|:----------------------------:|:-----------------------------:
![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image.png) | ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_1.png) | ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_2.png)

Running the script with default options will take an original image , e.g. `original_image.tif`, and crop each of the ROIs into its individual tif file, with white background. By default a subdirectory called `cropped_images` will be created where the cropped images will be saved with the name of the original image file followed by the ROI index, e.g. `original_image_1.tif`.

Working directory before running ROI_crop.py  |   Working directory after running ROI_crop.py        
:--------------------------------------------:|:----------------------------------------------:
![](https://github.com/ntomen/ROI_crop/blob/master/readme/dir_before.png) | ![](https://github.com/ntomen/ROI_crop/blob/master/readme/dir_after.png)

The above example shows only one .tif file from which the ROIs are extracted but the script will loop through all images of the .tif/.tiff format in the directory where `ROI_crop.py` is placed, and crop out all the ROIs in a similar way.

To run `ROI_crop.py` with the default settings, it sufficient to navigate on the terminal/command prompt (depending on your OS) to the directory where the collection of .tif/.tiff images and `ROI_crop.py` are located, and execute

    python ROI_crop.py

For non-default settings and detailed usage guidelines, please see the next sections about optional input arguments and setup & usage directions.

## 3. Optional input arguments

### bg_opacity
By default `ROI_crop.py` maps the pixels outside of the ROI ('background') to a white color ([255,255,255] in RGB space). Similarly, the red contours, both inside and surrounding the ROI, will be set to white.

Therefore, by default the background is kept opaque. If instead it is desirable to set the the background and the red annotation pixels to transparent (by setting alpha=0), rather than setting their color to white, the option --bg_opacity can be set to False.

    python ROI_crop.py --bg_opacity=False

Default value: True. Note: When set to False, the script will save the tif files in RGBA format (bit depth 32), instead of RGB (bit depth 24).')

Cropped ROI 1 on transparent background |  Cropped ROI 2 onto transparent background|  How ROI 1 looks on non-white background
:----------------------------:|:-----------------------------:|:----:
 ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_1_transparent.png) | ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_2_transparent.png) |    ![](https://github.com/ntomen/ROI_crop/blob/master/readme/transparent_eg.png){:height="50px" width="50px"}
	


### contours in contours
Standard work flow:
Left-before image
Right-after image
The contours_in_contours algorithm adopts a modified version of the [Scan-flood Fill (SCAFF)](https://github.com/SherylHYX/Scan-flood-Fill) algorithm.

### bg_color

### save directory

## 4. Setup & Usage Directions

## Authors

* **Nergis Tomen** - [TU Delft](https://www.tudelft.nl/en/eemcs/the-faculty/departments/intelligent-systems/pattern-recognition-bioinformatics/computer-vision-lab/people/nergis-toemen/) - [github](https://github.com/ntomen)
