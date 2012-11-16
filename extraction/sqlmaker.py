###
#sqlmaker.py
#export flickrdata to sqlight db
###
import sqlite3

def sqlexport(f,db):
    #parse raw file
    fp = open(f,"r")
    print db
    conn = sqlite3.connect(db)

    conn.execute("CREATE TABLE photos(\
                  photo_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                  latitude FLOAT,\
                  longitude FLOAT,\
                  datetime TIMESTAMP,\
                  owner VARCHAR(100));");
    conn.commit()
    for line in fp.readlines():
        fields = line.split(',')
        owner = fields[0].split(' ')[2]
        date = ' '.join((fields[1].split(' ')[3:5]))#datetime string
        latitude = fields[2].split(' ')[3]
        longitude = fields[3].split(' ')[3]
        conn.execute("INSERT INTO photos(latitude,longitude,datetime,owner)\
        VALUES (%s,%s,'%s','%s');" %\
                     (latitude,longitude,date,owner))
    conn.commit()
    conn.close()
    fp.close()




if __name__ == '__main__':
    sqlexport("flickrdataV2FINAL.txt","triplicant.db")
