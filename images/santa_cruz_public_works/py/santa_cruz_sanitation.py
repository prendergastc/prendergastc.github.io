# ----------------------------------------------------------------------------------------------------------------------
# santa_cruz_sanitation.py
# Christopher Prendergast
# 2024/05/04
# ----------------------------------------------------------------------------------------------------------------------
import arcpy
from pathlib import Path
from shutil import copytree

# Set project directory, geodatabase, feature class, field, and old/new pdf subdirectory names.
my_proj_dir = r"C:\ArcGIS_local_projects\Sanitation"
my_gdb = "SanitationData.gdb"
my_fc = "SanitationMapIndex"
my_field = "FileName"
my_old_pdf_subdir = "SanitationMaps"
my_new_pdf_subdir = "NewSanitationMaps"
my_save_pdf_subdir = "SanitationMapsSave"
line = "-" * 80

# Establish the old directory and check it exists.
old_dir = Path(my_proj_dir, my_old_pdf_subdir)
assert old_dir.is_dir(), "old_dir: {0} is not a directory or does not exist.".format(old_dir)
print("...old_dir", old_dir)

# Establish the save directory and create it if it doesn't already exist.
# Make a backup copy just in case!
save_dir = Path(my_proj_dir, my_save_pdf_subdir)
if not save_dir.is_dir():
    copytree(old_dir, save_dir)
assert save_dir.is_dir(), "save_dir: {0} is not a directory or does not exist.".format(save_dir)
print("...save_dir:", save_dir)

# Establish the new directory and create it if it doesn't already exist.
new_dir = Path(my_proj_dir, my_new_pdf_subdir)
new_dir.mkdir(parents=True, exist_ok=True)
assert new_dir.is_dir(), "new_dir: {0} is not a directory or does not exist.".format(new_dir)
print("...new_dir:", new_dir)

# Establish the geodatabase and check it exists.
sanitation_gdb = Path(my_proj_dir, my_gdb)
assert sanitation_gdb.is_dir(), "sanitation_gdb: {0} is not a directory or does not exist.".format(sanitation_gdb)
print("...sanitation_gdb", sanitation_gdb)

# Establish the feature class.
fc = Path(sanitation_gdb, my_fc)
print("...fc:", fc)

# Check that the feature class exists.
arcpy.env.workspace = str(sanitation_gdb)
assert arcpy.Exists(str(fc)), "fc: feature class {0} does not exists".format(fc)

# Check that field exists.
fields = arcpy.ListFields(str(fc), my_field)
assert len(fields) == 1 and fields[0].name == my_field, "my_fields: field {0} not found".format(my_field)
print("...my_field:", my_field)
print(line)

# Establish empty lists to hold any files that are not found in the old directory or are duplicate references.
files_not_found = []
duplicate_file_refs = []

# Establish a search cursor.
cursor = arcpy.da.SearchCursor(str(fc), ["OID@", my_field])
# Iterate through records in cursor.
for row in cursor:
    # Get the file name from the current record.
    curr_id, curr_file = row
    old_pdf_file = Path(old_dir, curr_file)
    new_pdf_file = Path(new_dir, curr_file)

    if old_pdf_file.is_file() and not new_pdf_file.is_file():
        # If the file exists then move it to the new directory.
        old_pdf_file.rename(new_pdf_file)
        print("-->", "{0}: File {1} moved to {2}".format(curr_id, curr_file, new_pdf_file))
    elif new_pdf_file.is_file():
        # If thee file already exists in the target directory then add it to a list of duplicate references.
        print("***", "{0}: Duplicate reference. File {1} already exists in {2}".format(curr_id, curr_file, new_dir))
        duplicate_file_refs.append(curr_file)
    else:
        # Otherwise, if the file is not found, add it to the list of missing files.
        print("***", "{0}: file {1} not found.".format(curr_id, old_pdf_file))
        files_not_found.append(old_pdf_file)

# Print list files in the save directory.
print()
print(line)
print("Files in the save directory {0}".format(save_dir))
print(line)
n = 0
for f in save_dir.iterdir():
    print("\t{0}".format(f.name))
    n += 1
print("Total number of files in the save directory: {0}".format(n))

# Print list of file references where the file was not found in the original directory.
print()
print(line)
print("Files not found in original directory {0}".format(old_dir))
print(line)
n = 0
for f in files_not_found:
    print("\t{0}".format(f.name))
    n += 1
print("Total number of file references not found in original directory: {0}".format(n))

# Print list of duplicate file references.
print()
print(line)
print("Duplicate file reference where the same file has already been moved.")
print(line)
n = 0
for f in duplicate_file_refs:
    print("\t{0}".format(f))
    n += 1
print("Total number of duplicate file references: {0}".format(n))

# Print list of files that remain in the original directory.
print()
print(line)
print("Files remaining in the original directory after move {0}".format(old_dir))
print(line)
n = 0
for f in old_dir.iterdir():
    print("\t{0}".format(f.name))
    n += 1
print("Total number of files remaining in the original directory after move: {0}".format(n))

