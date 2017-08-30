
import os
import hashlib
#import MySQLdb # access mysql for linux
import pymysql # access mysql for Windows
import sqlite3
from time import gmtime, strftime
from termcolor import colored
from colorama import init
import sys
import shutil
import datetime
import ntpath
import glob



init()
#-----------------------
#--- Script Ini OK di TEST di WINDOWS 10 System ---
#-----------------------

##------GLOBAL VAR----------
up = os.path.expanduser('~') + "\\" # For Linux System
wd = os.getcwd() + "\\"
win_dir = os.environ['WINDIR'] + "\\"
sys_dir = os.environ['WINDIR'] + "\\System\\"
file_collec =[]

g_db = 'winflist'
g_table = 'tflist1'
a,b,c,t,jr,rowsc = 0,0,0,0,"20",0	# tampung jumlah file renamed, digunakan di fungsi ren_findir()
					# b dan c untuk hitung data ADA dan TIADA dalam DB t untuk total data
					# lp : untuk menampung data lastpage/current page
tdb = False	
#odb = None				
##--------DB-CONFIG-Local-------
	
try:
	print ("""
  Anda dapat mengisi database secara manual atau memilih salah satu :
  Ketik 'Y' atau 'y'		: input other host, user, pass dan database manual 
  Ketik 'L' atau 'l'		: otomatis akses databases hasil configurasi dalam script ini
  Ketik 'X' atau 'x'		: Kembali / Exit.
----------------------------
	""")
	pilih_db = input("  Change Conf Database ? \t: ")
	if pilih_db == 'y' or pilih_db == 'Y':
		host_db = input("  Input Host Name \t: ")
		user_db = input("  Input User Name \t: ")
		pass_db = input("  Input Pass User \t: ")
		data_bs = input("  Input DtBs Name \t: ")
		#port_nm = input("  Input Port Numb \t: ")
		db = pymysql.connect(host=host_db,	# your host, usually localhost /in windows use 127.0.0.1
				 user=user_db,		        # your username
				 passwd=pass_db,			# your password
				 db=data_bs)		        # name of the data base
		odb = db.cursor()
		tdb = True
	elif pilih_db == 'L' or pilih_db == 'l':
		db = pymysql.connect(host="127.0.0.1",    # your host, usually localhost /in windows use 127.0.0.1
                     user="root",         # your username
                     passwd="",  # your password
                     db=g_db)        # name of the data base
		odb = db.cursor()
		tdb = True
	else:
		#con_to_db() # menggunakan funsi ini terasa lambat saat load data 
		#con_to_db_E() # menggunakan funsi ini terasa lambat saat load data 
		db = pymysql.connect(host="localhost",    # your host, usually localhost /in windows use 127.0.0.1
                     user="root",         # your username
                     passwd="password",  # your password
                     db = g_db)        # name of the data base
		odb = db.cursor()
		tdb = True
		#pass
except:
	print ("------------------------------------")
	print (colored("  GAGAL Mengakses MySQL Database !!!","red"))
	print ("------------------------------------")
	pass
# you must create a Cursor object. It will let
#  you execute all the queries you need

##--------END DB-CONFIG----
# --- ----FOR QUERY DATA -----
def strquery(sql):
	odb.execute(sql)
	odb.fetchall()
	db.commit()
	print (" Suksesss Process Data...")

def is_date(dt):
	dt = dt.replace('-','')
	if dt.isdigit():
		#print dt
		return True
		
# --- ----UPDATE DATA -----		
def updata(s1):	
	cur.execute("UPDATE `"+g_table+"` SET shash='"+hstr(s1)+"' WHERE id=id")
	cur.fetchall()
	db.commit()
	#print " Suksesss Input Data..."
# --- ----END UPDATE DATA -----	
def hitung_data(cr):
	cr = cr.replace(' ','%')
	odb.execute('SELECT COUNT(*) FROM `'+g_table+'` WHERE flist like "%'+cr+'%" OR addt like "%'+cr+'%"')
	row_count = odb.fetchone()[0]
	#print row_count
	return str(row_count)
	
