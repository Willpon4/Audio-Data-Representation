# -*- coding: utf-8 -*-
"""
/***************************************************************************
 adr_plugin
                                 A QGIS plugin
 Version 3 of ADR QGIS Plugin
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-05-05
        copyright            : (C) 2025 Will Ponczak
        email                : ponczawm@dukes.jmu.edu
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load adr_plugin class from file adr_plugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .adr_plugin_v3 import AdrPluginV3
    return AdrPluginV3(iface)
