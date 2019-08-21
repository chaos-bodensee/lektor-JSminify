# make print compatible with python2
from __future__ import print_function
import os
import errno
import re
import fnmatch

import rjsmin
from lektor.pluginsystem import Plugin
from lektor.utils import comma_delimited
from termcolor import colored
import threading
import time

MINIFY_FLAG = "jsminify"

def any_fnmatch(filename, patterns):
    for pat in patterns:
        if fnmatch.fnmatch(filename, pat):
            return True

    return False

class JsminifyPlugin(Plugin):
    name = u'Lektor JSminify'
    description = u'JS minifier for Lektor. Based on rjsmin.'

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        config = self.get_config()
        self.source_dir = config.get('source_dir', 'asset_sources/js/')
        self.output_dir = config.get('output_dir', 'assets/js/')
        self.name_prefix = config.get('name_prefix', '')
        self.keep_bang_comments = config.get('keep_bang_comments', 'False')
        self.included_assets = list(comma_delimited(config.get('included_assets', '')))
        self.excluded_assets = list(comma_delimited(config.get('excluded_assets', '')))
        self.watcher = None
        self.run_watcher = False

    def is_enabled(self, build_flags):
        return bool(build_flags.get(MINIFY_FLAG))

    def is_uninteresting_source_name(self, filename):
        """These files are ignored when sources are built into artifacts."""
        if any_fnmatch(filename, self.included_assets):
            # Included by the user's project config, thus not uninteresting.
            return False
        return any_fnmatch(filename, self.excluded_assets)

    def minify_file(self, target, output):
        """
        Minifies the target js file.
        """

        filename = os.path.basename(target)
        output_file = os.path.join(output, filename)
        file_end = self.name_prefix + '.js'
        if not output_file.endswith(file_end):
            output_file = output_file.replace('.js', file_end)
        
        rebuild = False
        config_file = os.path.join(self.env.root_path, 'configs/jsminify.ini')

        # when input file changed
        if os.path.isfile(output_file):
            if ( os.path.getmtime(target) > os.path.getmtime(output_file)
              # when config file exists and changed
              or os.path.isfile(config_file) and os.path.getmtime(config_file) > os.path.getmtime(output_file)):
                rebuild = True
        else:
            rebuild = True

        if not rebuild:
            return

        result = None
        with open(target, 'r') as fr:
            result = rjsmin.jsmin(fr.read(), self.keep_bang_comments.lower()=='true')

        if result == None:
            return
    
        with open(output_file, 'w') as fw:
            fw.write(result)
        print(colored('js', 'green'), self.source_dir + os.path.basename(target), '\u27a1', self.output_dir + os.path.basename(output_file))

    def find_source_files(self, destination):
        """
        Finds all js files in the given destination.
        """
        for root, dirs, files in os.walk(destination):
            for f in files:
                if f.endswith('.js') and not self.is_uninteresting_source_name(f):
                    yield os.path.join(root, f)

    def thread(self, filenames, output):
        while True:
            if not self.run_watcher:
                self.watcher = None
                break
            for filename in filenames:
                self.minify_file(filename, output)
            time.sleep(1)

    def on_server_spawn(self, **extra):
        self.run_watcher  = True

    def on_server_stop(self, **extra):
        if self.watcher is not None:
            self.run_watcher = False

    def make_sure_path_exists(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise            

    def on_before_build_all(self, builder, **extra):
        try: # lektor 3+
            is_enabled = self.is_enabled(builder.extra_flags)
        except AttributeError: # lektor 2+
            is_enabled = self.is_enabled(builder.build_flags)

        if not is_enabled:
            return

        root_js = os.path.join(self.env.root_path, self.source_dir )
        output = os.path.join(self.env.root_path, self.output_dir )

        # output path has to exist
        #os.makedirs(output, exist_ok=True) when python2 finally runs out
        self.make_sure_path_exists(output)

        if self.run_watcher:
            filenames = self.find_source_files(root_js)
            self.watcher = threading.Thread(target=self.thread, args=(filenames, output))
            self.watcher.start()
        else:
            for filename in self.find_source_files(root_js):
                self.minify_file(filename, output)
