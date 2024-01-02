import fileunlocker

# Create a File object
file = fileunlocker.File("path_to_file")

# Unlock the file
file.Unlock()

# Force delete the file
file.ForceDelete()

# Create a Dir object
dir = fileunlocker.Dir("path_to_directory")

# Delete the directory
dir.Delete()