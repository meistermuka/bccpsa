import gphoto2 as gp
import sys

def main():
    context = gp.gp_context_new()
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera, context))
    
    # Get config widget: this returns a child to be used...
    config_widget = gp.check_result(gp.gp_camera_get_config(camera, context))

    # Get all children
    children_count = gp.check_result(gp.gp_widget_count_children(config_widget))
    if children_count < 1:
        print "No children!"
    
    # Cycling through all available children and printing their names. Hope this works!
    for n in range(children_count):
        child = gp.check_result(gp.gp_widget_get_child(config_widget, n))
        name = gp.check_result(gp.gp_widget_get_name(child))
        print name
    
    #print config

    #iso = ''

    #ret = get_config_value_string(camera, "iso", iso, context)
    #if ret < gp.GP_OK:
    #    print "Unable to get ISO: %d" + ret
    #else:
    #    print "ISO is: " + iso

if __name__  == "__main__":
    sys.exit(main())
