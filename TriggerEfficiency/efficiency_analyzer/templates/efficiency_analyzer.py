#!/usr/bin/env python
import sys
import uuid

import ROOT


################################################################################
# TEMPLATE CONSTANTS

CUTS = [
{% for cut in cuts %}
    '{{ cut }}',
{% endfor %}
]

HISTOGRAMS = [
{% for histogram in histograms %}
    {{ histogram }},
{% endfor %}
]

################################################################################


class Events(ROOT.TChain):
    """A TChain subclass with convenience methods for a cutflow analysis.

    Assumes the ntuples are in NanoAOD format where the name of the tree
    is "Events".

    Parameters
    ----------
    filenames : path or paths
        The path or paths of ntuples to analyze.
    """
    def __init__(self, filenames):
        super(Events, self).__init__('Events')
        for filename in filenames:
            self.Add(filename)

    def __len__(self):
        """The total number of entries."""
        return self.GetEntries()

    @property
    def eventlist(self):
        return self.GetEventList()

    @eventlist.setter
    def eventlist(self, value):
        self.SetEventList(value)

    def _create_eventlist(self, selection):
        """Return the eventlist for a selection."""
        name = uuid.uuid4().hex
        self.Draw('>>{0}'.format(name), selection, 'goff')
        eventlist = ROOT.gDirectory.Get(name)
        eventlist.SetDirectory(0)
        return eventlist

    def histogram(self, name, variable, nbins, xmin, xmax, weights=''):
        """Draw and return a histogram.

        Parameters
        ----------
        name : string
            The name of the histogram. It should be unique to
            avoid being overwritten.
        variable : string
            The variable to draw. This can be a TTreeFormula expression.
        nbins : int
            The number of bins.
        xmin : numeric
            The value of the lower edge of the first bin.
        xmax : numeric
            The value of the upper edge of the last bin.
        weights : string, optional
            Any additional weights to apply to the events.
        """
        self.Draw('{variable}>>{name}({nbins!s}, {xmin!s}, {xmax!s})'.format(**locals()), weights, 'goff')
        h = ROOT.gDirectory.Get(name)
        h.SetDirectory(0)
        h.Sumw2()
        return h

    def select(self, selection):
        """Apply a selection on the events.

        If selections have already been applied, only the current
        subset of passing events are considered.

        Parameters
        ----------
        selection : string
            The selection expression.
        """
        eventlist = self._create_eventlist(selection)
        if eventlist:
            if self.eventlist:
                eventlist.Intersect(self.eventlist)
            self.eventlist = eventlist
        return self


def main():
    events = Events(filenames=sys.argv[1:-1])

    output_file = ROOT.TFile.Open(sys.argv[-1], 'recreate')

    # Collect histograms before any cuts are applied.
    subdir = output_file.mkdir('NoCuts')
    subdir.cd()
    for h in HISTOGRAMS:
        events.histogram(*h).Write()

    # Collect histograms after successively applying cuts.
    for i, cut in enumerate(CUTS, start=1):
        subdir = output_file.mkdir('Cut{0!s}'.format(i))
        subdir.cd()
        events.select(cut)
        tree_test = events.GetTree().CopyTree(cut)
        tree_test.Write()
        for h in HISTOGRAMS:
            events.histogram(*h).Write()

    output_file.Close()


if __name__ == '__main__':

    status = main()
    sys.exit(status)

