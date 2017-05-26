#!/usr/bin/python
import os
import hashlib
import MySQLdb
from time import gmtime, strftime

#--- -----------------------------
""" 
1.SCRIPT UNTUK AMBIL DATA DARI MYSQL DATABASE DAN BENTUK MENJADI FILE A
CONTOH FILE A : 
-----------------------------
3470a43e0fa7031d413a8efdeab0d923  /bin/ping4
73a662fa1882854dcec652e2b6cb55b7  /bin/ntfsls
-----------------------------
2.SCRIPT UNTUK INPUT DATA KE TABEL MYSQL 
CONTOH DIBAWAH : masukkandata() dan masukkandata1().
"""
#--- -----------------------------
#--- FUNGSI fwrite() dan FUNGSI tulislog 
#--- KEDUA FUNGSI sama2 membuat file baru jika file (fl) tidak ditemukan 
def fwrite(fl,s):
	f = open(fl, "a+")
	f.write(s+"\n")
	f.close
def tulislog(fl,s):
	try:
		f = open(fl,'a+')
		f.write(s+"\n")
	except:
		f = open(fl,'w')
	f.close
#--- -------------------------------

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="yourpass",  # your password
                     db="dbfilelist")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
# --- ----FOR QUERY DATA -----
def strquery(sql):
	cur.execute(sql)
	cur.fetchall()
	db.commit()
	print " Suksesss Process Data..."
# --- ----CHECKING DATA -----
def checkdata(s):
	#cur.execute("SELECT COUNT(1) FROM tflist1 WHERE flist like '%"+s+"%'") # yang ini OK, Hampir Perfect
	cur.execute("SELECT COUNT(1) FROM tflist1 WHERE flist like '"+s+"%'")		
	if cur.fetchone()[0]:
		return "1"
	else:
		return "0"
# --- ----END CHECKING DATA -----
# --- ----FOR QUERY SHOW DATA -----
def showquery(sql):
	cur.execute(sql)	
	print "-----------------------------------------"
	for row in cur.fetchall():
			print row[2] + "  " + row[1]
	#db.commit()
	print "-----------------------------------------"
# --- ----END FOR QUERY SHOW DATA -----
# --- -------SHOW DATA ----- OK
def showdata():
	#cur.execute("SELECT * FROM tflist1 WHERE flist like '%TESSS%'")
	cur.execute("SELECT * FROM tflist1")
	for row in cur.fetchall():
		print row[2] +"  " + row[1]
	print "--------END---DATA-----------"
# --- ------END SHOW DATA -----

# --- ----- INSERT DATA TEST---------- OK
def tesmasukkandata():
	cur.execute("INSERT INTO `tflist1` (id, `flist`, `hash`,`addt`) VALUES (1111111, 'tes-TESSSSS.conf', 'TESSSSa5221', '2017-03-28 17:39')")
	cur.fetchall()
	db.commit()
	print " Suksesss Tes Input Data..."
# --- ------- END INSERT DATA ---------

# --- ------TES Input Data From Another Process -----
def masukkandata(d1,d2):
	d3 = strftime("%Y-%m-%d %H:%M", gmtime())
	cur.execute("INSERT INTO `tflist1` (id, `flist`, `hash`,`addt`) VALUES (null, '"+d1+"','"+d2+"','"+d3+"')")
	cur.fetchall()
	db.commit()
	#print " Suksesss Input Data..."
# --- ------END Input Data ----------


# --- -------FUNCTION VERSION LIST-DIR--------
# --- -----Fungsi untuk meng-LIST File dalam Direktori-------
def processDirectory ( args, dirname, filenames ):
    for filename in filenames:
		dirfile = dirname+"/"+filename
		if os.path.isfile(dirfile):
			if checkdata(dirfile) == "0":
				fwrite("newdata.txt",dirfile)
				try:
					md = hashlib.md5(open(dirfile,'rb').read()).hexdigest()
					masukkandata(dirfile,md)
				except:
					masukkandata("FILE READ ERROR---BLANK","HASH BLANK")
			else:
				#print "SUDAH : "+ dirfile
				fwrite("olddata.txt",dirfile)


def listDir(direktori):
	base_dir = direktori
	os.path.walk( base_dir, processDirectory, None )

#s = raw_input("Pilih Direktori : ")
#listDir(s)
# --- ------END FUNCTION LIST DIR-------------

print "\t 1.Tampilkan Data\n\t 2.Tes Operasi Data\n\t \
3.Input Data From A Directory\n\t 4.Delete All Data From tflist1\n\t \
5.Tes Create File\n----------------------------------"

s = raw_input("Pilih No ? ")

if s == "1":
	showdata()

elif s == "2":
	#tesmasukkandata()
	s = raw_input("Input file path (exp:/home/tes.txt) : ")
	#showquery("SELECT * FROM tflist1 WHERE flist like '%"+s+"%'")
	checkdata(s)

elif s == "3":
	s = raw_input("Input Direktori (exp:/home) : ")
	if s != " " or s != "":
		listDir(s)	
		print " Selesai, Suksesss Input Data..."

elif s == "4":
	dt = 'tflist1'
	strquery("TRUNCATE TABLE "+ dt)
	showdata()
	
elif s == "5":
	fwrite("tx.x","X : ini hanya coba From frwrite()")
	tulislog("ty.y","Y : ini Hanya Coba From Tulislog().")

else:
	 quit()

print "-------------------------------------------------"
print "Selesai.s...."

db.close()
