# ROI crop
For cropping out annotated ROIs, especially in bioimaging data marked by red annotation lines in QuPath.

Generically, the script found here may be used to crop out parts of any tif image circled by solid red lines (multiple crop-outs in multiple images supported). However, this repository was started to help with cropping out exported ROI annotations in [QuPath, the open source software for bioimage analysis](https://github.com/qupath/qupath). Therefore, the script here is intended to be used to crop out ROIs annotated by red lines in biomedical images saved in .tif/.tiff format.

If you use the contents of this repository, please give credit to this github page.

## 1. Requirements
- Python installation (tested mainly on python 3, but should work with python 2)
- argparse
- OpenCV
- PIL/Pillow
- NumPy

## 2. How it works
The python script is meant to be placed in a directory with multiple annotated biomedical images in .tif/.tiff format, with red lines encircling regions of interest (ROIs). Running the script will crop out each ROI into its own .tif image against a white/transparent background.

Standard work flow:
Left-before image
Right-after image

Image before                   |             Image after
:-----------------------------:|:-----------------------------:
![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image.png "title-1") | ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_1.png "title-2")

![Image after2](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_2.png)

Describe how it should be run.

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

* **Nergis Tomen** - [github](https://github.com/ntomen)
