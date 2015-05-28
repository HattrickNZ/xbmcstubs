# -*- coding: utf-8 -*-
# Module: test_template
# Author: Roman V.M.
# Created on: 27.05.2015
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

__id__ = 'plugin.video.example'
__script__ = 'default'
__start_point__ = 'router'

import sys
import os
import mock
from plugin_test import plugin, import_mock

plugin.sys_argv = ['plugin://{0}/'.format(__id__), '1', '']
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), __id__))


@mock.patch('sys.argv', plugin.sys_argv)
@mock.patch('__builtin__.__import__', side_effect=import_mock)
def main(*args):
    script = __import__(__script__)
    while plugin.sys_argv:
        getattr(script, __start_point__)(plugin.sys_argv[2])


if __name__ == '__main__':
    main()