def check_showdata_bu(cr,p): # ini FUN yg ASLI ---
	jr = "20"
	c = 0
	pg = (int(p) * int(jr)) - int(jr)
	print ("---------PAGE :"+colored(str(p),'red')+" ------------")
	if cr != "":
		odb.execute('SELECT id, flist, shash FROM `'+g_table+'` WHERE flist like "%'+cr+'%" ORDER BY flist LIMIT '+str(pg)+','+jr)
	else:
		odb.execute('SELECT id, flist, shash FROM `'+g_table+'` LIMIT '+str(pg)+','+jr)
	for row in odb.fetchall():
		print (colored(" "+str(row[0]) +"\t : " + row[3][:3]+".."+row[3][-5:-1] + " : " + row[2][:3] +".."+ row[2][-4:]+" : " + row[1],"yellow"))
		c = c+1
	if c == 0:
		print (colored("  Data Not Found !, It's EMPTY Rows ... !",'red'))
	print ("---------END PAGE :"+colored(str(p),'red')+" ------------")
		
def check_showdata(cr,p): # ini FUN yg untuk di-MODIF
	global c,jr,rowsc #,odb
	c = 0
	pg = (int(p) * int(jr)) - int(jr)
	rowsc = int(hitung_data(cr))
	if rowsc > 0:
		
		print ("--- PAGE :"+colored(str(p),'red')+", rows "+colored(str(pg),'red')+" of "+colored(str(rowsc),'red')+" Found -----")  #STR_TO_DATE(addt, \'%Y-%m-%d %H:%M:%S\'))
		if cr != "":		
			odb.execute('SELECT id, flist, addt, shash FROM `'+g_table+'` WHERE flist like "%'+cr+'%" OR addt like "%'+cr+'%" ORDER BY addt LIMIT '+str(pg)+','+jr)
		else:
			odb.execute('SELECT id, flist, addt, shash FROM `'+g_table+'` LIMIT '+str(pg)+','+jr)
		for row in odb.fetchall():
			c = c+1
			if (c % 2 == 0):
				print (colored(" "+str(row[0]) +"\t : " + str(row[2])[:10]+ " : " + row[3][:6] +" : " + row[1],'cyan')) 
			else:
				print (colored(" "+str(row[0]) +"\t : " + str(row[2])[:10]+ " : " + row[3][:6] +" : " + row[1],'yellow'))
		crow = pg + int(c)
		#if c == 0:
		#	print colored("   It's EMPTY Rows ... !",'red')
		print ("--- PAGE :"+colored(str(p),'red')+", rows "+colored(str(crow),'red')+" of "+colored(str(rowsc),'red')+" Found -----")
	else:
		print (colored("   It's EMPTY Rows ... !",'red'))
		

def del_alldata():
	conf = input('  Delete All Rows in "'+g_table+'" ? [y/Y] : ')
	if conf == 'y' or conf == 'Y':
		odb.execute('DELETE FROM tflist1')
		db.commit()
		print ('  All Rows in "'+g_table+'" Table, has been DELETED !')
		

###=========================================================###
def hash_file(f):
	#return hashlib.md5(f).hexdigest()
	if os.path.isfile(f):
		#return hashlib.md5(open(f,'rb').read()).hexdigest()
		return hashlib.sha1(open(f,'rb').read()).hexdigest()
	else:
		#print colored("   "+f+", is not a File !","red")
		#pass 
		return "no"
	
def write_2file(fl,s):
	try:
		f = open(fl,'a+')
		f.write(s+"\n")
		#f.write(s)
		print (colored(' Write : "'+s[:12]+'...", to file : '+fl,'green'))
	except:
		f = open(fl,'w')
	f.close

def create_bat_shrcut(f,sf):
	try:
		f = open(f,'w')
		f.write('@echo off\n')
		f.write('python '+sf+'list-all-file-3.py\n')
		#print (' Success Create bat file : '+f)
	except:
		f = open(f,'w')
	f.close		

def clear_2file(fl,s):
	try:
		f = open(fl,'w')
		f.write(s)
		print (' Clear file : '+fl)
	except:
		f = open(fl,'w')
	f.close
				
