import os

def get_files_info(working_directory, directory = None):

    #making sure that directory is not None
    if directory == None:
        return f'Error: No directory given.'

    #if directory is not in working_directory
    working_directory_absolute_path = os.path.abspath(working_directory)
    directory_absolute_path = os.path.abspath(os.path.join(working_directory, directory))

    if not directory_absolute_path.startswith(working_directory_absolute_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(directory_absolute_path):
        return f'Error: "{directory}" is not a directory'

    directory_contents=os.listdir(directory_absolute_path)
    return_list=[]
    for item in directory_contents:
        item_path = os.path.join(directory_absolute_path, item)
        return_list.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")

    return "\n".join(return_list)

