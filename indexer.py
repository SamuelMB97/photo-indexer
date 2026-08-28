import sys
import os


def index_image_dir_recursive(directory, recursive_depth=1):
    """Searches directory recursively, indexing folders with images
    inside
    
    Takes a directory name or path and adds an index to each folder
    inside that has images within them. Returns True if there are 
    images are inside
    """

    depth_tab = "|\t"*recursive_depth
    print(f"{depth_tab}scanning {directory}")
    images_inside = False
    images = []
    directories = []

    for entry in os.scandir(directory):

        if entry.is_dir(): # Case 1 directory
            print(f"{depth_tab}Found DIRECTORY")
            sub_has_images = index_image_dir_recursive(entry, recursive_depth+1) # check for images inside

            if sub_has_images:
                images_inside = True
                create_index() # TODO make this function and one that it references to set up images

        # TODO make this elif vv reference a helper function
        elif entry.name.lower().endswith((".jpg", ".jpeg", ".png", ".gif")): # Case 2 image 
            print(f"{depth_tab}Found IMAGE")
            # set up image
            images.append(entry)
            images_inside = True

        else:
            print(f"{depth_tab}Found NON IMAGE/DIR")

    
    print(f"{depth_tab}done scanning {directory}, has images inside? {images_inside}")

    if images_inside:
        return True
    else: return False
        

def create_index():
    pass


def main():
    print(index_image_dir_recursive(sys.argv[1]))



if __name__ == "__main__":
    main()