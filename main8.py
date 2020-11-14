#!C:\python36_32\python.exe
import cgi
import cgitb
import os
import sys
import io
import datetime
import math
import re
import socket
import time

cgitb.enable()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPTNAME = "./main8.py"
LOGFILE = "log8.txt"
MAXLOG = 100
WAITTIME = 5

def autolink2(txt):
	pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
	res = re.findall(pattern, txt)
	"""
	<a href="$1" target="_blank">$1<\/a>
	"""
	#print(res)
	if res: 
		for r in res:
			txt = txt.replace(r, '<a href="' + r + '" target="_blank">' + r + '</a>')
			#print(txt)
	return txt
	

def autolink(txt):
	pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
	r = re.search(pattern, txt)
	"""
	<a href="$1" target="_blank">$1<\/a>
	"""
	#print(r)
	if r:
		txt = txt.replace(r.group(), '<a href="' + r.group() + '" target="_blank">' + r.group() + '</a>')
		#print(txt)
	return txt

def pp(value, flg=False):
	print(value, end="<br>")
	print(type(value), end="<br>")
	print(repr(value), end="<br>")
	if flg:
		sys.exit()

def update_data(com_no, tim, com, addr, host, epo):
	print("call update_data()")
	#print(com_no, end="<br>")
	#print(tim, end="<br>")
	#print(repr(com), end="<br>")
	
	#pp(addr)
	#pp(host)
	
	n = open(LOGFILE, mode="r", encoding="UTF-8")
	l = n.readlines()
	n.close()
	
	n = open(LOGFILE, mode="w", encoding="UTF-8")
	l_num = len(l)
	i = 0
	
	#com = cgi.escape(com)
	
	while (i < l_num):
		ll = l[i].split("<>")
		no = ll[0]
		
		com = (com.replace("\r\n", "<br>")).rstrip("<br>")
		
		if int(com_no) == int(no):
			#rstrip()が必要
			n.write(no + "<>" + tim + "<>" + com.rstrip() + "<>" + addr.rstrip() + "<>" + host.rstrip() + "<>" + epo.rstrip() + "\n")
		else:
			n.write(l[i])
		i += 1
		
	n.close()
	
	print('<a href="' + SCRIPTNAME + '">掲示板へ戻る</a>')
	
	footer()
	
	sys.exit()


def edit_form(log):
	print("call edit_form()")
	print(log)
	
	ll = log.split("<>")
	no = ll[0]
	t = ll[1]
	l = ll[2]
	addr = ll[3]
	host = ll[4]
	epo = ll[5]
	
	print('<form action="' + SCRIPTNAME + '" method="post">')
	
	print('<input type="hidden" name="mode" value="update">')
	print('<input type="hidden" name="com_no" value="' + no + '">')
	print('<input type="hidden" name="tim" value="' + t + '">')
	print('<input type="hidden" name="addr" value="' + addr + '">')
	print('<input type="hidden" name="host" value="' + host + '">')
	print('<input type="hidden" name="epo" value="' + epo + '">')
	
	print("<table>")
	print("<tr>")
	print("<td>")
	print('<textarea name="comment" cols="56" rows="7">' + l.replace("<br>", "\n") + '</textarea>')
	print("</td>")
	print("</tr>")
	print("</table>")
	
	print('<input type="submit" value="送信する">')
	print("</form>")
	
	footer()
	
	sys.exit()

def edit_data(com_no):
	print("call edit_data()")
	print(com_no)
	
	n = open(LOGFILE, mode="r", encoding="UTF-8")
	l = n.readlines()
	n.close()
	
	l_num = len(l)
	i = 0
	while (i < l_num):
		ll = l[i].split("<>")
		no = ll[0]
		if int(com_no) == int(no):
			edit_form(l[i]);
		else:
			i += 1
	#bbs_list()
	sys.exit()