"""
Fungsi listallfile_wtf : fungsi untuk melakukan list all file dan,
wtf adalah Write to File, fungsi ini menghasilkan report berupa file output.txt
"""

def listallfile_wtf(dr):
	with open("output.txt", "w") as a:
		for path, subdirs, files in os.walk(dr):
			for filename in files:
				f = os.path.join(path, filename)
				#print str(f) + os.linesep
				print (f)
				#print path
				a.write(str(f) + os.linesep)
			a.close
		print (" --- SELESAI ---")


def chstr1(s):
	global up
	#up = os.path.expanduser('~')
	file = open(up+'/mytool.txt', 'r')
	ln = file.read()
	file.close()
	ln = ln.split()
	if ln[0] in s:
		hs = s.replace(ln[0],'')
	elif ln[1] in s:
		hs = s.replace(ln[1],'')
	elif ln[2] in s:
		hs = s.replace(ln[2],'')
	else:
		hs = s
	return hs

def chstr2(s):
	global up
	#up = os.path.expanduser('~')
	file = open(up+'/mytool.txt', 'r')
	ln = file.read()
	file.close()
	ln = ln.split()
	if ln[0] in s: 
		hs = s.replace(ln[0],ln[1])
	if ln[1] in s:
		hs = s.replace(ln[1],ln[0])
	return hs
	
def bukaf(fl):	
	# mengakses FILE
	f = open(fl)
	line = f.readline()
	while line:
		print(line+'')
		line = f.readline()
	f.close()

""" Fungsi repstr adalah untuk melakukan Replace dan Rename filename """
def repstr(f,s1,s2):
	global a
	nf = f.replace(s1, s2)
	if nf != f:
		a = a + 1 # untuk nampung berapa jumlah file yang direname
		os.rename(f,nf)
		print ("  "+str(a)+". RENAMED : "+colored(s1, 'red') + " --> " +colored(s2, 'green')+" :" + nf)

def ren_findir(dr,s1,s2):
	global t    # deklarasi Untuk Mengubah var global
	for path, subdirs, files in os.walk(dr):
		for filename in files:
			t = t+1
			f = os.path.join(path, filename)
			repstr(f,s1,s2)
	print ("\n  Total Files \t\t: "+colored(t, 'green')+"\
		   \n  Total Files RENAMED \t: "+colored(a, 'green'))

# --- -------FUNCTION HASHING STRING----
def hstr(s):
	#return s
	s = s.encode('utf-8')
	return hashlib.md5(s).hexdigest()

# --- -------END FUNCTION HASHING STRING--------		   
		   
# --- ----CHECKING DATA - MODE I---NotUSE---
def checkdata1(s):
	sx = hstr(s)
	odb.execute('SELECT shash FROM `'+g_table+'` WHERE shash = "'+sx+'"')
	if odb.fetchall():
		return "1"
	else:
		return "0"

# --- ----END CHECKING DATA MODE I---NotUSE--
		   
# --- ----CHECKING DATA - MODE II--USE---
# --- ----rename dari checkdata1 --> checkdata2 untuk ujicoba 
		   
# --- ------TES Input Data From Another Process MODE I------
def masukkandata(d1):
	global b
	d1 = d1.replace('"','-')
	d2 = strftime("%Y-%m-%d %H:%M", gmtime())
	d3 = hstr(d1)	
	odb.execute('INSERT INTO `'+g_table+'` (id, `flist`, `addt`, `shash`) VALUES (null, "'+d1+'","'+d2+'","'+d3+'")')
	odb.fetchall()
	db.commit()
	print (" Suksesss Input Data... : "+str(b))
# --- ------END Input Data ----------
		   
def checkfindb(dr):
	# Cuma Cek keberadaan files di dalam DB
	global b,c,t
	b,c,t = 0,0,0
	for path, subdirs, files in os.walk(dr):
		for filename in files:
			f = os.path.join(path, filename)
			t = t+1
			try:
				if checkdata1(f) == "0":
					b = b+1
					print (colored(f, 'red'))
				if checkdata1(f) == "1":
					c = c+1
					print (colored(f, 'green'))
			except Exception as e:
				print (e)

	print ("\n  UnRecorded Data \t: "+colored(str(b),'red')+" \
		   \n  Recorded Data \t: "+colored(str(c),'green')+" \
		   \n  From Total Data \t: "+colored(str(t),'green'))


