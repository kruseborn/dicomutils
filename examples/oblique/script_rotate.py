import os
import pydicom
import numpy
import glob
import uuid

def generate_uid():
    u=uuid.uuid4()
    i = 0
    for c in u.bytes:
        i *= 256
        i += ord(c)
    return "2.25.{}".format(i)

studyUid = generate_uid()

patientName = "Spock^^^^"

mrPath = "C:/git/python-notebook/MR_HFP/*.dcm"
mrPathOutPath = "C:/git/python-notebook/MR_HFP/out/"

patientId = "21231666"

def showImage(pixelData):
    %pylab notebook
    imshow(pixelData)
    
def readFiles(path):
    allDs = []
    dcmFiles = glob.glob(path)
    for file in dcmFiles:
        ds = pydicom.read_file(file)
        allDs.append({"ds":ds, "name":os.path.basename(file)})
    return allDs;

def changeImage(allDs, ):
    first = True
    seriesUid = generate_uid()
    for dsDict in allDs:
        ds = dsDict['ds']
        ds.ImageOrientationPatient[0] = 0.707106769
        ds.ImageOrientationPatient[1] = -0.707106769
        ds.ImageOrientationPatient[2] = 0.0
        ds.ImageOrientationPatient[3] = 0.707106769
        ds.ImageOrientationPatient[4] = 0.707106769
        ds.ImageOrientationPatient[5] = 0.0
        
        ds.ImagePositionPatient[0] = -22.0
        ds.ImagePositionPatient[1] = 25.0
        ds.PatientName = patientName
        ds.PatientID = patientId

        ds.StudyInstanceUID = studyUid;
        ds.SeriesInstanceUID = seriesUid
        ds.SOPInstanceUID = generate_uid()
        if first:
            #showImage(ds.pixel_array)
            print(ds)
            first = False
        
def saveImages(allDs, outPath):
    for dsDict in allDs:
        ds = dsDict['ds']
        ds.save_as(outPath + dsDict['name'])

mrDs = readFiles(mrPath)
changeImage(mrDs)
saveImages(mrDs, mrPathOutPath)
