# -*- coding: utf-8 -*-
# Module: plugin_test
# Author: Roman V.M.
# Created on: 28.05.2015
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import urlparse
from xbmcplugin import *


orig_import = __import__  # Store the original __import__
def import_mock(name, *args, **kwargs):
    """
    The function allows to inject _Plugin instance methods instead of
    the original xbmcplugin module functions during import.
    :param name: str - importedmodule name
    :param args:
    :param kwargs:
    :return:
    """
    if name == 'xbmcplugin':
        return orig_import('plugin_test', *args, **kwargs)
    return orig_import(name, *args, **kwargs)


class PluginTestError(Exception):
    pass


class _Plugin(object):
    """Class for testing Kodi content plugins"""
    def __init__(self):
        """Class constructor"""
        self._items = []
        self.sys_argv = []
        self._backstack = []

    def addDirectoryItem(self, handle, url, listitem, isFolder=False, totalItems=0):
        """Callback function to pass directory contents back to XBMC.

        Replaces the original xbmcplugin.addDirectoryItem function
        """
        self._items.append({'handle': handle, 'url': url, 'list_item': listitem, 'isFolder': isFolder,
                           'totalItems': totalItems})
        return True

    def addDirectoryItems(self, handle, items, totalItems=0):
        """Callback function to pass directory contents back to XBMC as a list.

        Replaces the original xbmcplugin.addDirectoryItems function
        """
        for item in items:
            try:
                self.addDirectoryItem(handle, item[0], item[1], item[2], totalItems)
            except IndexError:
                self.addDirectoryItem(handle, item[0], item[1], totalItems=totalItems)
        return True

    def endOfDirectory(self, handle, succeeded=True, updateListing=False, cacheToDisc=True):
        """Callback function to tell XBMC that the end of the directory listing
        in a virtualPythonFolder module is reached.

        Replaces the original xbmcplugin.endOfDirectory function
        """
        if self.sys_argv[1] == '-1':
            raise PluginTestError('Trying to display a virtual folder when isFolder=False!')
        while True:
            i = 0
            # Print menu
            print '===***= Start Plugin Menu =***==='
            if self._backstack:
                print '0 - < Back'
            print '===***=== Start Listing ===***==='
            for item in self._items:
                i += 1
                print '{0} - {1}'.format(i, item['list_item'])
            print '===***==== End Listing ====***==='
            print 'Enter the item # to select it, or 0 to return back.'
            print 'Enter "q" to quit.'
            selection = raw_input('Your selection: ')
            if selection == 'q' or (selection == '0' and not self._backstack):
                print 'Exiting plugin test...'
                self.sys_argv = []
                break
            elif selection == '0' and self._backstack:
                self._decrement_backstack()
                break
            else:
                try:
                    index = int(selection) - 1
                except ValueError:
                    print 'Invalid input!'
                    continue
                else:
                    # Append current sys.argv to backstack
                    back_item = self.sys_argv[:]  # Copy sys_argv list by value
                    self._backstack.append(back_item)
                    # Construct new sys.argv for the next call
                    query = urlparse.urlparse(self._items[index]['url']).query
                    if query:
                        self.sys_argv[2] = '?' + query
                    else:
                        self.sys_argv[2] = ''
                    if self._items[index]['isFolder']:
                        self.sys_argv[1] = '1'
                    elif not self._items[index]['isFolder'] and self._items[index]['list_item']._list_item['properties']['IsPlayable'] == 'true':
                        self.sys_argv[1] = '-1'
                    else:
                        print '===***= Opening a direct URL =***==='
                        print 'Opening url: {0}'.format(self._items[index]['url'])
                        print '===***========================***==='
                        self._decrement_backstack()
                    break
        self._items = []

    def setResolvedUrl(self, handle, succeeded, listitem):
        """Callback function to tell XBMC that the file plugin has been resolved to a url

        Replaces the original xbmcplugin.setResolvedUrl function
        """
        if self.sys_argv[1] != '-1':
            raise PluginTestError('Trying to play an item with isFolder=True')
        print '===***=== Start Playback ===***==='
        print 'Playing path: {0}'.format(listitem._list_item['path'])
        print '===***==== End Playback ====***==='
        self._decrement_backstack()

    def _decrement_backstack(self):
        """
        Remove the last item in the backstack
        :return:
        """
        self.sys_argv = self._backstack[-1][:]
        del self._backstack[-1]


# Create plugin instance
plugin = _Plugin()
# Replace xbmcplugin functions with plugin methods
addDirectoryItem = plugin.addDirectoryItem
addDirectoryItems = plugin.addDirectoryItems
endOfDirectory = plugin.endOfDirectory
setResolvedUrl = plugin.setResolvedUrl