def processDirectory(dr,ext):
	# Untuk Input File Path ke dalam DB berdasarkan
	global b,c,t
	b,c,t = 0,0,0
	for path, subdirs, files in os.walk(dr):
		for filename in files:
			f = os.path.join(path, filename)
			if ext != "":
				l_ext = len(ext)
				if f[-l_ext:] == ext:
					fp = f.replace('\\','::')
					t = t+1
					if checkdata1(fp) == "0":
						#fwrite("newdata.txt",dirfile)
						try:
							b = b+1
							masukkandata(fp)
						except:
							print ("  Gagal Input Data : "+fp)
					elif checkdata1(fp) == "1":
						c = c+1
						print ("  "+str(c)+ '\t: '+colored(f, 'green'))
					else:
						print ("  UnKnown.....?.")
					#fwrite("olddata.txt",dirfile)
			else:
				fp = f.replace('\\','::')
				t = t+1
				if checkdata1(fp) == "0":
					#fwrite("newdata.txt",dirfile)
					try:
						b = b+1
						masukkandata(fp)
					except:
						print ("  Gagal Input Data : "+fp)
				elif checkdata1(fp) == "1":
					c = c+1
					print ("  "+str(c)+ '\t: '+colored(f, 'green'))
				else:
					print ("  UnKnown.....?.")
				#fwrite("olddata.txt",dirfile)
				
	print ("\n  New Data recorded \t: "+colored(str(b),'red')+" \
		   \n  Recorded Data \t: "+colored(str(c),'green')+" \
		   \n  From Total Data \t: "+colored(str(t),'green'))

"""
--- Get MD5 from all file ind mendeley folder save to mendeley-files.md5
--- Get MD5 from file input and compare to mendeley-files.md5
"""

def get_mendeley_hash(dr,ext):
	for path, subdirs, files in os.walk(dr):
		for filename in files:
			f = os.path.join(path, filename)
			f = f.strip()
			extent = f[-3:]
			try:
				if ext == extent:					
					hash_f = hash_file(f)
					str_to_write = hash_f +" : "+ f
					write_2file(up+"/.mendeley-all-file.md5", str_to_write)
			except Exception as e:
				print (e)

def check_s_infile(f,s):
	with open(f) as f:
		for line in f:
			if s in line:
				line = line.strip()
				return line
			#else:
				#return "Not Found ".join(f)
				#return "no"
	f.close()   
		

def hash_compare(file_in):
	global a,b,t
	# funsi untuk mencocokkan hash dengan hash yang ada di mendeley-files.md5
	up = os.path.expanduser('~')
	file_src = up+"/.mendeley-all-file.md5"
	hash_f = hash_file(file_in)
	if hash_f != "no": 
		c_hash = check_s_infile(file_src,hash_f)
		#if "20" in c_hash: c_hash = c_hash.replace('%20',' ')
		if not c_hash is None:
			a += 1
			print (colored(str("   "+ntpath.basename(c_hash)),"green"))
		else:
			b += 1
			print (colored(str("   Not Found : "+ntpath.basename(file_in)),"red"))
	else: 
		print (colored(str("   Hash Not Found : "+ntpath.basename(file_in)),"red"))



def cp_dbto():
	global wd
	src_dir = r'\AppData\Local\Mendeley Ltd\Mendeley Desktop\abuisa@yahoo.com@www.mendeley.com.sqlite'
	des_dir = wd+'\mendeley_files.sqlite'
	shutil.copy(up+src_dir,des_dir)
	
