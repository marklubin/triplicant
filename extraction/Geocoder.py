
import httplib,json,time,secret

TIMEOUT = 5
BASE_URL = "api.geonames.org"

class PyGeoNames:
    def reverse(self,latlong):
        tries = 0
        while tries < TIMEOUT:
            conn = httplib.HTTPConnection(BASE_URL)
            rstring = "/findNearbyPlaceNameJSON?lat=%f&lng=%f&username=%s" % (latlong[0],latlong[1],secret.UNAME)
            conn.request("GET",rstring)
            r = conn.getresponse()
            j = json.loads(r.read())
            if 'geonames' not in j.keys():
                tries += 1
                continue

            results = j['geonames'][0]

            return "%s,%s" % (results['name'],results['countryName'])

        return "NO PLACE_NAME FOUND"

    def timezone(self,latlong):
         tries = 0
         while tries < TIMEOUT:
            conn = httplib.HTTPConnection(BASE_URL)
            rstring = "/timezoneJSON?lat=%f&lng=%f&username=%s" % (latlong[0],latlong[1],secret.UNAME)
            conn.request("GET",rstring)
            r = conn.getresponse()
            j = json.loads(r.read())
            if 'timezoneId' not in j.keys():
                tries += 1
                continue
            return j['timezoneId']
         return "NO TIMEZONE FOUND"


if __name__ == '__main__':
    g = PyGeoNames()
    print g.timezone((42.3792686552198,-71.0818139711539))
