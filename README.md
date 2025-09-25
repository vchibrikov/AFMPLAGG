# AFMPLAGG.py

AFMPLAGG (Atomic Force Microscopy Persistence Length AGGregates) is a Python and R hardcode setup to perform image analysis of an aggregate-like objects, captured by means of atomic force microscopy (AFM). Setup was created for the purposes of 2023/51/B/NZ9/02121 OPUS26 project.

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
- The script loads each AFM image, applies flattening and artifact corrections, then performs threshold-based segmentation.
- Each detected aggregate is outlined with contours (green).


![OPUS26_WSP_0 01_S3_A_S_3 097_contours](https://github.com/user-attachments/assets/e266d4a4-102e-4284-bfe3-66cf281b89e3)


## Metrics saved:
- area_px2 → projected aggregate area in pixels²
- volume_px2_nm → integrated volume from height map (in nm)
- Interactive sliders allow tuning:
- Lower threshold
- Upper threshold
- Minimum object area

## Outputs
- Excel file (*_path.xlsx) containing contour_coordinates → X, Y coordinates of each contour, and aggregate_area_volume → area and volume data per aggregate
- Image file (*_contours.jpg) with contours drawn.

## Example workflow
- Load AFM/SEM height map
- Apply corrections
- Detect aggregates above threshold
- Export data and visualization

## Citation
If you use this script in research, please cite this repository or acknowledge the tool in your methods section.

## License
This project is released under the MIT License.
Feel free to use and modify it for your own research.










