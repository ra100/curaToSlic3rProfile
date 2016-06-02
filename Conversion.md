# Cura to Slic3r profile conversion

> this is assumed conversion pair table for converting Cura profile to Slic3r

Slic3r [PrintConfig.cpp](https://github.com/alexrj/Slic3r/blob/c12ccd8357cd3464e8b01273861f50acf14c5389/xs/src/libslic3r/PrintConfig.cpp)

## Conversion

| Slic3r                            | Cura                                                                 | example values                                                | notes     |
| --------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------- | --------- |
| max_fan_speed                     | fan_speed_max\*100                                                   | 1 -> 100                                                      |           |
| fan_always_on                     | (fan_speed) ? 1 : 0                                                  | False -> 0                                                    |           |
| min_fan_speed                     | (fan_enabled) ? 100 : 0                                              | True -> 100                                                   |           |
| bridge_fan_speed                  | (fan_enabled) ? 100 : 0                                              | True -> 100                                                   |           |
| nozzle_diameter                   | nozzle_size                                                          | 0.35                                                          |           |
| support_material_contact_distance | support_z_distance                                                   | 0.15                                                          |           |
| support_material_extruder         | (support_dual_extrusion == Both) ? 1 : 0                             | Both -> 1                                                     |           |
| support_material                  | (support != None) 1 : 0                                              | Everywhere -> 1                                               |           |
| support_material_pattern          | (support_type == Lines) ? rectilinear : rectilinear-grid             | Lines -> rectilinear / rectilinear-grid / honeycomb / pillars |           |
| support_material_spacing          | support_xy_distance                                                  | 0.7                                                           |           |
| support_material_threshold        | support_angle                                                        | 0 - 90                                                        |           |
| support_material_speed            | support_fill_rate                                                    | 20.0                                                          |           |
| min_skirt_length                  | skirt_minimal_length                                                 | 0                                                             |           |
| skirts                            | (platform_adhesion == Skirt) ? skirt_line_count : 0                  | 20                                                            |           |
| skirt_distance                    | skirt_gap                                                            | 2                                                             |           |
| first_layer_extrusion_width       | layer0_width_factor %                                                | 100.0 -> 100%                                                 |           |
| retract_speed                     | (retraction_enable) ? retraction_speed : 0                           | 25                                                            |           |
| retract_lift                      | retraction_hop                                                       | 0.1                                                           |           |
| retract_before_travel             | retraction_min_travel                                                | 1.5                                                           |           |
| retract_length                    | retraction_amount                                                    | 2.4                                                           |           |
| travel_speed                      | travel_speed                                                         | 20                                                            |           |
| raft_layers                       | (platform_adhesion == Raft) : raft_surface_layers : 0                | 2                                                             |           |
| infill_speed                      | inset0_speed                                                         | 16                                                            | 0 - auto  |
| fill_density                      | fill_density %                                                       | 8.75 -> 8.75%                                                 |           |
| infill_overlap                    | fill_overlap %                                                       | 0 -> 0%                                                       |           |
| bottom_solid_layers               | (solid_bottom) ? int(bottom_thickness / layer_height) : 0            | 4                                                             |           |
| layer_height                      | layer_height                                                         | 0.15                                                          |           |
| ooze_prevention                   | ooze_shield ? 1 : 0                                                  |                                                               |           |
| filament_diameter                 | filament_diameter                                                    | 1.75                                                          |           |
| max_print_speed                   | print_speed \* 2                                                     | 40                                                            |           |
| min_print_speed                   | print_speed / 2                                                      | 10                                                            |           |
| top_solid_layers                  | (solid_top) ? int(solid_layer_thickness / layer_height) : 0          | 4                                                             |           |
| spiral_vase                       | (spiralize) ? 1 : 0                                                  | 0                                                             |           |
| brim_width                        | (platform_adhesion == Brim) ? brim_line_count \* 0.35 : 0            | 5                                                             | in mm     |
| end_gcode                         | end.gcode                                                            |                                                               |           |
| bridge_speed                      | print_speed                                                          | 20                                                            |           |
| perimeter_speed                   | print_speed                                                          | 20                                                            | 0 - auto  |
| extrusion_multiplier              | filament_flow / 100                                                  | 1                                                             | 0.9 - 1.1 |
| solid_infill_speed                | insetx_speed                                                         | 18                                                            | ms/s or % |
| first_layer_speed                 | inset0_speed                                                         | 16                                                            | ms/s or % |
| start_gcode                       | start.gcode                                                          |                                                               |           |
| temperature                       | print_temperature                                                    | 0                                                             |           |
| bed_temperature                   | (has_heated_bed) ? print_bed_temperature : 0                         | 60                                                            |           |
| bed_shape                         | 0x0, machine_widthx0, machine_depthxmachine_height, 0xmachine_height |                                                               | not used  |
| perimeters                        | int(wall_thickness / layer_height)                                   | 3                                                             |           |
| extruder_offset                   | extruder_offset_x1xextruder_offset_y1                                | 0x0                                                           |           |

## Slic3r keys not in Cura

| key                                   | value                            | notes                                                                        |
| ------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------- |
| wipe                                  | 0                                | 0/1                                                                          |
| thin_walls                            | 1                                | 0/1                                                                          |
| support_material_enforce_layers       | 0                                |                                                                              |
| support_material_extrusion_width      | 0                                | float or %                                                                   |
| support_material_interface_extruder   | 1                                |                                                                              |
| support_material_interface_layers     | 0                                |                                                                              |
| support_material_interface_spacing    | 0                                | mm                                                                           |
| support_material_interface_speed      | 50%                              | float or %                                                                   |
| support_material_angle                | 45                               | 0 - 359                                                                      |
| skirt_height                          | 1                                | layers                                                                       |
| first_layer_acceleration              | 0                                | ms/s^2                                                                       |
| first_layer_bed_temperature           | 0                                |                                                                              |
| first_layer_height                    | 100%                             | mm or %                                                                      |
| first_layer_speed                     | 40%                              | mm/s or %                                                                    |
| first_layer_temperature               | 0                                |                                                                              |
| retract_layer_change                  | 1                                |                                                                              |
| retract_length_toolchange             | 3                                |                                                                              |
| retract_restart_extra                 | 0                                | rarely needed                                                                |
| retract_restart_extra_toolchange      | 0                                | rarely needed                                                                |
| disable_fan_first_layers              | 1                                |                                                                              |
| fan_below_layer_time                  | 20                               |                                                                              |
| infill_acceleration                   | 0                                |                                                                              |
| infill_every_layers                   | 2                                |                                                                              |
| infill_extruder                       | 1                                |                                                                              |
| infill_extrusion_width                | 0                                | mm or %                                                                      |
| infill_first                          | 0                                |                                                                              |
| infill_only_where_needed              | 0                                |                                                                              |
| max_volumetric_speed                  | 0                                |                                                                              |
| octoprint_apikey                      |                                  |                                                                              |
| octoprint_host                        |                                  |                                                                              |
| notes                                 |                                  |                                                                              |
| top_infill_extrusion_width            | 0                                | mm or %                                                                      |
| top_solid_infill_speed                | 80%                              | mm/s or %                                                                    |
| filament_colour                       | #FFFFFF                          |                                                                              |
| avoid_crossing_perimeters             | 0                                |                                                                              |
| before_layer_gcode                    |                                  |                                                                              |
| bridge_acceleration                   | 0                                |                                                                              |
| bridge_flow_ratio                     | 1                                |                                                                              |
| complete_objects                      | 0                                |                                                                              |
| default_acceleration                  | 0                                |                                                                              |
| dont_support_bridges                  | 1                                |                                                                              |
| duplicate_distance                    | 6                                |                                                                              |
| external_fill_pattern                 | rectilinear                      | rectilinear / concentric / hilbertcurve / archimedeanchords / octagramspiral |
| external_perimeter_extrusion_width    | 0                                | mm or %                                                                      |
| external_perimeter_speed              | 0                                | mm/s or %                                                                    |
| external_perimeters_first             | 0                                |                                                                              |
| extra_perimeters                      | 1                                |                                                                              |
| extruder_clearance_height             | 5                                | mm                                                                           |
| extruder_clearance_radius             | 20                               | mm                                                                           |
| extrusion_axis                        | E                                |                                                                              |
| extrusion_width                       | 0                                |                                                                              |
| gap_fill_speed                        | print_speed                      |                                                                              |
| gcode_arcs                            | 0                                |                                                                              |
| gcode_comments                        | 0                                |                                                                              |
| gcode_flavor                          | reprap                           |                                                                              |
| interface_shells                      | 0                                |                                                                              |
| layer_gcode                           |                                  |                                                                              |
| only_retract_when_crossing_perimeters | 0                                |                                                                              |
| output_filename_format                | [input_filename_base]\_M3D.gcode |                                                                              |
| overhangs                             | 1                                |                                                                              |
| perimeter_acceleration                | 0                                |                                                                              |
| perimeter_extruder                    | 1                                |                                                                              |
| perimeter_extrusion_width             | 0                                |                                                                              |
| pressure_advance                      | 0                                |                                                                              |
| resolution                            | 0                                | in mm                                                                        |
| seam_position                         | aligned                          | nearest / random / aligned                                                   |
| slowdown_below_layer_time             | 20                               | s                                                                            |
| small_perimeter_speed                 | 0                                | mm/s or %                                                                    |
| solid_infill_below_area               | 0                                | mm^2                                                                         |
| solid_infill_every_layers             | 0                                |                                                                              |
| solid_infill_extruder                 | 1                                |                                                                              |
| solid_infill_extrusion_width          | 0                                |                                                                              |
| standby_temperature_delta             | -5                               |                                                                              |
| threads                               | 4                                | parellelize slicing process                                                  |
| toolchange_gcode                      |                                  |                                                                              |
| use_firmware_retraction               | 0                                |                                                                              |
| use_relative_e_distances              | 0                                |                                                                              |
| use_volumetric_e                      | 0                                |                                                                              |
| vibration_limit                       | 0                                | Hz                                                                           |
| xy_size_compensation                  | 0                                | mm                                                                           |
| z_offset                              | 0                                | mm                                                                           |

## Keys in Cura not in Slic3r

| key                              | value  | notes                           |
| -------------------------------- | ------ | ------------------------------- |
| wipe_tower_volume                | 0.0    |                                 |
| fix_horrible_union_all_type_a    | False  |                                 |
| support_end.gcode                |        |                                 |
| support_start.gcode              |        |                                 |
| overlap_dual                     |        |                                 |
| cool_min_layer_time              | False  |                                 |
| cool_end.gcode                   |        |                                 |
| cool_min_feedrate                | 12     |                                 |
| cool_head_lift                   | True   |                                 |
| cool_start.gcode                 |        |                                 |
| retraction_dual_amount           | 14.5   |                                 |
| retraction_minimal_extrusion     | 0.1    |                                 |
| retraction_combing               | All    |                                 |
| raft_line_spacing                | 2.0    |                                 |
| raft_interface_thickness         | 0.2    |                                 |
| raft_base_thickness              | 0.4    |                                 |
| raft_airgap                      | 0.35   |                                 |
| raft_margin                      | 2.0    |                                 |
| raft_base_linewidth              | 2.5    |                                 |
| raft_interface_linewidth         | 0.5    |                                 |
| fan_full_height                  | 0.451  | maybe add to extruder clearance |
| simple_mode                      | False  |                                 |
| filament_diameter2               | 0.0    |                                 |
| filament_diameter3               | 0.0    |                                 |
| filament_diameter4               | 0.0    |                                 |
| filament_flow                    | 100    |                                 |
| fix_horrible_union_all_type_b    | False  |                                 |
| object_sink                      | False  |                                 |
| fix_horrible_extensive_stitching | False  |                                 |
| fix_horrible_use_open_bits       | False  |                                 |
| replace.csv                      |        |                                 |
| postswitchextruder.gcode         |        |                                 |
| preswitchextruder.gcode          |        |                                 |
| extruder_amount                  | 1      |                                 |
| machine_center_is_zero           | False  |                                 |
| machine_shape                    | Square |                                 |
