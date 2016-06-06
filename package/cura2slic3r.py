#!/usr/bin/env python2
import sys
import os
import argparse
import collections
from ConfigParser import SafeConfigParser


def max_fan_speed(i, p, o):
    if i.isdigit():
        return int(float(i) * 100 / 255)
    else:
        return 0


def fan_always_on(i, p, o):
    if int(i) == 1:
        return 1
    else:
        return 0


def min_fan_speed(i, p, o):
    if i == 'True':
        return o['max_fan_speed']
    else:
        return 0


def support_material_extruder(i, p, o):
    if i == 'Both':
        return 1
    else:
        return i


def support_material(i, p, o):
    if i != 'None':
        return 1
    else:
        return 0


def support_material_pattern(i, p, o):
    if i == 'Lines':
        return 'rectilinear'
    else:
        return 'rectilinear-grid'
    # options rectilinear, rectilinear-grid, honeycomb, pillars


def to_percent(i, p, o):
    return str(i) + '%'


def skirts(i, p, o):
    if p['platform_adhesion'] == 'Skirt':
        return i
    else:
        return 0


def retract_speed(i, p, o):
    if p['retraction_enable'] == 'True':
        return i
    else:
        return 0


def raft_layers(i, p, o):
    if p['platform_adhesion'] == 'Raft':
        return i
    else:
        return 0


def brim_width(i, p, o):
    if p['platform_adhesion'] == 'Brim':
        return int(round(i * float(p['layer_height'])))
    else:
        return 0


def bottom_solid_layers(i, p, o):
    if i == 'True':
        thick = float(p['solid_layer_thickness'])
        height = float(p['layer_height'])
        return int(round(thick / height))
    else:
        return 0


def first_layer_height(i, p, o):
    return str(int(float(p['bottom_thickness']) / float(p['layer_height']) * 100)) + "%"


def top_solid_layers(i, p, o):
    if i == 'True':
        thick = float(p['solid_layer_thickness'])
        height = float(p['layer_height'])
        return int(round(thick / height))
    else:
        return 0


def bool_to_int(i, p, o):
    if i == 'True':
        return 1
    else:
        return 0


def max_print_speed(i, p, o):
    return int(float(i) * 2)


def min_print_speed(i, p, o):
    return int(float(i) / 2)


def extrusion_multiplier(i, p, o):
    return float(i) / 100


def bed_temperature(i, p, o):
    if i == 'True':
        return print_bed_temperature
    else:
        return 0


def bed_shape(i, p, o):
    return '0x0{0!s},{1!s}x{2!s},0x{2!s}'.format(p['machine_width'],
                                                 p['machine_depth'],
                                                 p['machine_height'])


def perimeters(i, p, o):
    perimeter_width = float(p['nozzle_size'])
    if (p['perimeter_extrusion_width'] != None):
        perimeter_width = float(p['perimeter_extrusion_width'])
    return int(round(float(i) / perimeter_width))


def extruder_offset(i, p, o):
    return '{0!s}x{1!s}'.format(i, p['extruder_offset_y1'])


def first_layer_speed(i, p, o):
    return str(int((float(i) / float(p['print_speed'])) * 100)) + "%"


