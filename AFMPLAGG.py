import os
import pandas as pd
import pySPM
import matplotlib.pyplot as plt
from skimage.morphology import binary_erosion, binary_closing, disk
import cv2
import numpy as np
from matplotlib.widgets import Slider

# --- Image processing function ---
def process_image(image, min_area=5, filename="image", lower_threshold=2.3, upper_threshold=255, height_map=None):
    """
    Process AFM images to detect aggregates, measure their area and volume,
    save contour coordinates + metrics to Excel, and save an output image with drawn contours.
    """
    
    # Apply threshold to create binary mask
    binary_mask = (image < upper_threshold) & (image > lower_threshold)
    binary_mask = binary_mask.astype(np.uint8)
    
    # Close small gaps in binary mask
    closed_mask = binary_closing(binary_mask, disk(1)).astype(np.uint8)
    
    # Find connected contours
    contours, _ = cv2.findContours(closed_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Convert grayscale to RGB for drawing
    image_uint8 = np.uint8(image.copy())
    color_image = cv2.cvtColor(image_uint8, cv2.COLOR_GRAY2RGB)
    
    contour_data = []       # Store contour coordinates
    volume_area_data = []   # Store area and volume for each aggregate

    contour_count = 1
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= min_area:
            # Create mask for current contour
            mask = np.zeros_like(image, dtype=np.uint8)
            cv2.drawContours(mask, [contour], -1, 1, thickness=cv2.FILLED)

            # Estimate volume from original height map
            if height_map is not None:
                aggregate_heights = height_map[mask == 1]
                volume = np.sum(aggregate_heights)
            else:
                volume = np.nan

            # Draw contour outline
            cv2.drawContours(color_image, [contour], -1, (0, 255, 0), 1)

            # Save contour coordinates
            for point in contour:
                x, y = point[0]
                contour_data.append([f"{filename}_{contour_count:05d}", x, y])

            # Save metrics
            volume_area_data.append({
                "filename": f"{filename}_{contour_count:05d}",
                "area_px2": area,
                "volume_px2_nm": volume
            })

            contour_count += 1

    # Save coordinates and metrics to Excel
    df_coords = pd.DataFrame(contour_data, columns=["filename", "X", "Y"])
    df_metrics = pd.DataFrame(volume_area_data)

    output_xlsx_path = os.path.join(output_folder, f"{filename}_path.xlsx")
    with pd.ExcelWriter(output_xlsx_path, engine='openpyxl', mode='w') as writer:
        df_coords.to_excel(writer, index=False, sheet_name='contour_coordinates')
        df_metrics.to_excel(writer, index=False, sheet_name='aggregate_area_volume')
    
    print(f"Saved Excel with coordinates and metrics: {output_xlsx_path}")

    # Save output image with contours
    output_image_path = os.path.join(output_image, f"{filename}_contours.jpg")
    cv2.imwrite(output_image_path, color_image)
    print(f"Saved image with contours: {output_image_path}")

    return color_image

# --- Folder paths (adjust before running) ---
input_folder = 'path/to/input/folder'
output_folder = 'path/to/output/coordinate/folder'
output_image = 'path/to/output/image/folder'

# Create output folders if missing
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Check input folder contents
files_in_input_folder = os.listdir(input_folder)
if not files_in_input_folder:
    print("No files found in the input folder.")
else:
    print(f"Found {len(files_in_input_folder)} files in the input folder:")


# --- Process each file ---
for subdir, _, files in os.walk(input_folder):
    for file in files:
        if file == '.DS_Store':  # Skip system files on macOS
            continue

        image_path = os.path.join(subdir, file)
        current_image_filename = file

        # Load AFM/SEM file with pySPM
        image = pySPM.Bruker(image_path)
        height = image.get_channel("Height")

        # Apply corrections: flattening, scar removal, plane fit, etc.
        top = height.correct_lines(inline=False)
        top = top.correct_plane(inline=False)
        top = top.filter_scars_removal(.7, inline=False)
        top = top.correct_plane(inline=False)
        top = top.corr_fit2d(inline=False).offset([[10, 0, 10, 255]]).filter_scars_removal()
        mask0 = top.get_bin_threshold(.1, high=False)
        mask1 = binary_erosion(mask0, disk(3))
        top = top.corr_fit2d(mask=mask1, inline=False).offset([[10, 0, 10, 255]]).filter_scars_removal().correct_plane().correct_lines().zero_min()
        
        # Convert height data to NumPy array
        height_dataframe = pd.DataFrame(top.pixels)
        height_array = height_dataframe.to_numpy()

        # Display figure with interactive sliders
        fig, ax = plt.subplots(figsize=(18, 9))
        plt.subplots_adjust(bottom=0.25, left=0, right=0.9, top=0.9)
        
        # Prepare initial thresholded image
        thresholded_image = height_array.copy()
        thresholded_image[(thresholded_image < 1.4) | (thresholded_image > height_array.max())] = 255

        # Process image with initial parameters
        initial_image = process_image(
            thresholded_image,
            min_area=5,
            filename=current_image_filename,
            lower_threshold=1.4,
            upper_threshold=height_array.max(),
            height_map=height_array
        )

        im = ax.imshow(initial_image)
        plt.colorbar(im)

        # --- Slider widgets for adjusting thresholds and min area ---
        ax_slider_lower = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor="lightgray")
        ax_slider_upper = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor="lightgray")
        ax_slider_min_area = plt.axes([0.2, 0.00, 0.65, 0.03], facecolor="lightgray")  

        slider_lower = Slider(ax_slider_lower, "Lower Threshold", height_array.min(), height_array.max()/10, valinit=2.3)
        slider_upper = Slider(ax_slider_upper, "Upper Threshold", height_array.min()*0.5, height_array.max(), valinit=height_array.max())
        slider_min_area = Slider(ax_slider_min_area, "Min Object Area", 0, 100, valinit=5, valstep=1)

        # --- Callback to update image when sliders change ---
        def update_threshold(val):
            lower_threshold = slider_lower.val
            upper_threshold = slider_upper.val
            min_area = int(slider_min_area.val)

            mod_image = height_array.copy()
            mod_image[(mod_image < lower_threshold) | (mod_image > upper_threshold)] = 255

            updated_image = process_image(
                mod_image,
                min_area=min_area,
                filename=current_image_filename,
                lower_threshold=lower_threshold,
                upper_threshold=upper_threshold,
                height_map=height_array
            )

            im.set_data(updated_image)
            im.set_cmap(None)
            plt.draw()

        # Link sliders to update function
        slider_lower.on_changed(update_threshold)
        slider_upper.on_changed(update_threshold)
        slider_min_area.on_changed(update_threshold)

        plt.show()
