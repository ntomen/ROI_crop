# ROI crop
For cropping out annotated ROIs, especially in bioimaging data marked by red annotation lines in QuPath.

This repository was started to help with cropping out exported ROI annotations in [QuPath, the open source software for bioimage analysis](https://github.com/qupath/qupath). The script here may be used to crop out ROIs annotated by red lines in biomedical images saved in .tif/.tiff format.

If you use the contents of this repository, please give credit to this github page.

## 1 Requirements
- Python installation (tested mainly on python 3, but should work with python 2)
- argparse
- OpenCV
- PIL/Pillow
- NumPy

## 2 How it works
The python script is meant to be placed in a directory with multiple annotated biomedical images in .tif/.tiff format, with red lines encircling regions of interest (ROIs). Running the script will crop out each ROI into its own .tif image against a white/transparent background.

Standard work flow:
Left-before image
Right-after image

The contours_in_contours algorithm adopts a modified version of the [Scan-flood Fill (SCAFF)](https://github.com/SherylHYX/Scan-flood-Fill) algorithm.
