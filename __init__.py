from .readers import PandocReader
from pelican import signals

def initialize(pelican):
    # get pandoc file types from settings
    if 'PANDOC_FILES' in pelican.settings:
        PandocReader.file_extensions.extend(pelican.settings['PANDOC_FILES'])

    # get pandoc path from settings
    if 'PANDOC_PATH' in pelican.settings:
        PandocReader.pandoc[0] = pelican.settings['PANDOC_PATH']

    # get pandoc arguments from settings
    if 'PANDOC_ARGS' in pelican.settings:
        PandocReader.pandoc.extend(pelican.settings['PANDOC_ARGS'])

    # associate PandocReader with file types
    for ext in PandocReader.file_extensions:
        pelican.reader_classes[ext] = PandocReader

    return

def register():
    signals.readers_init.connect(initialize)
