"""
flickrtest.py
"""
import flickrapi

def main():
  api_key = 'c46b3e3fafbd93634c980519af81e280'
  api_secret = 'db1a54bfd71dbcb2'

  flickr = flickrapi.FlickrAPI(api_key, api_secret)

  (token, frob) = flickr.get_token_part_one(perms='write')
  if not token: raw_input("Press ENTER after you authorized this program")
  flickr.get_token_part_two((token, frob))

  groups = flickr.groups_search(text = "Travel Photography")

  #import pdb; pdb.set_trace()

  f = open('flickrdataV2.txt',"w")
  photoCnt = 0
  userCnt = 0

  for group in groups.find('groups').findall('group'):
    users = flickr.groups_members_getList(group_id = group.attrib['nsid'])
    for user in users.find('members').findall('member'):
      userCnt += 1
      photos = flickr.people_getPublicPhotos(user_id = user.attrib['nsid'],\
      extras = "date_taken,geo,tags",per_page = '500')
      for photo in photos.find('photos').findall('photo'):
       if photo.attrib['latitude'] != '0'and photo.attrib['longitude'] != '0':
         photoCnt += 1
         result = "owner = {:s}, datetaken = {:s}, latitude = {:s}, longitude = {:s}\n"\
           .format(photo.attrib['owner'],photo.attrib['datetaken'],photo.attrib['latitude'],photo.attrib['longitude'])
         #print result
         f.write(result)
  print "{:d} geotagged photos mined from {:d} users.".format(photoCnt,userCnts)


  
  




if __name__ == '__main__':
    main()