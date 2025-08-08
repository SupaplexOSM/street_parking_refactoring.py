#------------------------------------------------------------------------------#
#   Save street parking data with customized attribute table.                  #
#                                                                              #
#   > version/date: 2023-02-20                                                 #
#------------------------------------------------------------------------------#

from qgis.core import *
from os.path import exists
import os, processing, time

#working directory, see https://stackoverflow.com/a/65543293/729221
from console.console import _console
dir = _console.console.tabEditorWidget.currentWidget().path.replace("street_parking_refactoring_off_street.py","")
dir_input = dir + 'data/refactoring/export_off_street_parking.geojson'
dir_output = dir + 'data/refactoring/output/'

#read street parking file from street_parking.py output folder
print(time.strftime('%H:%M:%S', time.localtime()), 'Read street parking file...')
if not exists(dir_input):
    print(time.strftime('%H:%M:%S', time.localtime()), '[!] Error: Found no valid street parking file at "' + dir_input + '".')
else:
    layer_parking = QgsVectorLayer(dir_input + '|geometrytype=Polygon', 'off street parking', 'ogr')
    print(time.strftime('%H:%M:%S', time.localtime()), 'Refactor fields...')
    layer_parking = processing.run('native:refactorfields', { 'FIELDS_MAPPING' :
    [
        {'expression': '\"id\"','length': 0,'name': 'ID','precision': 0,'type': 10},
        {'expression': 'if(\"parking\" = \'surface\', \'Parkplatz\', if(\"parking\" = \'multi-storey\', \'Parkhaus\', if(\"parking\" = \'underground\', \'Tiefgarage\', \'Sonstiges\')))','length': 0,'name': 'Objektart','precision': 0,'type': 10},
        {'expression': '\"capacity\"','length': 4,'name': 'Anzahl der Stellplätze','precision': 0,'type': 2},
        {'expression': 'if(\"access\" = \'yes\', \'Öffentlich\', if(\"access\" = \'private\', \'Privat\', if(\"access\" = \'customers\', \'Kunden\', if(\"access\" = \'permissive\', \'Öffentlich geduldet\', if(\"access\" = \'no\', if(\"motorcar\" = \'designated\' OR \"motorcar\" = \'yes\', \'Öffentlich (nur Pkw)\', if(\"disabled\" = \'designated\' OR \"disabled\" = \'yes\', \'Öffentlich (Behindertenparkplatz)\', \'Unbestimmt\')), \'Unbestimmt\')))))','length': 0,'name': 'Zugänglichkeit','precision': 0,'type': 10},
        {'expression': 'if(\"private\" = \'residents\', \'Anwohner\', if(\"private\" = \'employees\', \'Mitarbeiter\', if(\"private\" = \'commercial\', \'Gewerbe\', \'Unbestimmt\')))','length': 0,'name': 'Nutzergruppe','precision': 0,'type': 10},
        {'expression': 'if(\"fee\" = \'yes\', \'Ja\', if(\"fee\" = \'no\', \'Nein\', \'Keine Angabe\'))','length': 0,'name': 'Parkgebühren','precision': 0,'type': 10},
        {'expression': 'if(\"maxstay\" IS NULL, \'Keine\', replace(\"maxstay\", array(\'hour\', \'hours\', \'minute\', \'minutes\', \'day\', \'days\'), array(\'Stunde\', \'Stunden\', \'Minute\', \'Minuten\', \'Tag\', \'Tage\')))','length': 0,'name': 'Höchstparkdauer','precision': 0,'type': 10},
        {'expression': 'if(\"maxweight\" IS NULL, \'Keine Beschränkung\', \"maxweight\")','length': 0,'name': 'Zulässiges Fahrzeuggewicht','precision': 0,'type': 10},
        {'expression': 'if(\"restriction\" = \'charging_only\', \'Laden von Elektrofahrzeugen\', if(\"restriction\" = \'loading_only\', \'Ladezone\', \'Keine\'))','length': 0,'name': 'Sonstige Parkbeschränkungen','precision': 0,'type': 10},
        {'expression': 'if(\"surface\" = \'asphalt\', \'Asphalt\', if(\"surface\" = \'sett\' OR \"surface\" = \'cobblestone\' OR \"surface\" = \'cobblestone\', \'Steinpflaster\', if(\"surface\" = \'unhewn_cobblestone\', \'Kopfsteinpflaster (unbehauen)\', if(\"surface\" = \'paving_stones\', \'Verbundpflaster\', if(\"surface\" = \'concrete\', \'Beton\', if(\"surface\" = \'concrete:plates\' OR \"surface\" = \'concrete:lanes\', \'Betonplatten\', if(\"surface\" = \'grass_paver\', \'Rasengittersteine\', if(\"surface\" = \'compacted\', \'unbefestigter, verdichteter Untergrund\', if(\"surface\" = \'fine_gravel\', \'Splitt\', if(\"surface\" = \'gravel\', \'Schotter\', if(\"surface\" = \'pebblestone\', \'Kies\', if(\"surface\" = \'rock\', \'Stein\', if(\"surface\" = \'ground\' OR \"surface\" = \'dirt\' OR \"surface\" = \'earth\', \'unbefestigter Boden\', if(\"surface\" = \'grass\', \'Gras\', if(\"surface\" = \'paved\', \'Versiegelt (unbestimmt)\', \'Sonstiges/Unbestimmt\')))))))))))))))','length': 0,'name': 'Oberfläche','precision': 0,'type': 10},
        {'expression': 'if(\"traffic_sign\" IS NULL, \'Keins\', \"traffic_sign\")','length': 0,'name': 'Verkehrszeichen','precision': 0,'type': 10},
        {'expression': 'if(\"markings\" = \'no\', \'Keine\', if(\"markings:type\" = \'lane\' OR \"markings:type\" = \'lane:dots\' OR \"markings:type\" = \'surface\', \'Ja (Parkstreifenmarkierung)\', if(\"markings:type\" IS NOT NULL, \'Ja (Einzelstellplatzmarkierung)\', if(\"markings\" = \'yes\', \'Ja (unbestimmt)\', \'Keine Angabe\'))))','length': 0,'name': 'Markierungen','precision': 0,'type': 10},
        {'expression': 'if(\"operator:type\" = \'private\', \'Privat\', if(\"operator:type\" = \'public\', \'Öffentlich\', if(\"operator:type\" IS NOT NULL, \'Sonstiges\', NULL)))','length': 0,'name': 'Rechtliche Zuordnung','precision': 0,'type': 10}
    ], 'INPUT' : layer_parking, 'OUTPUT' : dir_output + 'parking_off_street_residential_refactored.geojson' })
    print(time.strftime('%H:%M:%S', time.localtime()), 'Completed.')