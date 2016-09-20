import xml.etree.ElementTree as ET, urllib.request, gzip, io
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

def getEarthMass(elem):
        return round(float(elem.findtext("mass")), 3) * 317.8 if elem.findtext("mass") else 0

def getEarthRadius(elem):
        return round(float(elem.findtext("radius")), 3) * 11.209 if elem.findtext("radius") else 0

def getSemiMajorAxis(elem):
        return elem.findtext("semimajoraxis") if elem.findtext("semimajoraxis") else 0

def getSurfaceG(elem):

    if elem.findtext("radius") and elem.findtext("mass"):

        earthMass = getEarthMass(elem)
        earthRadius = getEarthRadius(elem)
        return earthMass / (earthRadius * earthRadius)

    else:
        return 0

for planet in sorted(oec.findall(".//planet"), key = getSurfaceG):

    g = getSurfaceG(planet)
    mass = getEarthMass(planet)
    radius = getEarthRadius(planet)

    if planet.findtext("mass") and planet.findtext("radius") and getEarthMass(planet) > 0.5 and getEarthMass(planet) < 2:
        print([planet.findtext("name"), str(getEarthMass(planet)) +" Earth masses", str(getEarthRadius(planet)) + " Earth radii", str(g) + "g", "Semi-major axis: " + str(getSemiMajorAxis(planet))])
