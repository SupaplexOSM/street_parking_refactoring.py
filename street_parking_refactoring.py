#------------------------------------------------------------------------------#
#   Save street parking data with customized attribute table.                  #
#                                                                              #
#   > version/date: 2025-06-27                                                 #
#------------------------------------------------------------------------------#

from qgis.core import *
from os.path import exists
import os, processing, time

#working directory, see https://stackoverflow.com/a/65543293/729221
from console.console import _console
dir = _console.console.tabEditorWidget.currentWidget().path.replace("street_parking_refactoring.py","")
dir_input = dir + 'data/output/street_parking.gpkg'
dir_output = dir + 'data/output/'

#read street parking file from street_parking.py output folder
print(time.strftime('%H:%M:%S', time.localtime()), 'Read street parking file...')
if not exists(dir_input):
    print(time.strftime('%H:%M:%S', time.localtime()), '[!] Error: Found no valid street parking file at "' + dir_input + '".')
else:
    layer_parking = QgsVectorLayer(dir_input + '|geometrytype=LineString', 'street parking', 'ogr')

    print(time.strftime('%H:%M:%S', time.localtime()), 'Reproject layer...')
    layer_parking = processing.run('native:reprojectlayer', { 'INPUT' : layer_parking, 'TARGET_CRS' : QgsCoordinateReferenceSystem("EPSG:4326"), 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), 'Refactor fields...')
    layer_parking = processing.run('native:refactorfields', { 'FIELDS_MAPPING' :
    [
        {'expression': '\"id\"','length': 0,'name': 'ID','precision': 0,'type': 10},
        {'expression': '\"highway:name\"','length': 0,'name': 'Straßenname','precision': 0,'type': 10},
        {'expression': 'if(\"highway\" = \'primary\', \'Hauptverbindungsstraße (OSM-Typ 1)\', if(\"highway\" = \'secondary\', \'Hauptverbindungsstraße (OSM-Typ 2)\', if(\"highway\" = \'tertiary\', \'Hauptverbindungsstraße (OSM-Typ 3)\', if(\"highway\" = \'primary_link\' OR \"highway\" = \'secondary_link\' OR \"highway\" = \'tertiary_link\', \'Hauptverbindungsstraße (Verbindungsweg)\', if(\"highway\" = \'residential\', \'Wohnstraße\', if(\"highway\" = \'living_street\', \'Verkehrsberuhigter Bereich\', if(\"highway\" = \'pedestrian\', \'Fußgängerstraße\', if(\"highway\" = \'service\', \'Zufahrtsweg\', if(\"highway\" = \'track\', \'Wirtschaftsweg\', \'Unbestimmte Straße\')))))))))','length': 0,'name': 'Straßenkategorie','precision': 0,'type': 10},
        {'expression': 'if(\"highway:oneway\" = \'yes\', \'Ja\', if(\"highway:oneway\" = \'no\', \'Nein\', NULL))','length': 0,'name': 'Einbahnstraße','precision': 0,'type': 10},
        {'expression': 'if(\"parking\" = \'lane\', \'Fahrbahn\', if(\"parking\" = \'street_side\', \'Parkbucht\', if(\"parking\" = \'on_kerb\', \'Gehweg\', if(\"parking\" = \'half_on_kerb\', \'Gehweg (halb)\', if(\"parking\" = \'shoulder\', \'Seitenstreifen\', \'Sonstiges/Unbestimmt\')))))','length': 0,'name': 'Parkposition','precision': 0,'type': 10},
        {'expression': 'if(\"orientation\" = \'parallel\', \'Parallelparken\', if(\"orientation\" = \'diagonal\', \'Schrägparken\', if(\"orientation\" = \'perpendicular\', \'Querparken\', \'Unbestimmt\')))','length': 0,'name': 'Ausrichtung','precision': 0,'type': 10},
        {'expression': '\"capacity\"','length': 4,'name': 'Anzahl der Stellplätze','precision': 0,'type': 2},
        {'expression': 'if(\"surface\" = \'asphalt\', \'Asphalt\', if(\"surface\" = \'sett\' OR \"surface\" = \'cobblestone\' OR \"surface\" = \'cobblestone\', \'Steinpflaster\', if(\"surface\" = \'unhewn_cobblestone\', \'Kopfsteinpflaster (unbehauen)\', if(\"surface\" = \'paving_stones\', \'Verbundpflaster\', if(\"surface\" = \'concrete\', \'Beton\', if(\"surface\" = \'concrete:plates\' OR \"surface\" = \'concrete:lanes\', \'Betonplatten\', if(\"surface\" = \'grass_paver\', \'Rasengittersteine\', if(\"surface\" = \'compacted\', \'unbefestigter, verdichteter Untergrund\', if(\"surface\" = \'fine_gravel\', \'Splitt\', if(\"surface\" = \'gravel\', \'Schotter\', if(\"surface\" = \'pebblestone\', \'Kies\', if(\"surface\" = \'rock\', \'Stein\', if(\"surface\" = \'ground\' OR \"surface\" = \'dirt\' OR \"surface\" = \'earth\', \'unbefestigter Boden\', if(\"surface\" = \'grass\', \'Gras\', if(\"surface\" = \'paved\', \'Versiegelt (unbestimmt)\', \'Sonstiges/Unbestimmt\')))))))))))))))','length': 0,'name': 'Oberfläche','precision': 0,'type': 10},
        {'expression': 'replace(\"condition_class\", array(\' @ \', \'free\', \'paid\', \'residents\', \'mixed\', \'time_limited\', \'loading\', \'charging\', \'disabled_private\', \'disabled\', \'taxi\', \'car_sharing\', \'vehicle_restriction\', \'access_restriction\', \'no_parking\', \'no_stopping\', \'Tu\', \'We\', \'Th\', \'Su\', \'PH\', \'SH\', \'Mar\', \'May\', \'Oct\'), array(\' \', \'Kostenfreies Parken\', \'Mit Parkschein\', \'Mit Bewohnerparkausweis\', \'Mit Bewohnerparkausweis oder Parkschein\', \'Parkscheibe\', \'Ladezone\', \'Laden von Elektrofahrzeugen\', \'personenbezogener Behindertenparkplatz\', \'Behindertenparkplatz\', \'Taxenstand\', \'Carsharing\', \'Fahrzeugbeschränkung\', \'Nutzerbeschränkung\', \'Eingeschränktes Haltverbot\', \'Absolutes Haltverbot\', \'Di\', \'Mi\', \'Do\', \'So\', \'Feiertags\', \'Schulferien\', \'Mär\', \'Mai\', \'Okt\'))','length': 0,'name': 'Parkraumangebot','precision': 0,'type': 10},
        {'expression': 'replace(\"vehicle_designated\", array(\' @ \', \'motorcar\', \'disabled\', \'bus\', \'taxi\', \'psv\', \'hgv\', \'goods\', \'car_sharing\', \'emergency\', \'motorhome\', \'Tu\', \'We\', \'Th\', \'Su\', \'PH\', \'SH\', \'Mar\', \'May\', \'Oct\'), array(\' \', \'Pkw\', \'Mit Schwerbehindertenausweis\', \'Busse\', \'Taxi\', \'Personenverkehr\', \'Lkw\', \'Transporter\', \'Carsharing\', \'Einsatz-/Rettungsfahrzeuge\', \'Wohnmobile\', \'Di\', \'Mi\', \'Do\', \'So\', \'Feiertags\', \'Schulferien\', \'Mär\', \'Mai\', \'Okt\'))','length': 0,'name': 'Fahrzeugbeschränkungen','precision': 0,'type': 10},
        {'expression': '\"zone\"','length': 0,'name': 'Parkzone','precision': 0,'type': 10},
        {'expression': 'if(\"markings\" = \'no\', \'Keine\', if(\"markings:type\" = \'lane\' OR \"markings:type\" = \'lane:dots\' OR \"markings:type\" = \'surface\', \'Ja (Parkstreifenmarkierung)\', if(\"markings:type\" IS NOT NULL, \'Ja (Einzelstellplatzmarkierung)\', if(\"markings\" = \'yes\', \'Ja (unbestimmt)\', NULL))))','length': 0,'name': 'Markierungen','precision': 0,'type': 10},
        {'expression': '\"width\"','length': 3,'name': 'Parkstreifenbreite','precision': 1,'type': 6},
        {'expression': 'if(\"location\" = \'median\', \'Mittelstreifen\', if(\"location\" = \'lane_centre\', \'Fahrbahnmitte\', NULL))','length': 0,'name': 'Besondere Lagemerkmale','precision': 0,'type': 10},
        {'expression': 'if(\"informal\" = \'yes\', \'Ja\', if(\"informal\" = \'no\', \'Nein\', NULL))','length': 0,'name': 'Informelles Parken','precision': 0,'type': 10},
        {'expression': 'if(\"operator:type\" = \'private\', \'Privat\', if(\"operator:type\" = \'public\', \'Öffentlich\', if(\"operator:type\" IS NOT NULL, \'Sonstiges\', NULL)))','length': 0,'name': 'Rechtliche Zuordnung','precision': 0,'type': 10}
    ], 'INPUT' : layer_parking, 'OUTPUT' : dir_output + 'street_parking_refactored.geojson' })
    print(time.strftime('%H:%M:%S', time.localtime()), 'Completed.')