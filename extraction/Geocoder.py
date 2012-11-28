
import httplib,json,time
BASE_URL = "maps.googleapis.com"
class Geocoder:
    def reverse(self,latlong):
        conn = httplib.HTTPConnection(BASE_URL)
        rstring = "/maps/api/geocode/json?latlng=%f,%f&sensor=true" % latlong
        conn.request("GET",rstring)
        r = conn.getresponse()
        j = json.loads(r.read())
        import pdb; pdb.set_trace()
        if not j['results']:
            time.sleep(2)#rate limited, messy but it works
            return self.reverse(latlong)
        for result in j['results']:
           if 'locality' in result['types']:
               return result['formatted_address']
           elif 'route' in result['types'] or 'street_address' in result['types']:
               comps = result['formatted_address'].split(',')[1:]
               if len(comps) > 1:
                   placename = []
                   for comp in comps:
                       words = comp.split(' ')
                       newcomp = []
                       for word in words:
                           if word and not word.isdigit():#strip digits
                               newcomp.append(word.strip(', '))
                       placename.append(' '.join(newcomp))
                   return ','.join(placename)
               else: return result['formatted_address']
           elif 'sublocality' in result['types']:
               return "JAPAN: ",result['formatted_address']


if __name__ == '__main__':
    g = Geocoder()
    print g.reverse((-9.41657248543689, 159.91543592233))
