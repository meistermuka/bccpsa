import gphoto2 as gp
import os
import sys
import time
from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from bccp_helper import ISO_CONSTANTS, SHUTTER_SPEED_CONSTANTS, APERTURE_CONSTANTS

app = Flask(__name__)
app.config.from_object(__name__)

context = gp.gp_context_new()
camera = gp.check_result(gp.gp_camera_new())
gp.check_result(gp.gp_camera_init(camera, context))


def get_config_value(key, camera, context):
    config_widget = gp.check_result(gp.gp_camera_get_config(camera, context))
    camera_widget_child = gp.check_result(gp.gp_widget_get_child_by_name(config_widget, key))
    config_value = gp.check_result(gp.gp_widget_get_value(camera_widget_child))
    return config_value

def set_config_value(key, value, camera, context):
    config_widget = gp.check_result(gp.gp_camera_get_config(camera, context))
    camera_widget_child = gp.check_result(gp.gp_widget_get_child_by_name(config_widget, key))
    gp.check_result(gp.gp_widget_set_value(camera_widget_child, value))
    gp.check_result(gp.gp_camera_set_config(camera, config_widget, context))

def _capture_image(camera, context, settings):
    print "Capturing Image"
    if settings:
        set_iso(str(ISO_CONSTANTS[settings['iso']]), camera, context)
        set_aperture(APERTURE_CONSTANTS[settings['f-number']], camera, context)
        set_shutterspeed(SHUTTER_SPEED_CONSTANTS[settings["shutterspeed2"]], camera, context)
    # Image being captured and stored on camera
    image_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE, context))
    # Grabbing timestamp for unique file name
    timestamp = int(time.time())
    extension = image_path.name.split('.')[1]
    image_name = "TST_{}.".format(timestamp) + extension
    target_path = os.path.join(os.getcwd()+'/images', image_name)
    # "Grunt" work to move the file off camera
    image_file = gp.check_result(gp.gp_camera_file_get(camera, image_path.folder, image_path.name, gp.GP_FILE_TYPE_NORMAL, context))
    gp.check_result(gp.gp_file_save(image_file, target_path))

def _get_folder_contents(folder, camera, context):
    result = []
    folders = []

    for name, value in camera.folder_list_files(folder, context):
        result.append(os.path.join(folder, name))

    for name, value in camera.folder_list_folders(folder, context):
        folders.append(name)

    if folders:
        for name in folders:
            result.extend(_get_folder_contents(os.path.join(folder, name),camera, context))
    else:
        print "No folders to print"

    return result

@app.route('/')
def basic_info():
    init_string = "ISO: " + get_iso(camera, context) + " <br>Shutter Speed: " + get_shutterspeed(camera, context) + "<br>Aperture: " + get_aperture(camera, context)
    return init_string
    #gp.check_result(gp.gp_camera_exit(camera, context))

@app.route('/process_capture', methods=['POST'])
def process_capture_image():
    basic_settings = {"iso": request.form['asa'], "shutterspeed2": request.form['shutterspeed'], "f-number": request.form['aperture']}
    print basic_settings
    print "Aperture: ", APERTURE_CONSTANTS[basic_settings['f-number']]
    print "ISO: ", ISO_CONSTANTS[basic_settings['iso']]
    print "SHUTTER: ", SHUTTER_SPEED_CONSTANTS[basic_settings["shutterspeed2"]]
    print "Going to capture image..."
    _capture_image(camera, context, basic_settings)
    return redirect(url_for('captured_images'))
    #return request.form['asa'] + "<br>" + request.form['shutterspeed'] + "<br>" + request.form['aperture']


@app.route('/captured_images')
def captured_images():
    target_folder = os.getcwd()+'/images'
    list_of_files = os.listdir(target_folder)
    return render_template('captured_images.html', list_of_files=list_of_files)

@app.route('/capture')
def capture():
    iso = get_iso(camera, context)
    fstop = get_aperture(camera, context)
    shutterspeed = get_shutterspeed(camera, context)
    return render_template('image_capture.html', iso_current=int(iso),
                           fstop_current=fstop,
                           shutterspeed_current=shutterspeed,
                           ISOS_SORTED=sorted(ISO_CONSTANTS, key=ISO_CONSTANTS.__getitem__),
                           ISOS=ISO_CONSTANTS,
                           FSTOPS=APERTURE_CONSTANTS,
                           SHUTTERS=SHUTTER_SPEED_CONSTANTS)

def get_iso(camera, context):
    return get_config_value("iso", camera, context)

def set_iso(value, camera, context):
    set_config_value("iso", value, camera, context)

def get_shutterspeed(camera, context):
    return get_config_value("shutterspeed2", camera, context)

def set_shutterspeed(value, camera, context):
    set_config_value("shutterspeed2", value, camera, context)

def get_aperture(camera, context):
    return get_config_value("f-number", camera, context)

def set_aperture(value, camera, context):
    set_config_value("f-number", value, camera, context)

@app.route('/folder')
def folder_contents():
    print "In FOLDER"
    folder = '/'
    return render_template('show_folder_contents.html', files=_get_folder_contents(folder, camera, context))


if __name__  == "__main__":
    app.run(debug=True)
    #sys.exit(main())
