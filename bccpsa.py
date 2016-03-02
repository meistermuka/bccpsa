import gphoto2 as gp
import sys

def get_config_value(value, camera, context):

    config_widget = gp.check_result(gp.gp_camera_get_config(camera, context))
    camera_widget_child = gp.check_result(gp.gp_widget_get_child_by_name(config_widget, value))
    config_value = gp.check_result(gp.gp_widget_get_value(camera_widget_child))

    return config_value

def main():

    #Initialize the camera
    context = gp.gp_context_new()
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera, context))

    #Get basic info from camera
    print "ISO: " + get_config_value("iso", camera, context)
    print "Shutter Speed: " + get_config_value("shutterspeed2", camera, context)
    print "Aperture: " + get_config_value("f-number", camera, context)


if __name__  == "__main__":
    sys.exit(main())
