import gphoto2 as gp
import sys


def _lookup_widget(key, child):
    ret = gp.gp_widget_get_child_by_name(child, key)

    if ret < gp.GP_OK:
        ret = gp.gp_widget_get_child_by_label(child, key)

    return ret

def get_config_value_string(camera, key, value, context):
    #child = gp._widget
    child = gp.gp_camera_get_config(camera, context)
    if child < gp.GP_OK:
        print "camera_get_config failed: %d" + child

    #ret = _lookup_widget(child, key)
    #if ret < gp.GP_OK:
    #    print "lookup widget failed: %d" + ret

    ret = gp.gp_widget_get_value(value)
    if ret < gp.GP_OK:
        print "could not query widget value: %d" + ret


def main():
    context = gp.gp_context_new()
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera, context))

    #config = gp.check_result(gp.gp_camera_get_config(camera, context))

    #print config

    iso = ''

    ret = get_config_value_string(camera, "iso", iso, context)
    if ret < gp.GP_OK:
        print "Unable to get ISO: %d" + ret
    else:
        print "ISO is: " + iso

if __name__  == "__main__":
    sys.exit(main())