c2s = [
    {'src': 'fan_speed_max', 'dest': 'max_fan_speed',
        'default': 100, 'conv': max_fan_speed},
    {'src': 'fan_speed', 'dest': 'fan_always_on',
        'default': 0, 'conv': fan_always_on},
    {'src': 'fan_enabled', 'dest': 'min_fan_speed',
        'default': 35, 'conv': min_fan_speed},
    {'src': 'fan_enabled', 'dest': 'bridge_fan_speed',
        'default': 100, 'conv': min_fan_speed},
    {'src': 'nozzle_size', 'dest': 'nozzle_diameter', 'default': 0.3},
    {'src': 'support_z_distance',
        'dest': 'support_material_contact_distance', 'default': 0.2},
    {'src': 'support_dual_extrusion', 'dest': 'support_material_extruder',
        'default': 1, 'conv': support_material_extruder},
    {'src': 'support', 'dest': 'support_material',
        'default': 0, 'conv': support_material},
    {'src': 'support_type', 'dest': 'support_material_pattern',
        'default': 'pillars', 'conv': support_material_pattern},
    {'src': 'support_xy_distance', 'dest': 'support_material_spacing',
        'default': 2.5},
    {'src': 'support_angle', 'dest': 'support_material_threshold',
        'default': 45},
    {'src': 'support_fill_rate', 'dest': 'support_material_speed',
        'default': 60},
    {'src': 'skirt_minimal_length', 'dest': 'min_skirt_length',
        'default': 0},
    {'src': 'skirt_line_count', 'dest': 'skirts',
        'default': 20, 'conv': skirts},
    {'src': 'skirt_gap', 'dest': 'skirt_distance',
        'default': 2},
    {'src': 'layer0_width_factor', 'dest': 'first_layer_extrusion_width',
        'default': '100%', 'conv': to_percent},
    {'src': 'retraction_speed', 'dest': 'retract_speed',
        'default': 40, 'conv': retract_speed},
    {'src': 'retraction_hop', 'dest': 'retract_lift',
        'default': 0},
    {'src': 'retraction_min_travel', 'dest': 'retract_before_travel',
        'default': 2},
    {'src': 'retraction_amount', 'dest': 'retract_length',
        'default': 2},
    {'src': 'travel_speed', 'dest': 'travel_speed',
        'default': 20},
    {'src': 'raft_surface_layers', 'dest': 'raft_layers',
        'default': 0, 'conv': raft_layers},
    {'src': 'inset0_speed', 'dest': 'infill_speed',
        'default': 0},
    {'src': 'fill_density', 'dest': 'fill_density',
        'default': '20%', 'conv': to_percent},
    {'src': 'fill_overlap', 'dest': 'infill_overlap',
        'default': '0', 'conv': to_percent},
    {'src': 'solid_bottom', 'dest': 'bottom_solid_layers',
        'default': 4, 'conv': bottom_solid_layers},
    {'src': 'solid_top', 'dest': 'top_solid_layers',
        'default': 4, 'conv': top_solid_layers},
    {'src': 'layer_height', 'dest': 'layer_height',
        'default': 0.15},
    {'src': 'ooze_shield', 'dest': 'ooze_prevention',
        'default': 0, 'conv': bool_to_int},
    {'src': 'filament_diameter', 'dest': 'filament_diameter',
        'default': 1.75},
    {'src': 'print_speed', 'dest': 'max_print_speed',
        'default': 80, 'conv': max_print_speed},
    {'src': 'min_print_speed', 'dest': 'min_print_speed',
        'default': 10, 'conv': min_print_speed},
    {'src': 'spiralize', 'dest': 'spiral_vase',
        'default': 0, 'conv': bool_to_int},
    {'src': 'brim_line_count', 'dest': 'brim_width',
        'default': 0, 'conv': brim_width},
    {'src': 'print_speed', 'dest': 'bridge_speed',
        'default': 60},
    {'src': 'print_speed', 'dest': 'perimeter_speed',
        'default': 0},
    {'src': 'filament_flow', 'dest': 'extrusion_multiplier',
        'default': 1, 'conv': extrusion_multiplier},
    {'src': 'insetx_speed', 'dest': 'solid_infill_speed',
        'default': 20},
    {'src': 'bottom_layer_speed', 'dest': 'first_layer_speed',
        'default': "60%", 'conv': first_layer_speed},
    {'src': 'bottom_thickness', 'dest': 'first_layer_height', 'default': '100%',
        'conv': first_layer_height},
    {'src': 'print_temperature', 'dest': 'temperature',
        'default': 0},
    {'src': 'has_heated_bed', 'dest': 'bed_temperature',
        'default': 60, 'conv': bed_temperature},
    {'src': 'machine_width', 'dest': 'bed_shape',
        'default': '0x0,200x0,200x200x0x200', 'conv': bed_shape},
    {'src': 'wall_thickness', 'dest': 'perimeters',
        'default': 3, 'conv': perimeters},
    {'src': 'extruder_offset_x1', 'dest': 'extruder_offset',
        'default': '0x0', 'conv': extruder_offset},
    # default not converted values
    {'src': 'NA', 'dest': 'wipe', 'default': 0},
    {'src': 'NA', 'dest': 'thin_walls', 'default': 1},
    {'src': 'NA', 'dest': 'support_material_enforce_layers', 'default': 0},
    {'src': 'NA', 'dest': 'support_material_extrusion_width', 'default': 0},
    {'src': 'NA', 'dest': 'support_material_interface_extruder', 'default': 1},
    {'src': 'NA', 'dest': 'support_material_interface_layers', 'default': 0},
    {'src': 'NA', 'dest': 'support_material_interface_spacing', 'default': 0},
    {'src': 'NA', 'dest': 'support_material_interface_speed', 'default': '100%'},
    {'src': 'NA', 'dest': 'support_material_angle', 'default': 0},
    {'src': 'NA', 'dest': 'skirt_height', 'default': 1},
    {'src': 'NA', 'dest': 'first_layer_acceleration', 'default': 0},
    {'src': 'NA', 'dest': 'first_layer_bed_temperature', 'default': 0},
    {'src': 'NA', 'dest': 'first_layer_temperature', 'default': 0},
    {'src': 'NA', 'dest': 'retract_layer_change', 'default': 1},
    {'src': 'NA', 'dest': 'retract_length_toolchange', 'default': 3},
    {'src': 'NA', 'dest': 'retract_restart_extra', 'default': 0},
    {'src': 'NA', 'dest': 'retract_restart_extra_toolchange', 'default': 0},
    {'src': 'NA', 'dest': 'disable_fan_first_layers', 'default': 1},
    {'src': 'NA', 'dest': 'fan_below_layer_time', 'default': 20},
    {'src': 'NA', 'dest': 'infill_acceleration', 'default': 0},
    {'src': 'NA', 'dest': 'infill_every_layers', 'default': 2},
    {'src': 'NA', 'dest': 'infill_extruder', 'default': 1},
    {'src': 'NA', 'dest': 'infill_extrusion_width', 'default': 0},
    {'src': 'NA', 'dest': 'infill_first', 'default': 0},
    {'src': 'NA', 'dest': 'infill_only_where_needed', 'default': 0},
    {'src': 'NA', 'dest': 'max_volumetric_speed', 'default': 0},
    {'src': 'NA', 'dest': 'octoprint_apikey', 'default': ''},
    {'src': 'NA', 'dest': 'octoprint_host', 'default': ''},
    {'src': 'NA', 'dest': 'notes', 'default': ''},
    {'src': 'NA', 'dest': 'top_infill_extrusion_width', 'default': 0},
    {'src': 'NA', 'dest': 'top_solid_infill_speed', 'default': "80%"},
    {'src': 'NA', 'dest': 'filament_colour', 'default': '#FFFFFF'},
    {'src': 'NA', 'dest': 'avoid_crossing_perimeters', 'default': 0},
    {'src': 'NA', 'dest': 'before_layer_gcode', 'default': ''},
    {'src': 'NA', 'dest': 'bridge_acceleration', 'default': 0},
    {'src': 'NA', 'dest': 'bridge_flow_ratio', 'default': 1},
    {'src': 'NA', 'dest': 'complete_objects', 'default': 0},
    {'src': 'NA', 'dest': 'default_acceleration', 'default': 0},
    {'src': 'NA', 'dest': 'dont_support_bridges', 'default': 1},
    {'src': 'NA', 'dest': 'duplicate_distance', 'default': 6},
    {'src': 'NA', 'dest': 'external_fill_pattern', 'default': 'rectilinear'},
    {'src': 'NA', 'dest': 'external_perimeter_speed', 'default': 0},
    {'src': 'NA', 'dest': 'external_perimeters_first', 'default': 0},
    {'src': 'NA', 'dest': 'extra_perimeters', 'default': 1},
    {'src': 'NA', 'dest': 'extruder_clearance_height', 'default': 20},
    {'src': 'NA', 'dest': 'extruder_clearance_radius', 'default': 20},
    {'src': 'NA', 'dest': 'extrusion_axis', 'default': 'E'},
    {'src': 'NA', 'dest': 'extrusion_width', 'default': 0},
    {'src': 'print_speed', 'dest': 'gap_fill_speed', 'default': 20},
    {'src': 'NA', 'dest': 'gcode_arcs', 'default': 0},
    {'src': 'NA', 'dest': 'gcode_comments', 'default': 0},
    {'src': 'NA', 'dest': 'gcode_flavor', 'default': 'reprap'},
    {'src': 'NA', 'dest': 'interface_shells', 'default': 0},
    {'src': 'NA', 'dest': 'layer_gcode', 'default': ''},
    {'src': 'NA', 'dest': 'only_retract_when_crossing_perimeters', 'default': 0},
    {'src': 'NA', 'dest': 'output_filename_format',
        'default': '[input_filename_base].gcode'},
    {'src': 'NA', 'dest': 'overhangs', 'default': 1},
    {'src': 'NA', 'dest': 'perimeter_acceleration', 'default': 0},
    {'src': 'NA', 'dest': 'perimeter_extruder', 'default': 1},
    {'src': 'NA', 'dest': 'perimeter_extrusion_width', 'default': 0},
    {'src': 'NA', 'dest': 'pressure_advance', 'default': 0},
    {'src': 'NA', 'dest': 'resolution', 'default': 0},
    {'src': 'NA', 'dest': 'seam_position', 'default': 'aligned'},
    {'src': 'NA', 'dest': 'slowdown_below_layer_time', 'default': 20},
    {'src': 'NA', 'dest': 'small_perimeter_speed', 'default': 0},
    {'src': 'NA', 'dest': 'solid_infill_below_area', 'default': 0},
    {'src': 'NA', 'dest': 'solid_infill_every_layers', 'default': 0},
    {'src': 'NA', 'dest': 'solid_infill_extruder', 'default': 1},
    {'src': 'NA', 'dest': 'solid_infill_extrusion_width', 'default': 0},
    {'src': 'NA', 'dest': 'standby_temperature_delta', 'default': '-5'},
    {'src': 'NA', 'dest': 'toolchange_gcode', 'default': ''},
    {'src': 'NA', 'dest': 'use_firmware_retraction', 'default': 0},
    {'src': 'NA', 'dest': 'use_relative_e_distances', 'default': 0},
    {'src': 'NA', 'dest': 'use_volumetric_e', 'default': 0},
    {'src': 'NA', 'dest': 'vibration_limit', 'default': 0},
    {'src': 'NA', 'dest': 'xy_size_compensation', 'default': 0},
    {'src': 'NA', 'dest': 'z_offset', 'default': 0}
]


