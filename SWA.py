import os
import os.path
import sys

from qgis.core import *
from qgis.gui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mapTools import *
from osgeo import gdal


from mainWindow import Ui_MainWindow
from newWelcomeWindow import Ui_Dialog

from mapTools import *

class Welcome(QMainWindow, Ui_Dialog):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        #self.loaded[str].connect(self.onLoadFile)

   # def onLoadFile(self, path):
       # self.hide()
        #self.newWindow = SWAMain(path)
       # self.newWindow.show()
        #self.newWindow.raise_()


class SWAMain(QMainWindow, Ui_MainWindow):
    def __init__(self, path):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.editing = False
        self.modified = False



        self.mapCanvas = self.QgsMapCanvas
        self.mapCanvas.setCanvasColor(Qt.white)
        self.mapCanvas.setGeometry(QRect(140, 130, 521, 301))
        self.mapCanvas.show()

        self.setupDatabase("StreetFlowLayer")
        self.setupMapLayers()
        self.setupRenderers(self.StreetFlowLayer)
        self.setupMapTools(self.StreetFlowLayer)
        self.setPanMode()
        self.adjustActions()
        self.view.setCurrentLayer(self.StreetFlowLayer)

        self.actionQuit.triggered.connect(self.quit)
        self.actionPan.triggered.connect(self.setPanMode)
        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionEdit.triggered.connect(self.setEditMode)
        self.actionAddFlowPath.triggered.connect(self.addFlowPath)
        self.actionEditFlowPath.triggered.connect(self.editFlowPath)
        self.actionDeleteFlowPath.triggered.connect(self.deleteFlowPath)
        self.actionLoad_File.triggered.connect(self.openShp)
        self.actionAddLayer.triggered.connect(self.addLayer)
        self.view.currentLayerChanged.connect(self.selectNewLayer)

    def setupDatabase(self, name):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        db_name = os.path.join(cur_dir, "data", name+".sqlite")
        if not os.path.exists(db_name):
            fields = QgsFields()
            fields.append(QgsField("id", QVariant.Int))
            fields.append(QgsField("type", QVariant.String))
            fields.append(QgsField("name", QVariant.String))
            fields.append(QgsField("direction", QVariant.String))

            crs = QgsCoordinateReferenceSystem(2913,
                                               QgsCoordinateReferenceSystem.EpsgCrsId)

            writer = QgsVectorFileWriter(db_name, "utf-8", fields,
                                         QgsWkbTypes.MultiLineString,
                                         crs, "SQLite",
                                         ["SPATIALITE=YES"])
            if writer.hasError() != QgsVectorFileWriter.NoError:
                print("Database create error")

            del writer

    def setupMapLayers(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        list_dir = os.listdir(os.path.join(cur_dir, "data"))
        layers = []
        self.baseLayer = QgsRasterLayer(os.path.join(cur_dir, "data", "basemap", "basemap.xml"), "OSM")
        if not self.baseLayer.isValid():
            print("Layer failed to load")
        crs = QgsCoordinateReferenceSystem(2913)
        self.baseLayer.setCrs(crs)
        QgsProject.instance().addMapLayer(self.baseLayer)
        layers.append(self.baseLayer)
        rect = QgsRectangle(-13735521, 5547682, -13730558, 5551709)
        self.mapCanvas.setExtent(rect)

        uri = QgsDataSourceUri()
        uri.setDatabase(os.path.join(cur_dir, "data", "StreetFlowLayer.sqlite"))
        uri.setDataSource("", "StreetFlowLayer", "GEOMETRY")

        self.StreetFlowLayer = QgsVectorLayer(uri.uri(), "Street Flow", "spatialite")
        QgsProject.instance().addMapLayer(self.StreetFlowLayer)

        layers.insert(0, self.StreetFlowLayer)
        QgsProject.instance().setCrs(crs)

        for f in list_dir:
            ext = os.path.splitext(f)[-1].lower()
            front = os.path.splitext(f)
            if ext == ".sqlite":
                if front[0] != "StreetFlowLayer":
                    uri = QgsDataSourceUri()
                    uri.setDatabase(os.path.join(cur_dir, "data", f))
                    uri.setDataSource("", front[0], "GEOMETRY")
                    self.drawLayer = QgsVectorLayer(uri.uri(), front[0], "spatialite")
                    QgsProject.instance().addMapLayer(self.drawLayer)
                    self.setupRenderers(self.drawLayer)
                    layers.insert(0, self.drawLayer)

        self.mapCanvas.setLayers(layers)

        self.root = QgsProject.instance().layerTreeRoot()
        self.bridge = QgsLayerTreeMapCanvasBridge(self.root, self.mapCanvas)
        self.model = QgsLayerTreeModel(self.root)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.model.setFlag(QgsLayerTreeModel.ShowLegend)
        self.view = QgsLayerTreeView()
        self.view.setModel(self.model)
        self.LegendDock = QDockWidget("Layers", self)
        self.LegendDock.setObjectName("layers")
        self.LegendDock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.LegendDock.setWidget(self.view)
        self.LegendDock.setContentsMargins(0, 0, 0, 0)
        self.addDockWidget(Qt.RightDockWidgetArea, self.LegendDock)



    def setupRenderers(self, layer):
        # Setup the renderer for our FlowPath layer.
        root_rule = QgsRuleBasedRenderer.Rule(None)
        width = .3
        line_colour  = "red"
        arrow_colour = "red"
        for FlowPath_direction in ("BOTH",
                                "FORWARD"):

            symbol = self.createFlowPathSymbol(width,
                                            line_colour,
                                            arrow_colour,
                                            FlowPath_direction)
            expression = "(direction='%s')" % FlowPath_direction

            rule = QgsRuleBasedRenderer.Rule(symbol,
                                               filterExp=expression)
            root_rule.appendChild(rule)
        symbol = QgsLineSymbol.createSimple({'line_style': 'dash', 'color': 'red'})
        rule = QgsRuleBasedRenderer.Rule(symbol, elseRule=True)
        root_rule.appendChild(rule)

        renderer = QgsRuleBasedRenderer(root_rule)
        layer.setRenderer(renderer)




    def createFlowPathSymbol(self, width, line_colour, arrow_colour,
                          direction):
        symbol = QgsLineSymbol.createSimple({})
        symbol.deleteSymbolLayer(0) # Remove default symbol layer.

        symbol_layer = QgsSimpleLineSymbolLayer()
        symbol_layer.setWidth(width)
        symbol_layer.setColor(QColor(line_colour))
        symbol.appendSymbolLayer(symbol_layer)
        registry = QgsSymbolLayerRegistry()
        marker_line_metadata = registry.symbolLayerMetadata("MarkerLine")
        marker_metadata      = registry.symbolLayerMetadata("SimpleMarker")

        symbol_layer = marker_line_metadata.createSymbolLayer({
                        "width"     : "0.26",
                        "color"     : arrow_colour,
                        "rotate"    : "1",
                        "placement" : "interval",
                        "interval"  : "20",
                        "offset"    : "0"})
        sub_symbol = symbol_layer.subSymbol()
        sub_symbol.deleteSymbolLayer(0)

        triangle = marker_metadata.createSymbolLayer({
                        "name"          : "filled_arrowhead",
                        "color"         : arrow_colour,
                        "color_border"  : arrow_colour,
                        "offset"        : "0.0",
                        "size"          : "2",
                        "outline_width" : "0.5",
                        "output_unit"   : "mapunit",
                        "angle"         : "0"})
        sub_symbol.appendSymbolLayer(triangle)
        symbol.appendSymbolLayer(symbol_layer)
        return symbol


    def onFlowPathAdded(self):
        self.modified = True
        self.mapCanvas.refresh()
        self.actionAddFlowPath.setChecked(False)
        self.setPanMode()

    def onFlowPathEdited(self):
        self.modified = True
        self.mapCanvas.refresh()

    def onFlowPathDeleted(self):
        self.modified = True
        self.mapCanvas.refresh()
        self.actionDeleteFlowPath.setChecked(False)
        self.setPanMode()

    def closeEvent(self, event):
        self.quit()

    def setupMapTools(self, layer):
        self.panTool = PanTool(self.mapCanvas)
        self.panTool.setAction(self.actionPan)
        self.addFlowPathTool = AddFlowPathTool(self.mapCanvas,
                                         layer,
                                         self.onFlowPathAdded)
        self.addFlowPathTool.setAction(self.actionAddFlowPath)

        self.editFlowPathTool = EditFlowPathTool(self.mapCanvas,
                                           layer,
                                           self.onFlowPathEdited)
        self.editFlowPathTool.setAction(self.actionEditFlowPath)

        self.deleteFlowPathTool = DeleteFlowPathTool(self.mapCanvas,
                                               layer,
                                               self.onFlowPathDeleted)
        self.deleteFlowPathTool.setAction(self.actionDeleteFlowPath)


    def zoomIn(self):
        self.mapCanvas.zoomIn()

    def zoomOut(self):
        self.mapCanvas.zoomOut()

    def quit(self):
        if self.editing and self.modified:
            reply = QMessageBox.question(self, "Confirm",
                                         "Save Changes?",
                                         QMessageBox.Yes | QMessageBox.No
                                         | QMessageBox.Cancel,
                                         QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.StreetFlowLayer.commitChanges()
            elif reply == QMessageBox.No:
                self.StreetFlowLayer.rollBack()

            if reply != QMessageBox.Cancel:
                qApp.quit()
        else:
            qApp.quit()


    def setPanMode(self):
        self.mapCanvas.setMapTool(self.panTool)

    def adjustActions(self):
        if self.editing:
            self.actionAddFlowPath.setEnabled(True)
            self.actionEditFlowPath.setEnabled(True)
            self.actionDeleteFlowPath.setEnabled(True)
        else:
            self.actionAddFlowPath.setEnabled(False)
            self.actionEditFlowPath.setEnabled(False)
            self.actionDeleteFlowPath.setEnabled(False)

    def addFlowPath(self):
        if self.actionAddFlowPath.isChecked():
            self.mapCanvas.setMapTool(self.addFlowPathTool)
        else:
            self.setPanMode()
        self.adjustActions()

    def editFlowPath(self):
        if self.actionEditFlowPath.isChecked():
            self.mapCanvas.setMapTool(self.editFlowPathTool)
        else:
            self.setPanMode()

    def deleteFlowPath(self):
        if self.actionDeleteFlowPath.isChecked():
            self.mapCanvas.setMapTool(self.deleteFlowPathTool)
        else:
            self.setPanMode()

    def setEditMode(self):
        layer = self.view.currentLayer()
        print(layer)
        if layer is None:
            layer = self.StreetFlowLayer
        if self.editing:
            if self.modified:
                reply = QMessageBox.question(self, "Confirm", "Save Changes?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    layer.commitChanges()
                else:
                    layer.rollBack()
            else:
                layer.commitChanges()
            layer.triggerRepaint()
            self.editing = False
            self.setPanMode()
        else:
            layer.startEditing()
            layer.triggerRepaint()
            self.editing = True
            self.modified = False

        self.adjustActions()

    def getInfo(self):
        pass

    def openShp(self):
        shpFileName = QFileDialog.getOpenFileName(None, "Select File")
        if shpFileName[0] != "":
            url = QUrl.fromLocalFile(shpFileName[0])
            filenameunsplit = url.fileName()
            filesplit = filenameunsplit.split(".")
            self.newLayer = QgsVectorLayer(shpFileName[0], filesplit[0], "ogr")
            QgsProject.instance().addMapLayer(self.newLayer)
            currentLayers = self.mapCanvas.layers()
            currentLayers.insert(0, self.newLayer)
            self.mapCanvas.setLayers(currentLayers)
            self.mapCanvas.setExtent(self.newLayer.extent())
            self.mapCanvas.refresh()

    def selectNewLayer(self):
        print("New layer selected")
        self.setupMapTools(self.view.currentLayer())
        if self.editing:
            self.setEditMode()

    def addLayer(self):
        print("Add a new layer")
        name, pressed = QInputDialog.getText(self, "Add a new layer", "Layer name (no spaces):", QLineEdit.Normal, "")
        if pressed:
            self.setupDatabase(name)
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            uri = QgsDataSourceUri()
            uri.setDatabase(os.path.join(cur_dir, "data", name + ".sqlite"))
            uri.setDataSource("", name, "GEOMETRY")
            self.newlayer1 = QgsVectorLayer(uri.uri(), name, "spatialite")
            QgsProject.instance().addMapLayer(self.newlayer1)
            self.setupRenderers(self.newlayer1)
            currentLayers = self.mapCanvas.layers()
            currentLayers.insert(0, self.newlayer1)
            self.mapCanvas.setLayers(currentLayers)
            self.mapCanvas.refresh()
            print("new layer added")



def handler(msg_type, msg_log_context, msg_string):
    pass



def main():
    #QtCore.qInstallMessageHandler(handler) #bug with docklayer + paint. Suppress error messages for now
    QgsApplication.setPrefixPath("C:\\OSGeo4W64\\apps\\qgis", True)
    app = QgsApplication([], False)
    app.initQgis()


    firstWindow = Welcome()
    firstWindow.show()

    app.exec_()
    app.deleteLater()
    QgsApplication.exitQgis()


if __name__ == '__main__':
    main()