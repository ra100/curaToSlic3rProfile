#!/usr/bin/env python2
import sys
import os
import argparse
from ConfigParser import SafeConfigParser


def max_fan_speed(i, out):
    if i.isdigit():
        return int(float(i) * 100)
    else:
        return 0


def fan_always_on(i, out):
    if int(i) == 1:
        return 1
    else:
        return 0


def min_fan_speed(i, out):
    if i == 'True':
        return out['max_fan_speed']
    else:
        return 0


def support_material_extruder(i, out):
    if i == 'Both':
        return 1
    else:
        return i


def support_material(i, out):
    if i != 'None':
        return 1
    else:
        return 0


def support_material_pattern(i, out):
    if i == 'Lines':
        return 'rectilinear'
    else:
        return 'rectilinear-grid'
    # options rectilinear, rectilinear-grid, honeycomb, pillars

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
        'default': 60}
    # TODO all other values
]


def getValue(profile, out, key):
    '''get source value, convert and save to out'''
    if key['src'] in profile.keys():
        if 'conv' in key.keys():
            o = key['conv'](profile[key['src']], out)
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
    out = SafeConfigParser()
    for k, v in slic3r.iteritems():
        out.set('', k, str(v))
    with open(slic3rFile, 'w') as cf:
        out.write(cf)
    print('Profile has been converted.')

if __name__ == "__main__":
    main()
