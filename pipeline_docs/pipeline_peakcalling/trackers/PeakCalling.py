'''Collection of per-caller summary statistics.

The data are specific for each caller.
'''

import os, sys, re, types, itertools
import matplotlib.pyplot as plt
import numpy, scipy.stats
import numpy.ma
import Stats
import Histogram

from SphinxReport.Tracker import *
from PeakcallingReport import *

class MacsSummary( DefaultTracker ):
    '''summary information from macs.'''

    tablename = 'macs_summary'

    def getTracks( self, subset = None ):
        if self.tablename in self.getTables():
            return self.getValues( "SELECT track FROM %(tablename)s ORDER BY track" )
        else: 
            return None
    
    def __call__(self, track, slice = None ):

        resultsdir = os.path.abspath( os.path.join( EXPORTDIR, "MACS" ) )
        
        fields = (
            "called_positive", "called_negative",
            "scan_window", "shift",
            "tag_treatment_total", "tag_treatment_filtered", 
            "tag_control_total", "tag_control_filtered", 
            "ncandidates_positive", "ncandidates_negative", 
            "min_tags",
            "paired_peaks", )

        f = ",".join(fields)
        data = self.getFirstRow( '''SELECT %(f)s FROM %(tablename)s WHERE track="%(track)s"''' )
        result = odict( zip( fields, data) )

        if os.path.exists( resultsdir ):
            result["peakshape"] = "`pdf <%(resultsdir)s/%(track)s_model.pdf>`_" % locals()

        return result

class MacsDiagnostics(CallingTracker):
    """summary of macs diagnostics data."""

    pattern = "(.*)_macs_diagnostics"

    def __call__(self, track, slice = None ):

        data = self.get( "SELECT fc,npeaks,p20,p30,p40,p50,p60,p70,p80,p90 FROM %(track)s_macs_diagnostics" % locals() )

        result = odict()
        for fc,npeaks,p20,p30,p40,p50,p60,p70,p80,p90 in data:
            result[fc] = odict()
            result[fc]["npeaks"] = npeaks
            result[fc]["proportion of reads"] = range( 20, 100, 10)
            result[fc]["proportion of peaks"] = map( float, (p20,p30,p40,p50,p60,p70,p80,p90) ) 
            
        return result

class MacsFiltering(CallingTracker, SingleTableTrackerColumns ):
    '''summary of filtering.'''
    column = "fdr"
    table = "macs_fdr"

class Macs2Summary(MacsSummary):
    tablename = 'macs2_summary'

class Macs2Diagnostics(MacsDiagnostics):
    pattern = "(.*)_macs2_diagnostics"

class Mac2sFiltering(MacsFiltering):
    table = 'macs2_fdr'

class SPPSummary( DefaultTracker, SingleTableTrackerRows ):
    '''summary information from spp.'''
    table = "spp_summary"

class SICERSummary( DefaultTracker, SingleTableTrackerRows ):
    '''summary information from sicer.'''
    table = "sicer_summary"


class SPPQuality( DefaultTracker, SingleTableTrackerRows ):
    '''quality control information from spp.'''
    table = "spp_quality"
