#
#    Copyright (C) 2010-2017 PyTRiP98 Developers.
#
#    This file is part of PyTRiP98.
#
#    PyTRiP98 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyTRiP98 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyTRiP98.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Auxiliary functions for handling Dicom data.
"""
import os
from pydicom import dcmread

def compare_dicom_key(dcm):
    """ Specifying the sorting key for CT images.
    """
    return float(dcm.ImagePositionPatient[2])


def read_dicom_dir(dicom_dir):
    """ Reads a directory with dicom files.
    Identifies each dicom file with .dcm suffix and returns a dict containing a dicom object.
    Dicom object may be "CT", "RTSTRUCT", "RTDOSE" or "RTPLAN".
    Corresponding keys for lookup are "images", "rtss", "rtdose" or "rtplan" respectively.
    CT objects are lists of images. They will be sorted by the position in patient given
    by the ImagePositionPatient[2] tag.

    :returns: A dict containing dicom objects and corresponding keys 'images','rtss','rtdose' or 'rtplan'.
    """
    if not os.path.isdir(dicom_dir):
        raise IOError("Directory {:s} does not exist".format(dicom_dir))

    # list of allowed DICOM file extensions names
    # all in lower case
    dicom_suffix = ('.dcm', '.ima', '.v2')

    data = {}
    _files = os.listdir(dicom_dir)
    for item in _files:
        if os.path.splitext(item)[1].lower() in dicom_suffix:
            # force reading even if no File Meta Information header is found
            dcm = dcmread(fp=os.path.join(dicom_dir, item), force=True)
            if dcm.Modality == "CT":
                if "images" not in data:
                    data["images"] = []
                data["images"].append(dcm)
            elif dcm.Modality == "RTSTRUCT":
                data["rtss"] = dcm
            elif dcm.Modality == "RTDOSE":
                data["rtdose"] = dcm
            elif dcm.Modality == "RTPLAN":
                data["rtplan"] = dcm
    if "images" in data:
        data["images"].sort(key=compare_dicom_key)
    return data
