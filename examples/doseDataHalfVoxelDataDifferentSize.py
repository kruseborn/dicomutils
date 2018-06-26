import shutil
import numpy
try:
    shutil.rmtree("doseSmallVoxelsOutsideImageData")
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
if not os.path.exists("doseSmallVoxelsOutsideImageData"):
    os.mkdir("doseSmallVoxelsOutsideImageData")

def build_orientation(patient_position, column_direction, row_direction, frame_of_reference_uid = None):
    sb = StudyBuilder(patient_position=patient_position, patient_id="doseSmallVoxelsOutsideImageData", patient_name="doseSmallVoxelsOutsideImageData", patient_birthdate = "20121212")
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

    print "rtplan"
    rtplan = sb.build_static_plan(structure_set = rtstruct, sad=20)
    b1 = rtplan.build_beam(gantry_angle = 0, collimator_angle=30, meterset = 100)
    b1.conform_to_rectangle(4, 4, [0,0])
    
    b2 = rtplan.build_beam(gantry_angle = 120, meterset = 100)
    b2.conform_to_rectangle(4, 4, [4,4])
    
    b3 = rtplan.build_beam(gantry_angle = 120, meterset = 100)
    b3.conform_to_rectangle(4, 4, [4,4])

    b4 = rtplan.build_beam(gantry_angle = 120, meterset = 100)
    b4.conform_to_rectangle(4, 4, [4,4])

    rtplan.build()

    print "rtdose beam 1"
    rtdose1 = sb.build_dose(planbuilder = None,
        num_voxels=[31, 31, 31],
        voxel_size=[1, 2, 1],
        row_direction=row_direction,
        column_direction=column_direction)
    rtdose1.dose_grid_scaling = 0.5
    rtdose1.dose_summation_type = "BEAM"
    rtdose1.beam_number = 1

    rtdose1.add_box(size = [1,1,1], center = [0, 14, 0], stored_value = 200) 
    rtdose1.add_box(size = [1,1,1], center = [0, 12, 0], stored_value = 180) 
    rtdose1.add_box(size = [1,1,1], center = [0, 10, 0], stored_value = 160) 
    rtdose1.add_box(size = [1,1,1], center = [0, 8, 0], stored_value = 140) 
    rtdose1.add_box(size = [1,1,1], center = [0, 6, 0], stored_value = 120) 
    rtdose1.add_box(size = [1,1,1], center = [0, 4, 0], stored_value = 110) 
    rtdose1.add_box(size = [1,1,1], center = [0, 2, 0], stored_value = 105) 
    rtdose1.add_box(size = [1,1,1], center = [0, 0, 0], stored_value = 100) 

    rtdose1.add_box(size = [1,1,1], center = [0, -14, 0], stored_value = 200) 
    rtdose1.add_box(size = [1,1,1], center = [0, -12, 0], stored_value = 180) 
    rtdose1.add_box(size = [1,1,1], center = [0, -10, 0], stored_value = 160) 
    rtdose1.add_box(size = [1,1,1], center = [0, -8, 0], stored_value = 140) 
    rtdose1.add_box(size = [1,1,1], center = [0, -6, 0], stored_value = 120) 
    rtdose1.add_box(size = [1,1,1], center = [0, -4, 0], stored_value = 110) 
    rtdose1.add_box(size = [1,1,1], center = [0, -2, 0], stored_value = 105) 
    rtdose1.add_box(size = [1,1,1], center = [0, 0, 0], stored_value = 100) 

    ############# second beam
    print "rtdose beam 2"
    rtdose2 = sb.build_dose(planbuilder = None,
        num_voxels=[31, 31, 31],
        voxel_size=[1, 2, 1],
        row_direction=row_direction,
        column_direction=column_direction)
    rtdose2.dose_grid_scaling = 0.5
    rtdose2.dose_summation_type = "BEAM"
    rtdose2.beam_number = 2
    
    rtdose2.add_box(size = [1,1,1], center = [14, 0, 0], stored_value = 200) 
    rtdose2.add_box(size = [1,1,1], center = [12, 0, 0], stored_value = 180) 
    rtdose2.add_box(size = [1,1,1], center = [10, 0, 0], stored_value = 160) 
    rtdose2.add_box(size = [1,1,1], center = [8,  0, 0], stored_value = 140) 
    rtdose2.add_box(size = [1,1,1], center = [6,  0, 0], stored_value = 120) 
    rtdose2.add_box(size = [1,1,1], center = [4,  0, 0], stored_value = 110) 
    rtdose2.add_box(size = [1,1,1], center = [2,  0, 0], stored_value = 105) 
    rtdose2.add_box(size = [1,1,1], center = [0,  0, 0], stored_value = 100) 

    rtdose2.add_box(size = [1,1,1], center = [-14, 0, 0], stored_value = 200) 
    rtdose2.add_box(size = [1,1,1], center = [-12, 0, 0], stored_value = 180) 
    rtdose2.add_box(size = [1,1,1], center = [-10, 0, 0], stored_value = 160) 
    rtdose2.add_box(size = [1,1,1], center = [-8,  0, 0], stored_value = 140) 
    rtdose2.add_box(size = [1,1,1], center = [-6,  0, 0], stored_value = 120) 
    rtdose2.add_box(size = [1,1,1], center = [-4,  0, 0], stored_value = 110) 
    rtdose2.add_box(size = [1,1,1], center = [-2,  0, 0], stored_value = 105) 
    rtdose2.add_box(size = [1,1,1], center = [ 0,  0, 0], stored_value = 100) 


    ############# third beam
    print "rtdose beam 3"
    rtdose3 = sb.build_dose(planbuilder = None,
        num_voxels=[31, 31, 31],
        voxel_size=[1, 2, 1],
        row_direction=row_direction,
        column_direction=column_direction)
    rtdose3.dose_grid_scaling = 0.5
    rtdose3.dose_summation_type = "BEAM"
    rtdose3.beam_number = 3
    
    rtdose3.add_box(size = [1,1,1], center = [14, 0, -12], stored_value = 200) 
    rtdose3.add_box(size = [1,1,1], center = [12, 0, -12], stored_value = 180) 
    rtdose3.add_box(size = [1,1,1], center = [10, 0, -12], stored_value = 160) 
    rtdose3.add_box(size = [1,1,1], center = [8,  0, -12], stored_value = 140) 
    rtdose3.add_box(size = [1,1,1], center = [6,  0, -12], stored_value = 120) 
    rtdose3.add_box(size = [1,1,1], center = [4,  0, -12], stored_value = 110) 
    rtdose3.add_box(size = [1,1,1], center = [2,  0, -12], stored_value = 105) 
    rtdose3.add_box(size = [1,1,1], center = [0,  0, -12], stored_value = 100) 

    rtdose3.add_box(size = [1,1,1], center = [-14, 0, -12], stored_value = 200) 
    rtdose3.add_box(size = [1,1,1], center = [-12, 0, -12], stored_value = 180) 
    rtdose3.add_box(size = [1,1,1], center = [-10, 0, -12], stored_value = 160) 
    rtdose3.add_box(size = [1,1,1], center = [-8,  0, -12], stored_value = 140) 
    rtdose3.add_box(size = [1,1,1], center = [-6,  0, -12], stored_value = 120) 
    rtdose3.add_box(size = [1,1,1], center = [-4,  0, -12], stored_value = 110) 
    rtdose3.add_box(size = [1,1,1], center = [-2,  0, -12], stored_value = 105) 
    rtdose3.add_box(size = [1,1,1], center = [ 0,  0, -12], stored_value = 100) 

    ############# fourth beam
    print "rtdose beam 4"
    rtdose4 = sb.build_dose(planbuilder = None,
        num_voxels=[31, 31, 31],
        voxel_size=[1, 2, 1],
        row_direction=row_direction,
        column_direction=column_direction)
    rtdose4.dose_grid_scaling = 0.5
    rtdose4.dose_summation_type = "BEAM"
    rtdose4.beam_number = 4
    
    rtdose4.add_box(size = [1,1,1], center = [14, 0, 12], stored_value = 200) 
    rtdose4.add_box(size = [1,1,1], center = [12, 0, 12], stored_value = 180) 
    rtdose4.add_box(size = [1,1,1], center = [10, 0, 12], stored_value = 160) 
    rtdose4.add_box(size = [1,1,1], center = [8,  0, 12], stored_value = 140) 
    rtdose4.add_box(size = [1,1,1], center = [6,  0, 12], stored_value = 120) 
    rtdose4.add_box(size = [1,1,1], center = [4,  0, 12], stored_value = 110) 
    rtdose4.add_box(size = [1,1,1], center = [2,  0, 12], stored_value = 105) 
    rtdose4.add_box(size = [1,1,1], center = [0,  0, 12], stored_value = 100) 

    rtdose4.add_box(size = [1,1,1], center = [-14, 0, 12], stored_value = 200) 
    rtdose4.add_box(size = [1,1,1], center = [-12, 0, 12], stored_value = 180) 
    rtdose4.add_box(size = [1,1,1], center = [-10, 0, 12], stored_value = 160) 
    rtdose4.add_box(size = [1,1,1], center = [-8,  0, 12], stored_value = 140) 
    rtdose4.add_box(size = [1,1,1], center = [-6,  0, 12], stored_value = 120) 
    rtdose4.add_box(size = [1,1,1], center = [-4,  0, 12], stored_value = 110) 
    rtdose4.add_box(size = [1,1,1], center = [-2,  0, 12], stored_value = 105) 
    rtdose4.add_box(size = [1,1,1], center = [ 0,  0, 12], stored_value = 100) 

    ############# second plan
    print "rtdose plan dose"
    rtdosePlan = sb.build_dose(planbuilder = None,
        num_voxels=[31, 31, 31],
        voxel_size=[1, 2, 1],
        row_direction=row_direction,
        column_direction=column_direction)
    rtdosePlan.dose_grid_scaling = 0.5
    rtdosePlan.dose_summation_type = "PLAN"
    rtdosePlan.beam_number = None

    rtdosePlan.pixel_array = numpy.add(rtdose2.pixel_array, rtdose1.pixel_array)
    rtdosePlan.pixel_array = numpy.add(rtdose3.pixel_array, rtdosePlan.pixel_array)
    rtdosePlan.pixel_array = numpy.add(rtdose4.pixel_array, rtdosePlan.pixel_array)

    return sb

##orientations = [([1,0,0], [0,1,0]),([-1,0,0], [0,-1,0]),([-1,0,0, [0,1,0]]),([1,0,0], [0,-1,0])]
##patientpositions = ['HFS','HFP','FFS','FFP','HFDR', 'HFDL', 'FFDR', 'FFDL']
orientations = [([1,0,0], [0,1,0])]
patientpositions = ['HFS']

sbs = []
FoR = None
for o in orientations:
    for p in patientpositions:
        sb = build_orientation(p, o[0], o[1], FoR)
        sbs.append(sb)
        FoR = sbs[0].current_study['FrameOfReferenceUID']
        d = "doseSmallVoxelsOutsideImageData/" + p + "/" + "%s%s%s%s%s%s" % tuple(x for y in o for x in y)
        os.makedirs(d)
        sb.write(d)
