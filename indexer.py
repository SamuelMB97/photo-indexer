import sys
import os
import exif





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
            create_index(entry, sub_dir_data)

        # CASE 2 IMAGE
        elif is_image(entry.name):
            print(f"{depth_tab}Found IMAGE")
            dir_data["images"].append(entry)

        # CASE 3 NOT A DIRECTORY OR AN IMAGE
        else:
            print(f"{depth_tab}Found NON IMAGE/DIR")

    
    print(f"{depth_tab}done scanning {directory}, has images inside? {bool(dir_data["images"])}")

    return dir_data
        

def create_index(parent_dir, sub_dir_data=None):
    index_path = os.path.join(parent_dir.path, "index.html")
    with open(index_path, "w", encoding="utf-8") as html:
        html.write(create_html_str(parent_dir, sub_dir_data))


def create_html_str(parent_dir, sub_dir_data=None):
    if sub_dir_data["directories_with_images"]:
        sub_dir_links = create_sub_dir_str(sub_dir_data)
    else:
        sub_dir_links = ""

    if sub_dir_data["images"]:
        images_html = create_images_html(sub_dir_data)
    else:
        images_html = ""

    style = """
        <style>
        .dirlink_el {font-size: 125%;}
        .sm_img {max-height: 200px; max-width: 200px;}
        .img_el {display: inline-block; padding-bottom: 15px; padding-right: 10px;}
        </style>""" #style is largely copied from example html

    html_str = f"""
<html>
    <head>{style}
    </head>
    <body>
        <h2> {parent_dir.name} </h2>
        {sub_dir_links}
        <br>
        {images_html}
    </body>
</html>"""
    return html_str


def create_sub_dir_str(sub_dir_data):
    sub_dir_str = ""

    for sub_dir in sub_dir_data["directories_with_images"]:
        sub_dir_str = sub_dir_str + f"""
        <div class="dirlink_el">
            <a href={sub_dir.name + r"\index.html"}>{sub_dir.name}</a>
        </div>"""
    
    return sub_dir_str


def create_images_html(sub_dir_data): # currently attaching the images too large
    images_str = ""

    for image in sub_dir_data["images"]:
        images_str = images_str + f"""
        <div class="img_el">
            <a href={image.name}>
                <img src={image.name} class="sm_img">
            </a>
            <br>
            {image.name}
            {get_exif_data(image)}
        </div>"""

    return images_str


def get_exif_data(image): # TODO This works great for the timestamp, but isn't working at all for location
    print(f"Let's get exif data for image: {image.name}")
    date_time = exif.get_timestamp(image)
    loc = exif_to_location(image)
    return f"""
            <br>
            {date_time if date_time else ""}
            <br>
            {loc if loc else ""}"""


def exif_to_location(image):
    lat, long = exif.get_coordiantes(image)
    print(f"lat: {lat}, long: {long}")
    try:
        loc = exif.convert_to_location(lat, long)
        print(f"\tLOCATION: {loc}")
        city_state_country = f"{loc[0]}, {loc[1]} {loc[2]}"
        return city_state_country
    except:
        print("\tCouldn't get the location data...")
        return None


def main():
    print(index_image_dir_recursive(sys.argv[1]))



if __name__ == "__main__":
    main()