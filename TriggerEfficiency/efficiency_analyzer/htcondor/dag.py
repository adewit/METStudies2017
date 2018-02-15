import os

import jinja2


class DAG(object):
    """An interface for submitting DAGMan jobs to HTCondor.

    Parameters
    ----------
    input_files : path or iterable of paths, optional
        The path or paths for additional input files provided by the user.
    """

    TEMPLATE_DIR = None

    def __init__(self, input_files=[]):
        self._templates = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.TEMPLATE_DIR),
            trim_blocks=True,
        )
        self.input_files = input_files

    @property
    def input_files(self):
        return self._input_files

    @input_files.setter
    def input_files(self, value):
        if isinstance(value, basestring):
            self._input_files = [os.path.abspath(value)]
        else:
            self._input_files = [os.path.abspath(_) for _ in value]

    def submit(self):
       raise NotImplementedError

    def _generate_from_template(self, name, path, context):
        """Generate a job submission file by rendering its template.

        Each job submission file has a corresponding template with variables
        that are rendered using the job submission arguments and environment.

        Parameters
        ----------
        name : str
            The name of the template.
        path : path
            The output file path.
        context : dict
            The mapping between job submission arguments and environment
            variables to the names of their corresponding template variables.
        """
        template = self._templates.get_template(name)
        with open(path, 'w') as f:
            f.write(template.render(context))