def open_sqlitedb():
	#conn = sqlite3.connect("mydb.sqlite")
	global up, file_collec
	cp_dbto()
	file_collec = []
	conn = sqlite3.connect(wd+"/mendeley_files.sqlite")
	cursor = conn.cursor()
	sql = "SELECT * FROM Files"
	hsl = cursor.execute(sql)
	hsl1 = cursor.fetchall()
	file_collec += hsl1
	for row in hsl1:
		row1 = row[1].replace('%20',' ')
		#print row[0][:8] + " : " +row[1]
		write_2file(up+"\.mendeley-all-file.md5", row[0] + " : " +row1)
	try:
		os.remove(wd+"\mendeley_files.sqlite")
		os.remove(wd+"\mendeley_files.sqlite-shm")	
	except OSError:
		pass
	


def printout_sqlite():
	global file_collec,up
	open_sqlitedb()
	#print list(file_collec)
	for fc in file_collec:
		print (fc[0] + " : " + fc[1])
		write_2file(up+"\.mendeley-all-file.md5", fc[0] + " : " + fc[1])
		
""" Fungsi listallfile : fungsi untuk melakukan list all file saja tanpa report ke file """
def listallfile(dr,ext):
	global file_collec
	dr = dr.encode('utf-8')
	file_collec = []
	ix = 0
	for path, subdirs, files in os.walk(dr):
		for filename in files:
			f = os.path.join(path, filename)			
			f_ext = f[-len(ext):]
			if ext == f_ext:
				ix += 1
				file_collec += [f]
				#print str("   "+str(ix)+",  "+f) # only for test
	if ix == 0:
		print (colored(str("   File Extention : "+ext+", Not Found !"),"red"))

def file_ls(dr,ext):
	f = os.listdir(dr.encode('utf-8'))
	print (f)
	#for fl in f:
		#print (" "+f)
		#f_ext = fl[-len(ext):]
		#if ext == f_ext:
			#print (" "+fl)
		   
