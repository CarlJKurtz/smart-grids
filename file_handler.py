from config import *
from xml.dom import minidom
import xmltodict
from unitlineedit import UnitLineEdit
import PyQt5


def read_file(window, path):
    try:
        file = open(f'{path}', 'r')
        content = file.read()
        dict = xmltodict.parse(content)['root']

        file_version = dict['document-preferences']['@version']
        if file_version != APP_VERSION:
            window.throw_error(f'This file was saved in a different version of {APP_TITLE}.\n'
                               f'An error while loading this file might occur.')

        try:
            window.dpi = int(dict['document-preferences']['@dpi'])
            window.change_unit(dict['document-preferences']['@unit'])
            window.resolution_output.setText(f'{window.dpi} dpi')
            window.page_width_spinbox.setValue(float(dict['page']['@page-width']))
            window.page_height_spinbox.setValue(float(dict['page']['@page-height']))
            window.top_margin_spinbox.setValue(float(dict['page']['@top-margin']))
            window.bottom_margin_spinbox.setValue(float(dict['page']['@bottom-margin']))
            window.left_margin_spinbox.setValue(float(dict['page']['@left-margin']))
            window.right_margin_spinbox.setValue(float(dict['page']['@right-margin']))

            if dict['font']['@key'] in window.font_dict:
                window.font_dropdown.setCurrentText((dict['font']['@key']))
            else:
                font_name = dict['font']['@key']
                window.throw_error(f'The font {font_name} does not exist on your system.')

            window.font_size_spinbox.setValue(float(dict['font']['@size']))
            window.leading_spinbox.setValue(float(dict['font']['@leading']))

            if dict['vertical-alignment']['@upper-alignment'] == 'ascender':
                window.ascender_radio.setChecked(True)
            elif dict['vertical-alignment']['@upper-alignment'] == 'cap-height':
                window.cap_height_radio.setChecked(True)
            elif dict['vertical-alignment']['@upper-alignment'] == 'x-height':
                window.xheight_radio.setChecked(True)

            if dict['vertical-alignment']['@lower-alignment'] == 'baseline':
                window.baseline_radio.setChecked(True)
            elif dict['vertical-alignment']['@lower-alignment'] == 'descender':
                window.descender_radio.setChecked(True)

            window.rows_spinbox.setValue(int(dict['grid']['@rows']))
            window.lines_in_gutter_spinbox.setValue(int(dict['grid']['@gutterlines']))
            window.columns_spinbox.setValue(int(dict['grid']['@columns']))
            window.custom_gutter_spinbox.setValue(float(dict['grid']['@gutter']))

            if dict['grid']['@use_custom_gutter'] == 'True':
                window.use_custom_gutter_checkbox.setChecked(True)
            else:
                window.use_custom_gutter_checkbox.setChecked(False)

        except:
            pass

    except:
        window.throw_error(f'Oops!\n{APP_TITLE} can’t read this file.', icon=PyQt5.QtWidgets.QMessageBox.Critical)

    window.update()



def write_file(window, path):
    xml_content = write_xml_content(window)

    with open(f'{path}{FILE_TYPE}', 'w') as file:
        file.write(xml_content)


def write_xml_content(window):
    root = minidom.Document()
    xml = root.createElement('root')
    root.appendChild(xml)

    preferences_child = root.createElement('document-preferences')
    preferences_child.setAttribute('version', str(APP_VERSION))
    preferences_child.setAttribute('unit', str(UnitLineEdit.unit))
    preferences_child.setAttribute('dpi', str(window.dpi))
    xml.appendChild(preferences_child)

    page_child = root.createElement('page')
    page_child.setAttribute('page-width', str(window.page_width_spinbox.value()))
    page_child.setAttribute('page-height', str(window.page_height_spinbox.value()))
    page_child.setAttribute('top-margin', str(window.top_margin_spinbox.value()))
    page_child.setAttribute('bottom-margin', str(window.bottom_margin_spinbox.value()))
    page_child.setAttribute('left-margin', str(window.left_margin_spinbox.value()))
    page_child.setAttribute('right-margin', str(window.right_margin_spinbox.value()))
    xml.appendChild(page_child)

    font_child = root.createElement('font')
    font_child.setAttribute('key', window.font_dropdown.currentText())
    font_child.setAttribute('size', str(window.font_size_spinbox.value()))
    font_child.setAttribute('leading', str(window.leading_spinbox.value()))
    xml.appendChild(font_child)

    if window.ascender_radio.isChecked():
        upper_alignement = 'ascender'
    elif window.cap_height_radio.isChecked():
        upper_alignement = 'cap-height'
    elif window.xheight_radio.isChecked():
        upper_alignement = 'x-height'

    if window.baseline_radio.isChecked():
        lower_alignement = 'baseline'
    elif window.descender_radio.isChecked():
        lower_alignement = 'descender'

    alignment_child = root.createElement('vertical-alignment')
    alignment_child.setAttribute('upper-alignment', upper_alignement)
    alignment_child.setAttribute('lower-alignment', lower_alignement)
    xml.appendChild(alignment_child)

    grid_child = root.createElement('grid')
    grid_child.setAttribute('rows', str(window.rows_spinbox.value()))
    grid_child.setAttribute('gutterlines', str(window.lines_in_gutter_spinbox.value()))
    grid_child.setAttribute('columns', str(window.columns_spinbox.value()))
    grid_child.setAttribute('gutter', str(window.custom_gutter_spinbox.value()))

    if window.use_custom_gutter_checkbox.isChecked():
        use_custom_gutter = 'True'
    else:
        use_custom_gutter = 'False'
    grid_child.setAttribute('use_custom_gutter', use_custom_gutter)
    xml.appendChild(grid_child)

    xml_str = root.toprettyxml(indent="\t")

    return xml_str
