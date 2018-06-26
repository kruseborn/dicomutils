import shutil
try:
    shutil.rmtree("oblique_mr_x_z")
except:
    pass

import sys
sys.path.append("../../")

import builders
reload(builders)
import modules
reload(modules)
from builders import StudyBuilder

import os
if not os.path.exists("oblique_mr_x_z"):
    os.mkdir("oblique_mr_x_z")

def build_orientation(patient_position, column_direction, row_direction, frame_of_reference_uid = None):
    sb = StudyBuilder(patient_position=patient_position, patient_id="oblique_mr_x_z", patient_name="Amanda^Grayson^Mother^Of^Spock", patient_birthdate = "20121212")
    if frame_of_reference_uid != None:
        sb.current_study['FrameOfReferenceUID'] = frame_of_reference_uid

    print "building %s..." % (patient_position,)
    print "ct"
    ct = sb.build_mr(
        num_voxels=[7, 7, 7],
        voxel_size=[4, 4, 4],
        pixel_representation=0,
        row_direction=row_direction,
        column_direction=column_direction)
    ct.clear(stored_value = 0)
    ct.add_box(size = [4,4,4], center = [-12,-12,-12], stored_value = 100)
    ct.add_box(size = [4,4,4], center = [-12,-12,-8], stored_value = 200)
    ct.add_box(size = [4,4,4], center = [-12,-12,-4], stored_value = 300)
    ct.add_box(size = [4,4,4], center = [-12,-12, 0], stored_value = 400)
    ct.add_box(size = [4,4,4], center = [-12,-12, 4], stored_value = 500)
    ct.add_box(size = [4,4,4], center = [-12,-12, 8], stored_value = 600)
    ct.add_box(size = [4,4,4], center = [-12,-12, 12], stored_value = 700)

    ct.add_box(size = [4,4,4], center = [0,0,-12], stored_value = 450)
    ct.add_box(size = [4,4,4], center = [0,0,-8], stored_value = 450)
    ct.add_box(size = [4,4,4], center = [0,0,-4], stored_value = 450)
    ct.add_box(size = [4,4,4], center = [0,0, 0], stored_value = 450)
    ct.add_box(size = [4,4,4], center = [0,0, 4], stored_value = 450)
    ct.add_box(size = [4,4,4], center = [0,0, 8], stored_value = 450)
    ct.add_box(size = [4,4,4], center = [0,0, 12], stored_value = 450)

    ct.add_box(size = [4,4,4], center = [12,-12,-12], stored_value = 100)
    ct.add_box(size = [4,4,4], center = [12,-8, -12], stored_value = 200)
    ct.add_box(size = [4,4,4], center = [12,-4, -12], stored_value = 300)
    ct.add_box(size = [4,4,4], center = [12,-0, -12], stored_value = 400)
    ct.add_box(size = [4,4,4], center = [12, 4, -12], stored_value = 500)
    ct.add_box(size = [4,4,4], center = [12, 8, -12], stored_value = 600)
    ct.add_box(size = [4,4,4], center = [12, 12,-12], stored_value = 700)

    ct.build()

    return sb

orientations = [([0.7071067812, 0, 0.7071067812],[0,1,0])]
patientpositions = ['HFS']
sbs = []
FoR = None
for o in orientations:
    for p in patientpositions:
        sb = build_orientation(p, o[0], o[1], FoR)
        sbs.append(sb)
        FoR = sbs[0].current_study['FrameOfReferenceUID']
        d = "oblique_mr_x_z/" + p + "/" + "%s%s%s%s%s%s" % tuple(x for y in o for x in y)
        os.makedirs(d)
        sb.write(d)

