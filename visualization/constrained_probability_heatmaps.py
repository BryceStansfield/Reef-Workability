import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pathlib
import math
from PIL import Image
from models.model_training import MODEL_FEATURES, MODEL_FEATURES_TO_PRETTY_NAME
from matplotlib.ticker import MaxNLocator

def plot_along_dimensions(x: str, y: str, monthly_table: pd.DataFrame, bounds_per_feature, save_path: pathlib.Path, num_bins=50):
    x_bounds = bounds_per_feature[x]
    y_bounds = bounds_per_feature[y]

    x_bin_width = (x_bounds[1]-x_bounds[0])/num_bins
    y_bin_width = (y_bounds[1]-y_bounds[0])/num_bins

    vals = [[[] for _ in range(num_bins)] for _ in range(num_bins)]

    for _, row in monthly_table.iterrows():
        x_val = getattr(row, x)
        y_val = getattr(row, y)
        prob_val = getattr(row, "predicted_success_prob")

        x_bin = math.floor((x_val - x_bounds[0])/x_bin_width)
        y_bin = math.floor((y_val - y_bounds[0])/y_bin_width)

        if x_bin == num_bins:
            x_bin -= 1
        if y_bin == num_bins:
            y_bin -= 1

        vals[y_bin][x_bin].append(prob_val)
    
    im = Image.new("RGBA", (num_bins, num_bins))
    for y_bin in range(num_bins):
        for x_bin in range(num_bins):
            xy_vals = vals[y_bin][x_bin]

            if len(xy_vals) == 0:
                im.putpixel((x_bin, y_bin), (0,0,0,0))
            else:
                average_prob = sum(xy_vals)/len(xy_vals)
                blue = round(255 * average_prob)
                red = 255 - blue
                im.putpixel((x_bin, y_bin), (red, 0, blue, 255))
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(im,
                aspect='auto',
                origin='lower',
                extent=[x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]])
    ax.set_box_aspect(1)
    x_pretty = MODEL_FEATURES_TO_PRETTY_NAME[x]
    y_pretty = MODEL_FEATURES_TO_PRETTY_NAME[y]

    ax.set_xlabel(x_pretty)
    ax.set_ylabel(y_pretty)
    ax.set_title(f"{x_pretty} vs {y_pretty} Success Probabilites")

    ax.xaxis.set_major_locator(MaxNLocator(nbins=5, steps=[1,2,5,10]))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5, steps=[1,2,5,10]))

    fig.savefig(save_path)

def plot_workability_heatmaps_with_constraints(historical_probabilities, save_directory=pathlib.Path("PlotOutputs/heatmaps")):
    bounds_per_feature = {}
    for feature in MODEL_FEATURES:
        bounds_per_feature[feature] = (historical_probabilities[feature].min(), historical_probabilities[feature].max())

    for month in range(1, 13):
        for i in range(len(MODEL_FEATURES)):
            for j in range(i+1, len(MODEL_FEATURES)):

                if MODEL_FEATURES[i] == "day_of_year" or MODEL_FEATURES[j] == "day_of_year":
                    continue
                
                month_table = historical_probabilities[historical_probabilities["datetime"].dt.month == month]
                plot_along_dimensions(MODEL_FEATURES[i], MODEL_FEATURES[j], month_table, bounds_per_feature, pathlib.Path(save_directory / f"{month}_{MODEL_FEATURES[i]}_{MODEL_FEATURES[j]}.png"))