#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import code
import nibabel as nib
import logging

from optparse import OptionParser
from StringIO import StringIO
from numpy import ndenumerate


log = logging.getLogger('nifti1_4d_to_geo.py')



def export_frame(frame, scale, path):
    geo = StringIO()

    geo.write("""PGEOMETRY V5
NPoints %d NPrims 0
NPointGroups 0 NPrimGroups 0
NPointAttrib 1 NVertexAttrib 0 NPrimAttrib 0 NAttrib 1
PointAttrib
value 1 int 0
""" % frame.size)


    for (x, y, z), value in ndenumerate(frame):
        geo.write("%d %d %d 1 (%d)\n" % (x * scale[0], y * scale[1], z * scale[2], value))

    geo.write("""DetailAttrib
varmap 1 index 1 "value -> value"
 (0)
beginExtra
endExtra
""")

    log.debug("Writing: %s", path)
    geo_file = open(path, "w")
    geo_file.write(geo.getvalue())
    log.debug("OK");
    


def nifti1_4d_to_geo(nii_path, padding):
    log.info(nii_path)

    valid_extension_list = [
        ".nii",
        ".nii.gz",
        ]
    geo_path = None
    for extension in valid_extension_list:
        if nii_path.endswith(extension):
            geo_path = "%s.%%0%dd.geo" % (nii_path[:-len(extension)], padding)
            break
    else:
        log.error("%s: does not end in .nii or .nii.gz. Skipping.", nii_path)
        return

    log.debug(geo_path)

    nii = nib.load(nii_path)

    data = nii.get_data()
    header = nii.get_header()

    scale = (1, 1, 1)
    duration = None

    try:
        pixdim = header["pixdim"]
        assert pixdim.size == 8
        scale = (float(pixdim[1]), float(pixdim[2]), float(pixdim[3]))
        duration = float(pixdim[4])
    except:
        pass

    space_unit, time_unit = ("", "")
    try:
        space_unit, time_unit = header.get_xyzt_units()
    except:
        pass

    log.info(u"Scale: %s%s" % (u"⨯".join([str(i) for i in scale]), space_unit))
    if (duration):
        log.info("Frame duration: %s%s" % (duration, time_unit))

    if data.ndim != 4:
        log.error("%s: does not contain 4-dimensional data. Skipping.", nii_path)
        return

    log.debug("Shape: %s", nii.shape)
    log.debug("Scale: %s", header.get_xyzt_units())

    for f in range(data.shape[3]):
        log.info("Frame %d", f)
        frame = data[..., f]
        export_frame(frame, scale, geo_path % f)



if __name__ == "__main__":
    log.addHandler(logging.StreamHandler())

    usage = """%prog NIFTI..."""

    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="count", dest="verbose",
                      help="Print verbose information for debugging.", default=0)
    parser.add_option("-q", "--quiet", action="count", dest="quiet",
                      help="Suppress warnings.", default=0)
    parser.add_option("-z", "--zero-padding", action="store", dest="padding", type=int,
                      help="Zero padding for frames. Eg. 0 would yield '123', 8 would yield '00000123'. Default is 0.", default=0)

    (options, args) = parser.parse_args()

    log_level = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG,)[
        max(0, min(3, 1 + options.verbose - options.quiet))]

    log.setLevel(log_level)

    if not len(args):
        parser.print_usage()
        sys.exit(1)

    for arg in args:
        nifti1_4d_to_geo(arg, options.padding)
