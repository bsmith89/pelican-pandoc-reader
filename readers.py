from pelican.readers import BaseReader

import os.path
import re
import yaml
from subprocess import Popen, PIPE
from pelican.utils import pelican_open

class PandocReader(BaseReader):
    enabled = True
    file_extensions = ['md']
    pandoc = ['pandoc', '--to=html5']

    def _pandoc_parse(self, pandoc, document):
        """Parse a document"""

        # start pandoc process
        proc = Popen(pandoc, stdin=PIPE, stdout=PIPE)

        # send document to pandoc and capture output
        output = proc.communicate(document.encode('utf-8'))[0]

        # convert output to unicode
        return output.decode('utf-8')

    def read(self, source_path):
        """Read files using pandoc"""

        # parts of the file
        frontmatter = {}
        document = u''

        # read the source file
        with pelican_open(source_path) as source:

            # split source into front matter and document
            match = re.match(r'\s*[-]{3}\n(.*?)\n[-.]{3}\n', source, re.U|re.M|re.S)
            if match:
                frontmatter = yaml.load(match.group(1), Loader=yaml.BaseLoader)
                document = source[len(match.group(0)) - 1:]
            else:
                document = source

        # make sure frontmatter was read as a dict
        if not isinstance(frontmatter, dict):
            frontmatter = {}

        # process frontmatter into metadata
        metadata = {}
        for name, value in frontmatter.items():
            name = name.lower()
            metadata[name] = self.process_metadata(name, value)

        # check if toc was requested
        if '--toc' in self.pandoc or '--table-of-contents' in self.pandoc:
            template_toc = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'toc.html'
            )

            # pandoc commands to generate toc
            pandoc_toc = self.pandoc + ['--template=' + template_toc]

            # run pandoc for toc
            metadata['toc'] = self._pandoc_parse(pandoc_toc, document)

        # run pandoc for content
        content = self._pandoc_parse(self.pandoc, document)

        return content, metadata