def acpt_data(com):
	print("call acpt_data()")
	
	#com = c
	#com = cgi.escape(c)
	
	#print(repr(com))
	#sys.exit()
	
	#com = cgi.escape(com)
	
	#windowsの改行コードは"\r\n"
	#repr(com)でわかった
	#print(repr(com))
	#sys.exit()
	com = (com.replace("\r\n", "<br>")).rstrip("<br>")
		
	#採番処理
	no = "1"
	n = open(LOGFILE, mode="r", encoding="UTF-8")
	l = n.readlines()
	l_num = len(l)
	
	#投稿上限チェック
	#if l_num > MAXLOG - 1:
	if l_num >= MAXLOG:
		n.close()
		print("投稿数が上限です")
		sys.exit()
		
	ll = []
	if not l_num == 0:
		ll = l[l_num - 1].split("<>")
		no = ll[0]
		no = str(int(no) + 1)
	n.close()
	
	f = open(LOGFILE, mode="a", encoding="UTF-8")
	#書き込むときは"\n"
	t = datetime.date.today()
	h = datetime.datetime.now()
	tim = "{}年{}月{}日{}時{}分{}秒".format(t.year,t.month,t.day,h.hour,h.minute,h.second)
	
	addr = os.environ["REMOTE_ADDR"]
	host = []
	try:
		host = socket.gethostbyaddr(addr)
	except socket.herror:
		host.append(addr)
	
	epoch = time.time()
	
	#未投稿の時はチェックしない
	if not l_num == 0:
		if epoch - float(ll[5]) <= WAITTIME and addr == ll[3]:
			print("連続投稿はできません")
			f.close()
			sys.exit()
		
	f.write(no + "<>" + tim + "<>" + com + "<>" + addr + "<>" + host[0] + "<>" + str(epoch) + "\n")
	f.close()
	
	print('<a href="' + SCRIPTNAME + '">掲示板へ戻る</a>')
	
	footer()
	
	sys.exit()

def abone_data(com_no, addr, epoch):
	print("call abone_data()")
	
	update_data(com_no, "あぼーん", "あぼーん", addr, "あぼーん", epoch)
	
	bbs_list()
	sys.exit()


def dele_data(com_no):
	print("call dele_data()")
	print(com_no)
	
	n = open(LOGFILE, mode="r", encoding="UTF-8")
	l = n.readlines()
	n.close()
	
	n = open(LOGFILE, mode="w", encoding="UTF-8")
	l_num = len(l)
	i = 0
	while (i < l_num):
		ll = l[i].split("<>")
		no = ll[0]
		if int(com_no) != int(no):
			n.write(l[i])
		i += 1
	
	n.close()
	bbs_list()
	sys.exit()


def ANDsearch(keylist, teststr):
	for keyword in keylist:
		if keyword in teststr:
			continue
		else:
			return False
	
	return True

def ORsearch(keylist, teststr):
	for keyword in keylist:
		if keyword in teststr:
			return True
	
	return False

def find_data():
	
	print("call find_data()")
	
	print('<form action="' + SCRIPTNAME + '" method="post">')
	print('<input type="hidden" name="mode" value="find">')
	print('<input type="text" name="comment" value="">')
	print('<select name="cond">')
	print('<option value="1">AND</option>')
	print('<option value="0">OR</option>')
	print('</select>')
	print('<input type="submit" value="検索">')
	print("</form>")
	
	footer()
	
	#sys.exit()