# Print list of files found in the new directory.
print()
print(line)
print("Files found in new directory after move {0}".format(new_dir))
print(line)
n = 0
for f in new_dir.iterdir():
    print("\t{0}".format(f.name))
    n += 1
print("Total number of files found in new directory after move: {0}".format(n))


# ----------------------------------------------------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------------------------------------------------
# "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" C:\PythonPro\Ex11\sanitation.py
# ...old_dir C:\ArcGIS_local_projects\Sanitation\SanitationMaps
# ...save_dir: C:\ArcGIS_local_projects\Sanitation\SanitationMapsSave
# ...new_dir: C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps
# ...sanitation_gdb C:\ArcGIS_local_projects\Sanitation\SanitationData.gdb
# ...fc: C:\ArcGIS_local_projects\Sanitation\SanitationData.gdb\SanitationMapIndex
# ...my_field: FileName
# --------------------------------------------------------------------------------
# --> 1: File A-082_COMPLETE.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-082_COMPLETE.pdf
# --> 2: File A-200.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-200.pdf
# --> 4: File A-018a.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-018a.pdf
# --> 7: File C-055.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\C-055.pdf
# --> 9: File A-216.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-216.pdf
# --> 11: File A-030.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-030.pdf
# *** 12: Duplicate reference. File A-082_COMPLETE.pdf already exists in C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps
# --> 14: File A-077.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-077.pdf
# --> 15: File C-128.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\C-128.pdf
# --> 16: File A-021.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-021.pdf
# --> 18: File A-031.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-031.pdf
# --> 19: File A-027.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-027.pdf
# --> 21: File A-018.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-018.pdf
# --> 22: File C-125.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\C-125.pdf
# --> 23: File A-191.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-191.pdf
# --> 25: File A-029.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-029.pdf
# *** 26: Duplicate reference. File A-082_COMPLETE.pdf already exists in C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps
# --> 28: File C-120.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\C-120.pdf
# --> 29: File C-021.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\C-021.pdf
# *** 31: Duplicate reference. File A-082_COMPLETE.pdf already exists in C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps
# --> 32: File C-116.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\C-116.pdf
# --> 34: File C-008.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\C-008.pdf
# --> 35: File C-109.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\C-109.pdf
# --> 36: File A-020.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-020.pdf
# --> 37: File A-149.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-149.pdf
# --> 38: File A-022.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-022.pdf
# --> 39: File A-196.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-196.pdf
# --> 40: File A-019.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-019.pdf
# --> 42: File C-129.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\C-129.pdf
# --> 43: File A-017.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-017.pdf
# --> 44: File A-032.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\A-032.pdf
# --> 45: File C-123.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\C-123.pdf
# --> 46: File C-050.pdf moved to C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps\C-050.pdf
#
# --------------------------------------------------------------------------------
# Files in the save directory C:\ArcGIS_local_projects\Sanitation\SanitationMapsSave
# --------------------------------------------------------------------------------
# 	A-017.pdf
# 	A-018.pdf
# 	A-018a.pdf
# 	A-019.pdf
# 	A-020.pdf
# 	A-021.pdf
# 	A-022.pdf
# 	A-024.pdf
# 	A-025.pdf
# 	A-026.pdf
# 	A-027.pdf
# 	A-029.pdf
# 	A-030.pdf
# 	A-031.pdf
# 	A-032.pdf
# 	A-034.pdf
# 	A-036.pdf
# 	A-037.pdf
# 	A-039.pdf
# 	A-040..pdf
# 	A-043.pdf
# 	A-044.pdf
# 	A-048.pdf
# 	A-050.pdf
# 	A-051.pdf
# 	A-053.pdf
# 	A-054.pdf
# 	A-056.pdf
# 	A-059.pdf
# 	A-061.pdf
# 	A-062.pdf
# 	A-063.pdf
# 	A-064.pdf
# 	A-065.pdf
# 	A-067.pdf
# 	A-068.pdf
# 	A-069.pdf
# 	A-070.pdf
# 	A-072.pdf
# 	A-073.pdf
# 	A-074.pdf
# 	A-075.pdf
# 	A-076.pdf
# 	A-077.pdf
# 	A-078.pdf
# 	A-082_COMPLETE.pdf
# 	A-149.pdf
# 	A-150.pdf
# 	A-151.pdf
# 	A-186.pdf
# 	A-187.pdf
# 	A-188.pdf
# 	A-189.pdf
# 	A-190.pdf
# 	A-191.pdf
# 	A-194.pdf
# 	A-195.pdf
# 	A-196.pdf
# 	A-197.pdf
# 	A-198.pdf
# 	A-200.pdf
# 	A-202.pdf
# 	A-209.pdf
# 	A-210.pdf
# 	A-211.pdf
# 	A-212.pdf
# 	A-212B.pdf
# 	A-213.pdf
# 	A-213B.pdf
# 	A-214.pdf
# 	A-215.pdf
# 	A-216.pdf
# 	A-217.pdf
# 	A-218.pdf
# 	A-219.pdf
# 	A-220.pdf
# 	A-78.pdf
# 	C-001A.pdf
# 	C-008.pdf
# 	C-021.pdf
# 	C-050.pdf
# 	C-055.pdf
# 	C-108A.pdf
# 	C-109.pdf
# 	C-110.pdf
# 	C-110A.pdf
# 	C-111.pdf
# 	C-112.pdf
# 	C-113.pdf
# 	C-114.pdf
# 	C-115.pdf
# 	C-116.pdf
# 	C-117.pdf
# 	C-118.pdf
# 	C-119.pdf
# 	C-120.pdf
# 	C-121.pdf
# 	C-122.pdf
# 	C-123.pdf
# 	C-124.pdf
# 	C-125.pdf
# 	C-126.pdf
# 	C-127.pdf
# 	C-128.pdf
# 	C-129.pdf
# 	C-130.pdf
# Total number of files in the save directory: 106
#
# --------------------------------------------------------------------------------
# Files not found in original directory C:\ArcGIS_local_projects\Sanitation\SanitationMaps
# --------------------------------------------------------------------------------
# Total number of file references not found in original directory: 0
#
# --------------------------------------------------------------------------------
# Duplicate file reference where the same file has already been moved.
# --------------------------------------------------------------------------------
# 	A-082_COMPLETE.pdf
# 	A-082_COMPLETE.pdf
# 	A-082_COMPLETE.pdf
# Total number of duplicate file references: 3
#
# --------------------------------------------------------------------------------
# Files remaining in the original directory after move C:\ArcGIS_local_projects\Sanitation\SanitationMaps
# --------------------------------------------------------------------------------
# 	A-024.pdf
# 	A-025.pdf
# 	A-026.pdf
# 	A-034.pdf
# 	A-036.pdf
# 	A-037.pdf
# 	A-039.pdf
# 	A-040..pdf
# 	A-043.pdf
# 	A-044.pdf
# 	A-048.pdf
# 	A-050.pdf
# 	A-051.pdf
# 	A-053.pdf
# 	A-054.pdf
# 	A-056.pdf
# 	A-059.pdf
# 	A-061.pdf
# 	A-062.pdf
# 	A-063.pdf
# 	A-064.pdf
# 	A-065.pdf
# 	A-067.pdf
# 	A-068.pdf
# 	A-069.pdf
# 	A-070.pdf
# 	A-072.pdf
# 	A-073.pdf
# 	A-074.pdf
# 	A-075.pdf
# 	A-076.pdf
# 	A-078.pdf
# 	A-150.pdf
# 	A-151.pdf
# 	A-186.pdf
# 	A-187.pdf
# 	A-188.pdf
# 	A-189.pdf
# 	A-190.pdf
# 	A-194.pdf
# 	A-195.pdf
# 	A-197.pdf
# 	A-198.pdf
# 	A-202.pdf
# 	A-209.pdf
# 	A-210.pdf
# 	A-211.pdf
# 	A-212.pdf
# 	A-212B.pdf
# 	A-213.pdf
# 	A-213B.pdf
# 	A-214.pdf
# 	A-215.pdf
# 	A-217.pdf
# 	A-218.pdf
# 	A-219.pdf
# 	A-220.pdf
# 	A-78.pdf
# 	C-001A.pdf
# 	C-108A.pdf
# 	C-110.pdf
# 	C-110A.pdf
# 	C-111.pdf
# 	C-112.pdf
# 	C-113.pdf
# 	C-114.pdf
# 	C-115.pdf
# 	C-117.pdf
# 	C-118.pdf
# 	C-119.pdf
# 	C-121.pdf
# 	C-122.pdf
# 	C-124.pdf
# 	C-126.pdf
# 	C-127.pdf
# 	C-130.pdf
# Total number of files remaining in the original directory after move: 76
#
# --------------------------------------------------------------------------------
# Files found in new directory after move C:\ArcGIS_local_projects\Sanitation\NewSanitationMaps
# --------------------------------------------------------------------------------
# 	A-017.pdf
# 	A-018.pdf
# 	A-018a.pdf
# 	A-019.pdf
# 	A-020.pdf
# 	A-021.pdf
# 	A-022.pdf
# 	A-027.pdf
# 	A-029.pdf
# 	A-030.pdf
# 	A-031.pdf
# 	A-032.pdf
# 	A-077.pdf
# 	A-082_COMPLETE.pdf
# 	A-149.pdf
# 	A-191.pdf
# 	A-196.pdf
# 	A-200.pdf
# 	A-216.pdf
# 	C-008.pdf
# 	C-021.pdf
# 	C-050.pdf
# 	C-055.pdf
# 	C-109.pdf
# 	C-116.pdf
# 	C-120.pdf
# 	C-123.pdf
# 	C-125.pdf
# 	C-128.pdf
# 	C-129.pdf
# Total number of files found in new directory after move: 30
#
# Process finished with exit code 0
# ----------------------------------------------------------------------------------------------------------------------
