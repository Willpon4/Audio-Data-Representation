import os
import time
import math
from qgis.core import QgsProject, QgsRasterBandStats, QgsPointXY
from qgis.gui import QgsMapToolEmitPoint
from .adr_plugin_v3_dialogue import AdrPluginDialog  # Ensure correct import
from mido import Message, MidiFile, MidiTrack, open_output, get_output_names




class AdrPluginV3:
    def __init__(self, iface):
        """Constructor for the plugin"""
        self.iface = iface
        self.dlg = None
        self.canvas = None
        self.emitPoint = None
        self.coord_x = None
        self.coord_y = None
        self.transform = None
        self.layers = None

    def run(self):
        """Run method that identifies user click on QGIS canvas and sends point to display_point function"""
        self.dlg = AdrPluginDialog()
        self.dlg.show()

        self.canvas = self.iface.mapCanvas()
        self.emitPoint = QgsMapToolEmitPoint(self.canvas)
        self.canvas.setMapTool(self.emitPoint)

        # Connect the click event to the display_point function
        self.emitPoint.canvasClicked.connect(self.display_point)

    def display_point(self, emitPoint):
        """Handles click events on the map, processes the raster data, and writes normalized values to a named pipe."""
        self.coord_x = emitPoint.x()
        self.coord_y = emitPoint.y()

        # Convert coordinates
        self.transform = QgsPointXY(self.coord_x, self.coord_y)

        # Retrieve normalization values and hearable data
        normalizationVals, layer_hearable, band_hearable = self.dlg.get_all_inputs()

        # Get the layers in the project
        self.layers = QgsProject.instance().layerTreeRoot().children()

        data_values = self.get_layer_data_values(layer_hearable, band_hearable, normalizationVals)

        # If there are any valid data values, write them to the named pipe
        if data_values:
            self.play_midi(data_values)

    def get_layer_data_values(self, layer_hearable, band_hearable, normalizationVals):
        """Loops through all layers and bands, retrieves the data values, and normalizes them."""
        data_values = []

        for layer in self.layers:
            layer_name = layer.name()
            layer = layer.layer()

            if layer_hearable.get(layer_name):
                for band_index, is_band_hearable in enumerate(band_hearable.get(layer_name, [])):
                    if is_band_hearable:
                        band_num = band_index + 1
                        val = self.get_band_value(layer, band_num)

                        if not math.isnan(val):
                            stats = self.get_band_statistics(layer, band_num)
                            normalized_val = self.normalize_value(val, stats, normalizationVals, layer_name, band_num, layer)

                            data_values.append(normalized_val)

        return data_values

    def get_band_value(self, layer, band_num):
        """Retrieves the raster value at the clicked point for the specified band."""
        return layer.dataProvider().sample(self.transform, band_num)[0]

    def get_band_statistics(self, layer, band_num):
        """Retrieves band statistics for the specified band."""
        return layer.dataProvider().bandStatistics(band_num, QgsRasterBandStats.All)

    def normalize_value(self, val, stats, normalizationVals, layer_name, band_num, layer):
        """Normalizes the value using feature scaling (min-max normalization)."""
        band_name = layer.bandName(band_num)
        normalized_min, normalized_max = normalizationVals[layer_name][band_name]
        normalized_val = normalized_min + (((val - stats.minimumValue) * (normalized_max - normalized_min)) / (stats.maximumValue - stats.minimumValue))
        return round(normalized_val)

    def play_midi(self, data_values):
        try:
            print("Available MIDI ports:", get_output_names())
            port_name = 'IAC Driver Python to GarageBand'  # Change if your IAC name is different
            with open_output(port_name) as port:
                print(f"Sending MIDI: {data_values}")
                for val in data_values:
                    if 0 <= val <= 127:
                        msg = Message('note_on', note=val, velocity=64, time=0)
                        port.send(msg)
                        time.sleep(0.2)
                        port.send(Message('note_off', note=val, velocity=64, time=0))
        except Exception as e:
            print(f"Error playing MIDI: {e}")

    def initGui(self):
        from qgis.PyQt.QtWidgets import QAction
        from qgis.PyQt.QtGui import QIcon
        import os

        icon_path = os.path.join(os.path.dirname(__file__), "")  # Or leave as "" if no icon
        action = QAction(QIcon(icon_path), "ADR Plugin", self.iface.mainWindow())
        action.triggered.connect(self.run)

        self.iface.addToolBarIcon(action)
        self.iface.addPluginToMenu("&ADR Plugin", action)

    def unload(self):
        if hasattr(self, "action"):
            self.iface.removeToolBarIcon(action)
            self.iface.removePluginMenu("&ADR Plugin", action)



        