def search_data(c, condition):
	print("call search_data()")
	print(c)
	print(condition)
	
	f = open(LOGFILE, encoding="UTF-8")
	line = f.readlines()
	llen = len(line)
	f.close()
	
	#keylist = " ".join(c) #まちがい
	keylist = c.split()
	print(keylist)
	lines = []
	i = 0
	while (i < llen):
		ll = line[i].split("<>")
		#
		# <br>を削除しないと"b" "r"で検索に引っかかる
		#
		#print(repr(ll[2]), end="<br>")
		ll[2] = ll[2].replace("<br>", "")
		#print(repr(ll[2]), end="<br>")
		
		if int(condition) == 1:
			if ANDsearch(keylist, ll[2]):
				lines.append(line[i])
		elif int(condition) == 0:
			if ORsearch(keylist, ll[2]):
				lines.append(line[i])
		else:
			print("ありえない")
		
		i += 1
	
	print(lines)
	
	find_data()
	
	print('<table border="1">')
	
	i = 0
	while i < len(lines):
		ll = lines[i].split("<>")
		print("<tr>")
		print("<td>")
		print(ll[0])
		print("</td>")
		print("<td>")
		print(ll[1])
		print("</td>")
		print("<td>")
		print(ll[2])
		print("</td>")
		print("<td>")
		print('<a href="' + SCRIPTNAME + '?mode=dele&res=' + str(ll[0]) + '">削除</a>')
		print("</td>")
		print("<td>")
		print('<a href="' + SCRIPTNAME + '?mode=edit&res=' + str(ll[0]) + '">編集</a>')
		print("</td>")
		print("<td>")
		print('<a href="' + SCRIPTNAME + '?mode=abone&res=' + str(ll[0]) + '&addr=' + str(ll[3]) + '&epo=' + str(ll[5]) + '">あぼーん</a>')
		print("</td>")
		print("<td>")
		print(ll[3])
		print("</td>")
		print("<td>")
		print(ll[4])
		print("</td>")
		print("<td>")
		print(ll[5])
		print("</td>")
		print("</tr>")
		i += 1
	print("</table>")
	
	print('<a href="' + SCRIPTNAME + '">掲示板へ戻る</a>')
	
	footer()
	
	sys.exit()
	
def note_page():
	print("call note_page()")
	sys.exit()

start = 0
NUM_PER_PAGE = 10

def bbs_list():
	global start

	print("call bbs_list()", end="<br>")
	
	try:
		f = open(LOGFILE, encoding="UTF-8")
	except Exception as e:
		print(e)
	"""        
	except:
		print("ファイル関連エラー")
		footer()
		sys.exit()
	"""
	line = f.readlines()
	#llen = len(line) $#は長さlen(line) - 1と等価
	llen = len(line) - 1
	f.close()
	
	if start > llen:
		start = llen
	nextpage = start + NUM_PER_PAGE
	backpage = start - NUM_PER_PAGE
	if backpage < 0:
		backpage = 0
	
	
	print('<table border="1">')
	
	i = start
	while i < nextpage:
		if i > llen or i < 0: #i<0は投稿がない時breakで抜ける
			break
		
		ll = line[i].split("<>")
		print("<tr>")
		print("<td>")
		print(ll[0])
		print("</td>")
		print("<td>")
		print(ll[1])
		print("</td>")
		print("<td>")
		print(ll[2])
		print("</td>")
		print("<td>")
		print('<a href="' + SCRIPTNAME + '?mode=dele&res=' + str(ll[0]) + '">削除</a>')
		print("</td>")
		print("<td>")
		print('<a href="' + SCRIPTNAME + '?mode=edit&res=' + str(ll[0]) + '">編集</a>')
		print("</td>")
		print("<td>")
		#print('<a href="' + SCRIPTNAME + '?mode=abone&res=' + str(ll[0]) + '">あぼーん</a>')
		print('<a href="' + SCRIPTNAME + '?mode=abone&res=' + str(ll[0]) + '&addr=' + str(ll[3]) + '&epo=' + str(ll[5]) + '">あぼーん</a>')
		print("</td>")
		print("<td>")
		print(ll[3])
		print("</td>")
		print("<td>")
		print(ll[4])
		print("</td>")
		print("<td>")
		print(ll[5])
		print("</td>")
		print("</tr>")
		i += 1
	print("</table>")
	
	
	print('<form action="' + SCRIPTNAME + '" method="post">')
	print('<input type="hidden" name="mode" value="acpt">')
	#print('<input type="hidden" name="com_no" value="' + ll[0] + '">')
	#print('<input type="hidden" name="tim" value="' + ll[1] + '">')
	print('<textarea name="comment" rows="10"></textarea>')
	print('<input type="submit" value="送信">')
	print("</form>")
	
	if start > 0:
		print('<a href="' + SCRIPTNAME + '?start=' + str(backpage) + '">前</a>')
	
	j = 0
	startpage = 0
	while j < math.ceil((llen + 1) / NUM_PER_PAGE): # llenは$#で-1の値 +1が必要 もしくはlen(line)/10にする
		if startpage == start:
			print(str(j + 1))
		else:
			print('<a href="' + SCRIPTNAME + '?start=' + str(startpage) + '">' + str(j + 1) + '</a>')
		startpage += NUM_PER_PAGE
		j += 1
	
	if nextpage - 1 < llen:
		print('<a href="' + SCRIPTNAME + '?start=' + str(nextpage) + '">次</a>')
	
	print('<a href="' + SCRIPTNAME + '?mode=find">検索</a>')
	
	#footer()