def shelp(s):
	global a,b,t,c, jr, up,wd, rowsc, file_collec # c = jumlah data yang ditemukan di Function check_showdata_bu ---
	if s == "6": # Untuk menampilkan data atau mencari data exp-inpt : master
		st = input("  Input Search Keyword ? : ")
		st = st.replace(' ','%')
		print ("-------------------------------------------------")
		check_showdata(st,"1")

	elif s == "2": # Untuk Cek Data di DB, exp input : /home/username/Pictures/DeepinScreenshot20170313215336.png
		st = input("  Input file with full path (exp:/home/USER/tes.txt) : ")
		print ("-------------------------------------------------")
		try:
			#if checkdata1(st) == "1":
			if checkdata1(st) is None:
				print (colored("  Ups...!!!, DATA Tidak Ditemukan......!","red"))
			if checkdata1(st) != "":
				print (colored("  Status Ditemukan !","green"))
		except:
			#pass
			print (colored("  Status Ditemukan !","green"))
		print ("-------------------------------------------------")
		#print "Cari : "+st

	elif s == "3": # Menge-List semua file di all dir dan check jika file yg di-list ada dalam DB, merah=belum-ada, hijau: udah-ada di DB
		sa = input("  Input Direktori (exp:/home) : ")
		f_ext = input("  Filter by File Extention or Enter for Input All (exp: .docx) : ")
		if sa != "." and sa != "":
			processDirectory(sa,f_ext)
			print ("  Path \t\t\t: "+colored(sa,'green'))
		if sa == ".":
			processDirectory(wd,f_ext)
			print ("  Path \t\t\t: "+colored(wd+'\\','green'))

	elif s == "4": # Menge-List semua file di all dir dan check jika file yg di-list ada dalam DB, merah=belum-ada, hijau: udah-ada di DB
		#print "  Pilihan NO : "+s
		sa = input("  Input Direktori (exp:/home) : ")
		print ("-------------------------------------------------")
		if sa != "." and sa != "":
			checkfindb(sa)
			print ("  Path \t\t\t: "+colored(sa,'green'))
		if sa == ".":
			checkfindb(wd)
			print ("  Path \t\t\t: "+colored(wd,'green'))

	elif s == "5": # Rename or Replace files Names dalam all dir
		#print "  Pilihan NO : "+s
		sa = input("  Input find-str, rep-str, Direktori : ")
		sa = sa.split()
		fstr = sa[0]
		rstr = sa[1]
		ddir = sa[2]
		if ddir == ".":
			ddir = wd
		sb = input('  Reename / Replace File name "'+fstr+'" With "'+rstr+'" to All File in "'+ddir+'" Directory ? [x:Exit][y:Yes]: ')
		#print "Hasil : "+sa[0]
		if sb == "y" or sb == "Y":
			if (ddir != "" and (fstr != "" or rstr != "")):
				print (colored("  Process Rename or Replace Start....", 'green'))
				ren_findir(ddir,fstr,rstr)
			else:
				print (colored("  UPS..!, Please Input the Path/Directory !.", 'red'))
		else:
			pass
		print ('\n\n----------------END OF PROCESS-------------------')

	elif s == "1":	# Untuk menampilkan data atau mencari data, exp-inpt : master; dengan paginatig sistem, Enter untuk next page
		st = input("  Input Search Keyword ! : ")
		print ("  Result for Search Keyword \t: "+colored(st,'red'))
		sx = st.replace(' ','%')
		check_showdata(sx,"1")
		try:
			px = 1
			while True:
				if rowsc > 0 and int(c) < int(jr):
					print ("  This is the Last Page !")
				pg = input("  Input Page or enter for next page [X/x:Exit]: ")
				if pg == "x" or pg == "X" or int(c) == 0:
					break
				sa = input("  Continue for Search Keyword "+colored(st,'red')+" hit Enter, or Search Other Keyword ? [X/x:Exit]: ")
				if sa == "x" or sa == "X":
					break
				#os.system('clear') # For Linux System
				os.system('CLS') # For Windows System
				if sa:
					st = sa
					px = 0 # reset ke halaman 0 jika terdapat input baru dari sa
					print ("  Result for Search Keyword \t: "+colored(sa,'red'))
				else:
					print ("  Result for Search Keyword \t: "+colored(st,'red'))
				
				if pg == "":
					if int(c) < int(jr):
						px = int(px)
					else:
						px = int(px) +1 #or use : px += 1
				else:
					px = pg
				pg = px
				sx = st.replace(' ','%')
				check_showdata(sx,pg)

		except Exception as e:
			print (e) #"Error ?"
			#pass
			
	elif s == "7": # Copy this file to /usr/bin (linux)
		#try:
			#if os.path.isfile(win_dir+'mytool.bat'):
		print ("  Create Shortcut in \t: "+colored(win_dir,'green'))
		print ("  Create Shortcut in \t: "+colored(sys_dir,'green'))
		fn_shrtcut = input("  Input Shortcut File Name : ")
		cp =input("  Create Shortcut ? [y/Y] : ")
		if cp == "y" or cp == "Y":
			#shutil.copytree(wd+'tes.txt', up+'mytool.py')
			if fn_shrtcut != "":
				create_bat_shrcut(win_dir+fn_shrtcut)
				if os.path.isfile(win_dir+fn_shrtcut):
					print (colored("  Success Create Shortcut \t: "+colored(win_dir+fn_shrtcut,'red'),"green")) 
			else:
				create_bat_shrcut(win_dir+'mytool.bat')
				if os.path.isfile(win_dir+'mytool.bat'):
					print (colored("  Success Create Shortcut \t: "+colored(win_dir+'mytool.bat','red'),"green"))
		#except:
			#print (colored("  GAGAL Copy File !","red"))
	elif s == "8": # tes runt function
		while True:
			print (colored("--------SubMenu:8-----------","yellow"))
			print ("""
	1. Test Function
	2. Get All Hash From (mendeley) Folder 
	3. Compare Input file hash to All Hash in file .mendeley-all-file.md5
	4. Compare All File hash to All Hash in file .mendeley-all-file.md5
	5. Print File .mendeley-all-file.md5
	6. Clear File .mendeley-all-file.md5
	7. Copy mendeley.sqlite to Working_Dir then open and write result to .mendeley-all-file.md5
	""")
			print (colored("--------End-SubMenu:8---------","yellow"))
			s8 = input("   Pilih no ?: ")
			print ("--------------------------------")
			if s8 == "x" or s8 == "X":
				break
			if s8 == "1":				
				print ("---chstr-----------------")
				print ("  Hasil File_toList : "+check_s_infile(up+"/tes.txt","tool"))
				print ("---------------------------------------")

			if s8 == "2":
				#print str("   Working Directory : "+wd)
				s82 = input("  Enter the folder of the file to be taken hash : ")
				s82e = input("  Enter Extention File to filter : ")
				if s82 == "" and s82e != "":
					get_mendeley_hash(wd,s82e)
				if s82 != "" and s82e != "":
					get_mendeley_hash(s82,s82e)
			if s8 == "3":
				s83 = input ("   Enter File to Compare [Enter to list file] : ")
				if s83 == "":
					dr = wd
					s831 = input("   Enter File Extention to Filter : ")
					listallfile(dr,s831)
					ix = 0
					e_ix = 0
					for fc in file_collec:
						try:
							ix += 1
							fc = fc.replace('"','"\\')
							print ("   "+str(ix)+",  "+fc)
						except:
							e_ix += 1
							print ("   "+str(ix)+",  Error")
					print ('----------------------------------------')
					print ("  Jumlah File : "+str(len(file_collec)))
					print('  Jumlah yang ERROR : '+str(e_ix)) 
					while True:
						print ("-------------------------------------")
						f_dipilih = input("   Pilih Nomor File to CHECKING ? : ")
						print ("   -----------------------------------")
						if f_dipilih == "x" or f_dipilih == "X":
							break						
						if f_dipilih.isdigit() and int(f_dipilih) <= len(file_collec):
							hash_compare(file_collec[int(f_dipilih)-1])

			if s8 == "4":
				dr = wd
				a,b=0,0
				s84 = input("   Enter File Extention to Filter : ")
				listallfile(dr,s84)
				print ("------------------------")
				for fc in file_collec:
					hash_compare(fc)
				print ("------------------------")
				print ("   Jumlah Total File \t\t: "+ str(int(a)+int(b)))
				print ("   File Yang Ditemukan \t\t: " +str(a))
				print ("   File Yang Tidak Ditemukan \t: " +str(b))
			if s8 == "5":
				of = open(up+'.mendeley-all-file.md5','r')
				ix = 0
				for line in of:
					ix += 1
					print (str(ix)+"\t: "+line.strip())

			if s8 == "6":
				clear_2file(up+'.mendeley-all-file.md5','')
			if s8 == "7":
				open_sqlitedb()
				#printout_sqlite()
	elif s == "9": # tes runt function
		#print (' TES 9')
		del_alldata()
	elif s == "t" or s == "T":
		ext = input(" Extention File exp:.pdf ? \t: ")
		file_ls(wd,ext)
	else:
		quit()
	print ("-------------------------------------------------")
	#print "Selesai.s...."

