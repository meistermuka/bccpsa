import gphoto2 as gp
import os
import sys
import time

def get_config_value(value, camera, context):

    config_widget = gp.check_result(gp.gp_camera_get_config(camera, context))
    camera_widget_child = gp.check_result(gp.gp_widget_get_child_by_name(config_widget, value))
    config_value = gp.check_result(gp.gp_widget_get_value(camera_widget_child))

    return config_value

def capture_image(camera, context):
    print "Capturing Image"
    image_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE, context))
    timestamp = int(time.time())
    print "Captured at ", timestamp
    extension = image_path.name.split('.')[1]
    image_name = "TST_{}.".format(timestamp) + extension
    target_path = os.path.join('/tmp/bccpsa', image_name)
    print "Copying to ", target_path
    image_file = gp.check_result(gp.gp_camera_file_get(camera, image_path.folder, image_path.name, gp.GP_FILE_TYPE_NORMAL, context))
    gp.check_result(gp.gp_file_save(image_file, target_path))

#Used to get more information on the folders on the camera
def get_folder_contents(folder, camera, context):

    result = []

    for name, value in camera.folder_list_files(folder, context):
        result.append(os.path.join(folder, name))

    folders = []

    for name, value in camera.folder_list_folders(folder, context):
        folders.append(name)

    if folders:
        for name in folders:
            result.extend(get_folder_contents(os.path.join(folder, name),camera, context))

    return result


def main():

    #Initialize the camera
    context = gp.gp_context_new()
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera, context))

    #Get basic info from camera
    print "ISO: " + get_config_value("iso", camera, context)
    print "Shutter Speed: " + get_config_value("shutterspeed2", camera, context)
    print "Aperture: " + get_config_value("f-number", camera, context)

    #files = get_folder_contents("/", camera, context)

    capture_image(camera, context)

    gp.check_result(gp.gp_camera_exit(camera, context))




if __name__  == "__main__":
    sys.exit(main())
