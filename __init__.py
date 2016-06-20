from pelican.readers import BaseReader
from pelican import signals
from pypandoc import convert_file
from datetime import datetime
import yaml
import logging
import os

logger = logging.getLogger(__name__)

META_TEMPLATE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'metadata.template')

class PandocReader(BaseReader):
    enabled = True
    file_extensions = []
    outfmt = 'html5'
    args = []
    filters = []

    def read(self, path):
        content = convert_file(path, to=self.outfmt, extra_args=self.args, filters=self.filters)
        metadata = self.read_metadata(path)
        return content, metadata

    def read_metadata(self, path, format=None):
        metadata_yaml = convert_file(path, to='markdown', format=format,
                                     extra_args=['--template', META_TEMPLATE])
        raw_metadata = yaml.safe_load(metadata_yaml)
        logger.debug(str(raw_metadata))
        metadata = {}
        for name, value in raw_metadata.items():
            name = name.lower()
            metadata[name] = self.process_metadata(name, value)
        return metadata


def add_reader(readers):
    if 'PANDOC_FILES' in readers.settings:
        PandocReader.file_extensions.extend(readers.settings['PANDOC_FILES'])

    if 'PANDOC_ARGS' in readers.settings:
        PandocReader.args.extend(readers.settings['PANDOC_ARGS'])

    if 'PANDOC_FILTERS' in readers.settings:
        PandocReader.filters.extend(readers.settings['PANDOC_FILTERS'])

    for ext in PandocReader.file_extensions:
        readers.reader_classes[ext] = PandocReader

def register():
    logger.debug("Registering pandoc_reader plugin.")
    signals.readers_init.connect(add_reader)