## colored : yellow, magenta, cyan, red, blue, white
## ---- Start Loop Main menu -----
try:
	if len(sys.argv) > 1:
		#print "Hasil : "+sys.argv[1]
		print ("----------------------------------")
		shelp(sys.argv[1])

	while True:
		print (colored("\n------Main Menu-------------------------------\n\
  1. Find and Show Data, with Paginatig,Only 20 Lines\n\
  2. Check if files in Dir is in DB (Only Check)\n\
  3. Input Data to DB From A Directory Given\n\
  4. Check and Print Out the booth of data \n\
  5. Rename or Replace Files Names\n\
  6. Find and Show Data from DB (Only Showing 20 Data)\n\
  7. Copy myself.py to /usr/bin/mypysql-tool.py [for linux system]\n\
  8. Test Function and Check File Hash Compare to All Mendeley Hash \n\
  9. Clear All Table tflist1 data !\n\
  *. U can use this menu number as a parameter, exp:<<$ mytool 1>>\n\
-------------------------------------------------------","cyan"))
		
		sx = input("  Pilih Menu No ? [x:Exit]: ")
		#sx = si.split(' ')
		if sx == "x":
			break
		shelp(sx)
		#print sx[0] +" : "+sx[1] 

except Exception as e:
	print (e) #"  Exit  !!!."
	#pass
## ---- END Loop Main menu -----
try:
	if tdb is True:
		db.close()
except:
	pass
