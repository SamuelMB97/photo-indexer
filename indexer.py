import sys
import os


def is_image(file_name):
    if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
        return True
    else:
        return False


def index_image_dir_recursive(directory, recursive_depth=1):
    """Searches directory recursively, indexing folders with images
    inside
    
    Takes a directory name or path and adds an index to each folder
    inside that has images within them. Returns True if there are 
    images are inside
    """

    depth_tab = "|\t"*recursive_depth
    print(f"{depth_tab}scanning {directory}")
    dir_data = {"directories_with_images": [], "images": []}

    for entry in os.scandir(directory):

        # CASE 1 DIRECTORY
        if entry.is_dir(): 
            print(f"{depth_tab}Found DIRECTORY")

            #Recursive call vv
            sub_dir_data = index_image_dir_recursive(entry, recursive_depth+1) # check for images inside

            if sub_dir_data["images"] or sub_dir_data["directories_with_images"]:
                dir_data["directories_with_images"].append(entry)
                create_index(sub_dir_data) # TODO make this function and one that it references to set up images

        # TODO make this elif vv reference a helper function
        # CASE 2 IMAGE
        elif is_image(entry.name):
            print(f"{depth_tab}Found IMAGE")
            dir_data["images"].append(entry)

        # CASE 3 NOT A DIRECTORY OR AN IMAGE
        else:
            print(f"{depth_tab}Found NON IMAGE/DIR")

    
    print(f"{depth_tab}done scanning {directory}, has images inside? {bool(dir_data["images"])}")

    return dir_data
        

def create_index(entry):
    pass
    #with open("this should be the index name?") as d:



def main():
    print(index_image_dir_recursive(sys.argv[1]))



if __name__ == "__main__":
    main()