# AFMPLAGG.py

AFMPLAGG is a Python and R hardcode setup to perform image analysis of aggregate-like objects, captured by means of atomic force microscopy (AFM). 
Code written for the project entitled "Studies on the conformation and rheological properties of pectins depending on the postharvest maturity of the plant source", supported by the National Science Center, Poland (grant nr - 2023/51/B/NZ9/02121). More information of project: [https://projekty.ncn.gov.pl/index.php?projekt_id=591903](https://projekty.ncn.gov.pl/index.php?projekt_id=604538)

## AFMPLAGG.py
This repository contains a Python script for processing images and detecting contours based on a specified threshold range. It calculates and saves contour coordinates, areas, volumes (if a height map is available), and saves the results in both Excel and image formats.

## Requirements
- Visual Studio Code release: 1.93.1
- Python release: 3.12.4. 64-bit
- RStudio version: 2022.07.1 Build 554

> Warning! There are no guaranties this code will run on your machine.

### Features
- Contour detection: code detects contours in images using a binary thresholding approach
- Area and volume calculation: code computes the area and volume of detected contours if a height map is provided
- Interactive visualization: code allows the user to adjust thresholds and minimum contour area using interactive sliders
- Output: code saves the contour coordinates, volume, and area data in an Excel file, and the processed image with contours in a JPG format
- - Thresholding and filtering: code applies custom thresholds and erosion for better contour identification and image cleanup

### Requirements
- Python 3.12
- Libraries: pandas, pySPM, opencv-python, matplotlib, scikit-image, numpy

You can install these libraries using pip:

### Script overview
The script performs the following operations:
- Load and preprocess images: reads images from an input folder; uses the pySPM package to process and clean up images; corrects the plane, removes scars, and applies additional filters
- Thresholding and contour detection: thresholds the image to create a binary mask based on user-defined upper and lower threshold values; applies morphological operations (erosion and closing) to clean up the binary mask (Fig.1); detects contours and calculates areas and volumes (if a height map is provided)
- Interactive plotting: displays the image and detected contours using matplotlib; provides sliders for adjusting the lower and upper thresholds, as well as the minimum contour area for detection; updates the displayed image interactively based on slider values (Fig.1)
- Data output: saves the contour coordinates and area/volume metrics into an Excel file; saves the processed image with contours drawn on it as a JPG file.

![Figure_1](https://github.com/user-attachments/assets/b1d7fc8c-33a1-47fe-b400-073294bb0f6b)
Fig.1. USer interface representation of an AFMPLAGG.py script.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

> For any issues or feature requests, feel free to open an issue in this repository.
