# Figures
Python script to generate PDF scientific figures

This script needs 2 files: 
- a data file with a txt extension
- a parameter file with the same name and a param extension

Parameter list:
- Figure_type : errorbar, barchart, scatter
- Index_number : number of index column
- Figure_number : figure id
- Relative_values : 0 if values should be absolute, 1 if they should be relative to the first value
- Xlabel : string to be displayed along the X axis
- Ylabel : string to be displayed along the Y axis
- Xscale : log or linear
- Legend_loc : location of the legend, automatic by default
- Stats : for barcharts, displays stats with stars
- Colormap : color map to be used
