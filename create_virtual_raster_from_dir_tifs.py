import glob
import os
# The directory where the tif-files live. The last / is important
data_directory = "/home/iiro/Documents/Koulutyöt/Gradu/data/predictions/older slope filtered"
out_vrt_path = data_directory + os.path.basename(os.path.normpath(data_directory)) + ".vrt"
data_files = [file for file in glob.glob(data_directory + "**/*.tif", recursive=True)]

tmp_txt_file = "/home/iiro/Documents/Koulutyöt/Gradu/data/predictions/older slope filtered.txt"

if os.path.exists(tmp_txt_file):
    os.remove(tmp_txt_file)

with open(tmp_txt_file, 'w') as fp:
    for name in data_files:
        fp.write(f"{name}\n")

"""
processing.run("gdal:buildvirtualraster",
{'INPUT':tmp_txt_file,'RESOLUTION':0,'SEPARATE':False,
'PROJ_DIFFERENCE':False,'ADD_ALPHA':False,'ASSIGN_CRS':None,
'RESAMPLING':0,'SRC_NODATA':0,'EXTRA':'','OUTPUT':out_vrt_path})
"""