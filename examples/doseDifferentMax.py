import shutil
import numpy
try:
    shutil.rmtree("doseDifferentMax")
except:
    pass

import sys
sys.path.append("../")

import builders
reload(builders)
import modules
reload(modules)
from builders import StudyBuilder

import os
if not os.path.exists("doseDifferentMax"):
    os.mkdir("doseDifferentMax")

def build_orientation(patient_position, column_direction, row_direction, frame_of_reference_uid = None):
    sb = StudyBuilder(patient_position=patient_position, patient_id="doseDifferentMax", patient_name="doseDifferentMax", patient_birthdate = "20121212")
    if frame_of_reference_uid != None:
        sb.current_study['FrameOfReferenceUID'] = frame_of_reference_uid

    print "building %s..." % (patient_position,)
    print "ct"
    ct = sb.build_ct(
        num_voxels=[7, 7, 7],
        voxel_size=[4, 4, 4],
        pixel_representation=0,
        rescale_slope=1,
        rescale_intercept=-1024,
        row_direction=row_direction,
        column_direction=column_direction)
    ct.clear(real_value = -1000)
    ct.add_box(size = [4,4,4], center = [0,0,0], real_value = 0)
    ct.add_box(size = [20,4,4], center = [0,-8,-8], real_value = 0)
    ct.add_box(size = [4,20,4], center = [8,0,-8], real_value = 0)
    ct.add_box(size = [4,4,20], center = [8,8,0], real_value = 0)
    ct.add_sphere(radius = 4, center = [-8,-8,-8], real_value = 0)

    print "rtstruct"
    rtstruct = sb.build_structure_set(ct)
    rtstruct.add_external_box()
    rtstruct.add_box(size = [4,4,4], center = [0,0,0], name='CenterVoxel', interpreted_type='SITE')
    rtstruct.add_box(size = [20,4,4], center = [0,-8,-8], name='x=-8 to 8, y=z=-8', interpreted_type='SITE')
    rtstruct.add_box(size = [4,20,4], center = [8,0,-8], name='y=-8 to 8 x=8, z=-8', interpreted_type='SITE')
    rtstruct.add_box(size = [4,4,20], center = [8,8,0], name='z=-8 to 8, x=y=8', interpreted_type='SITE')
    rtstruct.add_sphere(radius=4, center = [-8,-8,-8], name='x=y=z=-8', interpreted_type='SITE')
    rtstruct.build()

    print "rtstruct 2 not connected to the plan"
    rtstruct2 = sb.build_structure_set(ct)
    rtstruct2.add_external_box()
    rtstruct2.add_sphere(radius=4, center = [0,0,0], name='center sphere', interpreted_type='SITE')
    rtstruct2.build()

    print "rtplan"
    rtplan = sb.build_static_plan(structure_set = rtstruct, sad=20)
    b1 = rtplan.build_beam(gantry_angle = 0, collimator_angle=30, meterset = 100)
    b1.conform_to_rectangle(4, 4, [0,0])
    b2 = rtplan.build_beam(gantry_angle = 120, meterset = 100)
    b2.conform_to_rectangle(4, 4, [4,4])
    rtplan.build()

    print "rtdose beam 1"
    rtdose1 = sb.build_dose(planbuilder = None,
        num_voxels=[7, 9, 5],
        voxel_size=[3, 1, 1],
        row_direction=row_direction,
        column_direction=column_direction)
    rtdose1.dose_grid_scaling = 0.01
    rtdose1.dose_summation_type = "BEAM"
    rtdose1.beam_number = 1

    rtdose1.add_box(size = [3,1,1], center = [0,-3, 0], stored_value = 100) 
    rtdose1.add_box(size = [3,1,1], center = [0, -2, 0], stored_value = 91) 
    rtdose1.add_box(size = [3,1,1], center = [0, -1, 0], stored_value = 81) 
    rtdose1.add_box(size = [3,1,1], center = [0,  0, 0], stored_value = 71) 
    rtdose1.add_box(size = [3,1,1], center = [0,  1, 0], stored_value = 61) 
    rtdose1.add_box(size = [3,1,1], center = [0,  2, 0], stored_value = 51) 
    rtdose1.add_box(size = [3,1,1], center = [0, 3, 0], stored_value = 0)     

    ############# second beam
    print "rtdose beam 2"
    rtdose2 = sb.build_dose(planbuilder = None,
        num_voxels=[7, 9, 5],
        voxel_size=[3, 1, 1],
        row_direction=row_direction,
        column_direction=column_direction)
    rtdose2.dose_grid_scaling = 0.01
    rtdose2.dose_summation_type = "BEAM"
    rtdose2.beam_number = 2

    rtdose2.add_box(size = [3,1,1], center = [-9,0, 0], stored_value = 100)
    rtdose2.add_box(size = [3,1,1], center = [-6, 0, 0], stored_value = 91)
    rtdose2.add_box(size = [3,1,1], center = [-3, 0, 0], stored_value = 81)
    rtdose2.add_box(size = [3,1,1], center = [0,  0, 0], stored_value = 71)
    rtdose2.add_box(size = [3,1,1], center = [3,  0, 0], stored_value = 61)
    rtdose2.add_box(size = [3,1,1], center = [6,  0, 0], stored_value = 51)
    rtdose2.add_box(size = [3,1,1], center = [9, 0, 0], stored_value = 0)

    ############# second plan
    print "rtdose plan dose"
    rtdosePlan = sb.build_dose(planbuilder = None,        
        num_voxels=[7, 9, 5],
        voxel_size=[3, 1, 1],
        row_direction=row_direction,
        column_direction=column_direction)
    rtdosePlan.dose_grid_scaling = 0.01
    rtdosePlan.dose_summation_type = "PLAN"
    rtdosePlan.beam_number = None

    rtdosePlan.pixel_array = numpy.add(rtdose2.pixel_array, rtdose1.pixel_array)

    return sb

##orientations = [([1,0,0], [0,1,0]),([-1,0,0], [0,-1,0]),([-1,0,0, [0,1,0]]),([1,0,0], [0,-1,0])]
##patientpositions = ['HFS','HFP','FFS','FFP','HFDR', 'HFDL', 'FFDR', 'FFDL']
orientations = [([-1,0,0], [0,-1,0])]
patientpositions = ['FFS']

sbs = []
FoR = None
for o in orientations:
    for p in patientpositions:
        sb = build_orientation(p, o[0], o[1], FoR)
        sbs.append(sb)
        FoR = sbs[0].current_study['FrameOfReferenceUID']
        d = "doseDifferentMax/" + p + "/" + "%s%s%s%s%s%s" % tuple(x for y in o for x in y)
        os.makedirs(d)
        sb.write(d)
