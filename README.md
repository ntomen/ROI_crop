# ROI crop
For cropping out annotated ROIs, especially in bioimaging data marked by red annotation lines in QuPath.

Generically, the script found here may be used to crop out parts of any TIFF image circled by solid red lines (multiple crop-outs in multiple images supported). However, this repository was started to help with cropping out exported ROI annotations in [QuPath, the open source software for bioimage analysis](https://github.com/qupath/qupath). Therefore, the script here is intended to be used to crop out ROIs annotated by red lines in biomedical images saved in .tif/.tiff format.

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

The above example shows only one .tif file from which the ROIs are extracted but the script will loop through all images of the .tif/.tiff format in the directory where `ROI_crop.py` is placed, and crop out all the ROIs in the same manner.

To run `ROI_crop.py` with the default settings, it is sufficient to navigate on the terminal/command prompt (depending on your OS) to the directory where the collection of .tif/.tiff images and `ROI_crop.py` are located, and call

    python ROI_crop.py

For non-default settings and detailed usage guidelines, please see the next sections about optional input arguments and setup & usage directions.

## 3. Optional input arguments

### background opacity
By default `ROI_crop.py` maps the pixels outside of the ROI ('background') to a white color ([255,255,255] in RGB space). Similarly, the red contours, both inside and surrounding the ROI, will be set to white.

Therefore, by default the background is kept opaque. If instead it is desirable to set the the background and the red annotation pixels to transparent (by setting alpha=0), rather than setting their color to white, the option `--bg_opacity` can be set to `False`.

    python ROI_crop.py --bg_opacity=False

Default value: `True`. Note: When set to `False`, the script will save the .tif files in RGBA format (bit depth 32), instead of RGB (bit depth 24).

Cropped ROI 1 on transparent background |  Cropped ROI 2 on transparent background|  How the crops look on non-white background
:----------------------------:|:-----------------------------:|:----:
 ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_1_transparent.png) | ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_2_transparent.png) |    ![](https://github.com/ntomen/ROI_crop/blob/master/readme/transparent_eg.png) -------------------------------------------------------for example if you open it in photoshop
	


### contours in contours
The default settings do not recognize contours (or other annotations using red lines) within ROIs. 
Even if other annotations or red contours exist within a ROI, the code will only recognize the **outermost** red contours as defining a ROI. This will then be cropped out into its own .tif file and the red lines both inside and surrounding the ROI will be set to the background color (or transparent if `--bg_opacity=False`).

To change this behaviour please use the `--contours_in_contours` option.

    python ROI_crop.py --contours_in_contours=True

When `True` the algorithm will scan for concentric contours and will exclude regions within the ROI annotated by red closed contours from the crop. This option may be useful when manually removing regions within the ROI, such as visible blood vessels, if desired.

Default value: `False`. By default the script will ignore annotations within the ROI and delete the red lines marking them as described above. Note: When set to `True`, a rather slow scanning operation will be used. The scan is estimated to take 2-10 minutes to process a single image of 10000x10000 resolution.

The contours_in_contours algorithm adopts a modified version of the [Scan-flood Fill (SCAFF)](https://github.com/SherylHYX/Scan-flood-Fill) algorithm.

Original image |  Default behaviour|  contours_in_contours behaviour
:----------------------------:|:-----------------------------:|:----:
 ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_im_crop.png) | ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_1.png) |    ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_1_c_in_c.png)
### background color
When the background color is opaque (`--bg_opacity=False`) the default behaviour is to set the background color to white. A different background color can be specified using the `--bg_color` option.

The `--bg_color` argument admits inputs in RGB format, so 3 integer values in range [0,255] need to be passed as input arguments. For example, to get a black background call

    python ROI_crop.py --bg_color 0 0 0
    
or for a green background call

    python ROI_crop.py --bg_color 0 255 0

Default value: white/[255,255,255].

Default behaviour (white background) |  Black background|  Green background
:----------------------------:|:-----------------------------:|:----:
 ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_2.png) | ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_2_bg_black.png) |    ![](https://github.com/ntomen/ROI_crop/blob/master/readme/original_image_ROI_2_bg_green.png)
 
### save directory
As explained above in section 2, the cropped .tif files will be saved default in a subdirectory called `cropped_images`. Optionally, you could specify the name of the subdirectory where the .tif files should be saved. If the subdirectory does not exist in the current working directory, it will be automatically created.

To specify the save directory, please use the `--save_dir` option.

    python ROI_crop.py --save_dir=cropped_ROIs

Default value: `cropped_images`

## 4. Setup & Usage Directions

### Setup

To run this script, you need a python installation. You can follow the instructions [here](https://realpython.com/installing-python) based on your OS. The instructions are up-to-date as of April 30, 2020.

Once you have python set up, you need to install some image processing libraries. This is straightforward using 'pip', which should automatically be installed together with the python installation. To check if you have pip installed on a Windows OS, you can type 'cmd' to into the search bar in the Start menu, and then click on Command Prompt. In command prompt, you can type:

    pip --version

For Linux, just enter it in the terminal.

If you don't get an error msg, and the pip version is printed you can continue with package installations. (Otherwise please install pip or another package manager like Anaconda).

To install the libraries, open to the command prompt/terminal again and call

    python3 -m pip install --upgrade pip
    pip install opencv-python
    pip install numpy

In Windows, you may have to also call

    python3 -m pip install --upgrade Pillow

### Usage

Download the script `ROI_crop.py` and put it in a directory together with the TIFF images with annotations. Tip: You may first want to test with 2-3 images in a directory, and check for errors as well as measure execution time which is especially important if you want to use the contous_in_contours option.

Next navigate to the directory containing the images to be processed and the script on the command prompt/terminal. For an example in Windows, let's say the .tif files as well as `ROI_crop.py` are now located in `C:\Users\Nergis\Documents\work\all_images`. This means after you open command prompt you need to type `cd Documents\work\all_images` and press Enter.

Once you're in the directory `all_images` just call

    python ROI_crop.py

to execute the script with default settings. To run it with optional settings, please see Section 3 above.

## Authors

* **Nergis Tomen** - [TU Delft](https://www.tudelft.nl/en/eemcs/the-faculty/departments/intelligent-systems/pattern-recognition-bioinformatics/computer-vision-lab/people/nergis-toemen/) - [github](https://github.com/ntomen)
