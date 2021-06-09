import sqlite3
con = sqlite3.connect('video_details.db')
# create a cursor
c = con.cursor()
# create a table 
# c.execute("DROP TABLE videos")
c.execute("""
CREATE TABLE if not exists videos (
url text PRIMARY KEY,
title text, 
Thumbnail_image blob,
author text,
description text,
rating real,
views integer,
good_comments text,
bad_comments text, 
profanity_comments real,
path text,
subtitle text,
vid_text_predict real ,
vid_bad_words integer,
resolution text
)
""")
# NULL
# INTEGER
#REAL(DEIMAL)
# TEXT
#BLOB "like images and music videos"
# commit our command
con.commit()
con.close()

