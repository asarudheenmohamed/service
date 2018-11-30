# https:
#     //maps.googleapis.com / maps / api / geocode / json?key = AIzaSyBgXEjOMJU2_XAnuI6mv6pREmieM639Gh8 & address = "Sithalapakam post , Nookampalayam, Chennai, Tamil Nadu, India"


# https:
#     //geocoder.cit.api.here.com / 6.2 / geocode.json?app_id = u8XrvtBsdETuyfqbfQSr & app_code = 48ec7l83gZeMaaMPxpiRsQ & searchtext = "Sithalapakam post , Nookampalayam, Chennai, Tamil Nadu, India"

import geopy.distance
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyBgXEjOMJU2_XAnuI6mv6pREmieM639Gh8')
best_loc = None
import pandas as pd
from app.core.models.customer import address


def is_more_accurate(res2, res1):
    vp = res2['geometry']['viewport']

    n2, e2, s2, w2 = \
        vp['northeast']['lat'], vp['northeast']['lng'], vp[
            'southwest']['lat'], vp['southwest']['lng']

    vp = res1['geometry']['viewport']
    n1, e1, s1, w1 = \
        vp['northeast']['lat'], vp['northeast']['lng'], vp[
            'southwest']['lat'], vp['southwest']['lng']

    if n2 <= n1 and e2 <= e1 and s2 >= s1 and w2 >= w1:
        return True

    return False


def geocode(query_components):
    # best_loc = None

    # for query in query_components:

    # sub_query = re.sub('Tam.*?India', '', query)
    # global best_loc
    query = query_components
    result = gmaps.geocode(query)

    result = result[0]
    if 'bounds' in result['geometry']:
        vp = result['geometry']['bounds']
    else:

        vp = result['geometry']['viewport']
    n1, e1, s1, w1 = \
        vp['northeast']['lat'], vp['northeast']['lng'], vp[
            'southwest']['lat'], vp['southwest']['lng']

    print("{}: bounding box distance {}".format(
        query,
        geopy.distance.geodesic((n1, e1), (s1, w1))
    ))
    km_ = geopy.distance.geodesic((n1, e1), (s1, w1)).km

    # print km_, '[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[['
    # import pdb
    # pdb.set_trace()
    # if not best_loc:
    #     best_loc = result
    # else:
    #     if is_more_accurate(result, best_loc):
    #         print("Found a better result with {}".format(query))
    #         best_loc = result

    return result, km_


query_components = [
    ('Perumbakkam, Tamil Nadu, India',
     'Flat no. 8403, Embassy Residency,Perumbakkam, Tamil Nadu, India'
     ), ('Kavery street, kalakshetra colony, besant nagar,chennai', 'Vaigai St, Kalakshetra Colony, Besant Nagar, Chennai, Tamil Nadu 600090, India'), ('Plot No 9,Door No 12, Ramachandran Street,Shanthi Avenue,Chitlapakkam, Chennai, Tamil Nadu, India', 'Chitlapakam Chennai, Tamilnadu, 600073')]

# query_components = [
#     ('Plot No 9,Door No 12, Ramachandran Street,Shanthi Avenue,Chitlapakkam, Chennai, Tamil Nadu, India',
#      'Chitlapakam Chennai, Tamilnadu, 600073')]

# query_components = [("flat nno112 block 1 siddarth natural",
#                      "flat nno112 block 1 siddarth natural appts bhbl nagar medavakam 600100,medavakam")]


def fetch_location(query_components):
    import re
    list_ = []
    for query_component in query_components:
        best_loc = None
        radious_km = None
        sub_query, query = query_component
        obj, km_ = geocode(query)
        if not best_loc:
            best_loc = obj
            radious_km = km_
        if km_ > 0.5:
            sub_query = re.sub('Tam.*?India', '', sub_query)
            for i in reversed(sub_query.split(',')):

                obj, km_ = geocode(i + query)
                if is_more_accurate(obj, best_loc):
                    print("Found a better result with {}".format(query))
                    best_loc = obj
                    radious_km = km_

        # else:
        # import pdb
        # pdb.set_trace()
        list_.append(
            (query, radious_km, "{},{}".format(
                best_loc["geometry"]["location"]["lat"],
                best_loc["geometry"]["location"]["lng"])))

    # import pdb
    # pdb.set_trace()
    df = pd.DataFrame(list_)
    df.to_csv('address.csv', header=['Address', 'radious_km', 'location'])
    # print list_, '[[[[[[[[[[[[[[[[[[[[[[[[[[[[['
    return list_


def fetch_geo_location():
    address_obj = address.CustomerAddressEntityText.objects.filter(
        attribute__attribute_id=25)[:100].values_list('value')
    query_components = []

    for obj in address_obj:
        query_components.append(tuple(obj[0].split('\n')))

    y = fetch_location(query_components)