def getValue(profile, out, key):
    '''get source value, convert and save to out'''
    if key['src'] in profile.keys():
        if 'conv' in key.keys():
            o = key['conv'](profile[key['src']], profile, out)
        else:
            o = profile[key['src']]
    else:
        o = key['default']
    out[key['dest']] = o


def convert(profile):
    '''Convert profile'''

    out = {}
    for o in c2s:
        getValue(profile, out, o)
    return out


def main():
    '''main function'''
    parser = argparse.ArgumentParser(
        description='''Convert Cura slicing profile to Slic3r''')
    parser.add_argument('cura', metavar='INPUT', type=str,
                        help='Cura input profile file')
    parser.add_argument('slic3r', metavar='OUTPUT', type=str, nargs='?',
                        help='Slic3r output profile file')
    args = parser.parse_args()
    curaFile = args.cura
    slic3rFile = args.slic3r

    cura = SafeConfigParser()
    cura.read(curaFile)
    slic3r = convert(cura._sections['profile'])
    srt = collections.OrderedDict(sorted(slic3r.items()))
    #When output is not specified, print profile to stdout
    if slic3rFile == None:
        print('# Slic3r profile converted from Cura {0!s}\n'.format(curaFile))
        for k in srt:
            print("{0!s} = {1!s}".format(k, slic3r[k]))
    else:
        with open(slic3rFile, 'w') as cf:
            cf.write(
                '# Slic3r profile converted from Cura {0!s}\n'.format(curaFile))
            for k in srt:
                cf.write("{0!s} = {1!s}\n".format(k, slic3r[k]))
        print('Profile has been converted.')

if __name__ == "__main__":
    main()
