# AFMPLAGG.py

This repository contains a Python script for **processing AFM images** (e.g., Bruker format) to:
- Detect and segment aggregates
- Measure their **area** and **volume** from height maps
- Save **contour coordinates** and metrics into Excel files
- Export processed images with drawn contours
- Interactively adjust thresholds and object size using sliders

## Requirements

Install the dependencies before running:

```
pip install pandas pySPM matplotlib scikit-image opencv-python openpyxl numpy
```

## Folder Structure

You need to specify three folders in the script:
	- input_folder → path to folder containing input AFM files (.spm, etc.)
	- output_folder → path where Excel files with contour coordinates and aggregate metrics will be saved
	- output_image → path where processed images with contours will be saved

```
input_folder = "data/input"
output_folder = "data/output/excel"
output_image = "data/output/images"
```

## Features
  •	The script loads each AFM image, applies flattening and artifact corrections, then performs threshold-based segmentation.
  •	Each detected aggregate is outlined with contours (green).
  •	Metrics saved:
  •	area_px2 → projected aggregate area in pixels²
  •	volume_px2_nm → integrated volume from height map (in nm)
  •	Interactive sliders allow tuning:
  •	Lower threshold
  •	Upper threshold
  •	Minimum object area

## Outputs
Excel file (*_path.xlsx) containing contour_coordinates → X, Y coordinates of each contour, and aggregate_area_volume → area and volume data per aggregate
Image file (*_contours.jpg) with contours drawn.

## Example Workflow
Load AFM/SEM height map
Apply corrections
Detect aggregates above threshold
Export data and visualization