def footer():
	print("</body>")
	print("</html>")

if __name__ == "__main__":

	print("Content-type: text/html\n")
	print("<html>")
	print('<head><TITLE>CGI script output</TITLE><meta charset="UTF-8"></head>')
	#print('<head><TITLE>CGI script output</TITLE></head>')
	print("<body>")
	
	if os.environ["REQUEST_METHOD"] == "GET":
		#print(os.environ["QUERY_STRING"])
		line = os.environ["QUERY_STRING"].split("&")
		#print(line)
		
		d = {}
		i = 0
		l = len(line)
		
		while (i < l):
			ll = line[i].split("=")
			if not ll[0] == "":
				d[ll[0]] = ll[1]
			i += 1
		
		if "start" in d:
			start = int(d["start"])
		else:
			start = 0
		
		
		for key in d:
			print(key + ":" + d[key] + "<br>")
		
		"""
		# 処理分岐
		if ($in{mode} eq 'acpt') { acpt_data(); }
		if ($in{mode} eq 'dele') { dele_data(); }
		if ($in{mode} eq 'find') { find_data(); }
		if ($in{mode} eq 'note') { note_page(); }
		bbs_list();
		"""
		if "mode" in d:
			if d["mode"] == "acpt":
				acpt_data("あぼん")
			if d["mode"] == "dele":
				if d["res"]: 
					dele_data(d["res"])
			if d["mode"] == "edit":
				edit_data(d["res"])
			if d["mode"] == "find":
				find_data()
				sys.exit()
			if d["mode"] == "note":
				note_page()
			if d["mode"] == "abone":
				if d["res"] and d["addr"] and d["epo"]:
					abone_data(d["res"], d["addr"], d["epo"])
		bbs_list()
		
	elif os.environ["REQUEST_METHOD"] == "POST":
		print("postです")
		
		form = cgi.FieldStorage()
		
		m = form["mode"].value
		if "comment" in form:
			comm = form["comment"].value
			comm = cgi.escape(comm)
			
			#comm = autolink2(comm)
			
		else:
			print("えらーです")
			bbs_list()
			sys.exit()
		
		
		if m == "acpt":
			acpt_data(comm)
		if m == "edit":
			c = form["com_no"].value
			#t = form["tim"].value
			edit_data(c)
		if m == "update":
			c = form["com_no"].value
			t = form["tim"].value
			addr = form["addr"].value
			host = form["host"].value
			e = form["epo"].value
			
			update_data(c, t, comm, addr, host, e)
		if m == "find":
			condition = form["cond"].value
			search_data(comm, condition)
			sys.exit()
			
		bbs_list()
	else:
		print("エラー")

	#bbs_list()

	footer()

