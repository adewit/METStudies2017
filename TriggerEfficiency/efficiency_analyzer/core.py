import os
import subprocess
import sys
import time

from .htcondor.dag import DAG
from .utils.dbs import get_file_records_from_dbs
from .utils.os import safe_makedirs
from .utils.xrootd import xrdfs_locate_root_files


class EfficiencyAnalyzerError(Exception):
    pass


class EfficiencyAnalyzer(DAG):
    """An interface for submitting efficiency analyzer jobs to HTCondor.

    Parameters
    ----------
    input_files : path or iterable of path, optional
        The path or paths for additional input files provided by the user.
    no_submit : bool, optional
        If true, prevents the submit method from submitting jobs
        to the scheduler. The default is False.
    """

    TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

    def __init__(self, input_files=[], no_submit=False):
        super(EfficiencyAnalyzer, self).__init__(input_files)
        self.no_submit = no_submit

    def submit(self, name, src, cuts, histograms, dbs_instance=None, xrootd_redirector='cms-xrd-global.cern.ch', commands={}, max_jobs=250, no_submit=False):
        """Submit an analyzer job to HTCondor DAGMan.

        DAGMan jobs can be retried automatically and, should jobs fail, users can
        take advantage of the automatically generated rescue DAG for resubmitting
        only failed jobs.

        For more information, see the DAGMan documentation at
        http://research.cs.wisc.edu/htcondor/manual/latest/2_10DAGMan_Applications.html

        Parameters
        ----------
        name : string
            The name of the parent directory for the generated job submission files.
        src : string or url
            Either a fully qualified dataset name or an XRootD url.
        dbs : string, optional
            Use a DBS instance to locate dataset files, e.g. phys03.
            The default is None to use xrdfs to locate the input files.
        xrootd_redirector : string, optional
            The XRootD redirector used to access dataset files. This is only
            used when the source is a dataset. The default is "cms-xrd-global.cern.ch".
        commands : dict, optional
            HTCondor commands to include in the submit description file, in addition to the
            following which are handled automatically:
                * arguments
                * error
                * executable
                * getenv
                * log
                * output
                * queue
                * should_transfer_files
                * transfer_input_files
                * transfer_output_files
                * universe
            The default is no additional commands.
        max_jobs : int, optional
            The maximum number of concurrent jobs within the DAG. The default is 250.
        no_submit : bool, optional
            If True, the job submission files are generated but not submitted
            to the HTCondor scheduler. The default is False.
        """
        # Collect the job context variables.
        context = {
            'timestamp': time.strftime('%a %b %d %H:%M:%S %Z %Y'),
            'CMSSW_VERSION': os.environ['CMSSW_VERSION'],
            'SCRAM_ARCH': os.environ['SCRAM_ARCH'],
            'input_files': self.input_files[:] + ['efficiency_analyzer.py'],
            'cuts': cuts,
            'histograms': histograms,
            'commands': commands,
        }

        if dbs_instance is None:
            context['jobs'] = xrdfs_locate_root_files(src)
        else:
            context['jobs'] = [
                'root://{0}//{1}'.format(xrootd_redirector, _.logical_file_name)
                for _ in get_file_records_from_dbs(dataset=src, instance=dbs_instance)
            ]

        # Create the directory tree for the job submission files.
        dagdir = os.path.join(os.getcwd(), 'EfficiencyAnalyzerJobs', name)
        dag_path = os.path.join(dagdir, 'dag')
        dag_exists = True if os.path.isfile(dag_path) else False
        if not dag_exists:
            logdir = os.path.join(dagdir, 'logs')
            safe_makedirs(logdir)
            # Generate the job submission files.
            self._generate_from_template('dag_input_file', dag_path, context)
            self._generate_from_template('node_submit_description', os.path.join(dagdir, 'node'), context)
            self._generate_from_template('run_efficiency_analyzer.sh', os.path.join(dagdir, 'run_efficiency_analyzer.sh'), context)
            self._generate_from_template('efficiency_analyzer.py', os.path.join(dagdir, 'efficiency_analyzer.py'), context)
            for input_file in self.input_files[:-1]:
                shutil.copy(input_file, dagdir)
            safe_makedirs(os.path.join(dagdir, 'outputs'))
        # Unless otherwise directed, submit the DAG input file to DAGMan.
        if self.no_submit or no_submit:
            if dag_exists:
                print 'HTCondor DAG input file exists but not submitted: {0}'.format(dag_path)
            else:
                print 'HTCondor DAG input file generated but not submitted: {0}'.format(dag_path)
        else:
            subprocess.check_call(['condor_submit_dag', '-usedagdir', '-maxjobs', str(max_jobs), dag_path])

