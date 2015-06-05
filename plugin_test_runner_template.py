# -*- coding: utf-8 -*-
# Module: test_template
# Author: Roman V.M.
# Created on: 27.05.2015
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

# Your plugin ID as in addon.xml and the plugin folder name.
__id__ = 'plugin.video.example'
# Starting script of your plugin
__script__ = 'default'
# Starting point of your plugin.
# This is a starting point
__start_point__ = 'router'

import sys
import os
import mock
from plugin_test import plugin, import_mock

plugin.sys_argv = ['plugin://{0}/'.format(__id__), '1', '']
# Your test runner script must be 1 level higher than your plugin folder.
# E.g:
# /project_folder/
#       |
#       +-- /your.plugin.folder/
#       +-- test_runner.py
#
sys.path.append(os.path.join(os.path.dirname(__file__), __id__))


@mock.patch('sys.argv', plugin.sys_argv)
@mock.patch('__builtin__.__import__', side_effect=import_mock)
# Below you can add your plugin-specific mock patches for Kodi Python API calls
# Mind the parameters order for a decorated function!!!
# Bottom-top (patches) => left-right (function parameters)
def main(*args):
    # If you add your own mock patches,
    # here you need to set-up your mock parameters
    # (properties, return values, etc.)
    script = __import__(__script__)
    while plugin.sys_argv:
        getattr(script, __start_point__)(plugin.sys_argv[2])


if __name__ == '__main__':
    main()
