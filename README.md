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

For non-default settings and detailed usage guidelines, please see the next sections about optional input arguments and setup & usage directions.

## 3. Optional input arguments

### bg_opacity
Standard work flow:
Left-before image
Right-after image

### contours in contours
Standard work flow:
Left-before image
Right-after image
The contours_in_contours algorithm adopts a modified version of the [Scan-flood Fill (SCAFF)](https://github.com/SherylHYX/Scan-flood-Fill) algorithm.

### save directory

## 4. Setup & Usage Directions

## Authors

* **Nergis Tomen** - [TU Delft](https://www.tudelft.nl/en/eemcs/the-faculty/departments/intelligent-systems/pattern-recognition-bioinformatics/computer-vision-lab/people/nergis-toemen/) - [github](https://github.com/ntomen)
