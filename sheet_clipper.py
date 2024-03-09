import shutil
import os
import glob
from time import perf_counter
from os.path import exists, join
from statistics import mean

def convert_sec(seconds):
    """ Prints pretty seconds
    """
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)

clip_dir = "/home/iiro/Documents/Koulutyöt/Gradu/data/tmp/clip/"
tmp_clip_poly_dir = "/tmp/clip_poly/"
orig_dir = "/home/iiro/Documents/Koulutyöt/Gradu/data/georef_kartat/"

tmp_dirs = [clip_dir, tmp_clip_poly_dir]
for dir in tmp_dirs:
    if not os.path.isdir(dir):
        os.mkdir(dir)

grid_path = "/home/iiro/Documents/Koulutyöt/Gradu/data/grids/newer.gpkg"
grid_layer = QgsVectorLayer(grid_path, "grid", "ogr")
grid = grid_layer.getFeatures()
cell_count = 2722
times = []
for i, cell in enumerate(grid):
    loop_start = perf_counter()
    
    # Converts the needed feature to separate vector layer and saves it to temp file
    # Necessary attributes
    image_name = cell['filename']
    
    if not image_name == "304406_304409_1974.jpg":
        continue
    
    in_path = os.path.join(orig_dir, image_name)
    out_path = os.path.join(clip_dir, image_name)
    feature_id = cell['fid']
    
    cell_path = join(tmp_clip_poly_dir, str(feature_id) + ".gpkg")
    selection_expression = f'"fid"=\'{feature_id}\''
    grid_layer.selectByExpression(selection_expression)
        
    # Save the selected feature to temporary location as geopackage
    QgsVectorFileWriter.writeAsVectorFormat(
    grid_layer, cell_path, "utf-8", 
    grid_layer.crs(), "GPKG", 1)
    # Opening the one cell file
    cell_layer = QgsVectorLayer(cell_path, "cell", "ogr")
    

    processing.run("gdal:cliprasterbymasklayer", 
    {'INPUT':in_path,
    'MASK':cell_layer,
    'SOURCE_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:3067'),
    'TARGET_EXTENT':None,'NODATA':0,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,'KEEP_RESOLUTION':False,
    'SET_RESOLUTION':False,'X_RESOLUTION':None,'Y_RESOLUTION':None,
    'MULTITHREADING':True,'OPTIONS':'','DATA_TYPE':0,
    'EXTRA':'','OUTPUT':out_path})
    loop_end = perf_counter()
    time = loop_end-loop_start
    times.append(time)
    ETA = (cell_count - 1 - i) * mean(times)
    ETA = convert_sec(ETA)
    print(f"{i}/ {cell_count -1}, ETA:{ETA}")
    
    
    