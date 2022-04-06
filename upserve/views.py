from re import X
from string import Template
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib import messages
import datetime
from datetime import datetime
import calendar
# Create your views here.
class MyIndexView(View):
	def get(self, request):
		request.session['success'] = 0
		rooms = Room.objects.raw("SELECT *, COUNT(tblReserve.rmid_id) as 'count' FROM `tblReserve` RIGHT JOIN tblRoom on tblReserve.rmid_id = tblRoom.rmid group by rmid order by 'count' desc limit 6")
		rooms_all = Room.objects.all();
		p = Room.objects.raw("select * from tblRoom where rmtype='Standard'")
		context = {
			'rooms' : rooms,
			'rooms_all' : rooms_all,
			'p': p
		}
		return render(request, 'index.html', context)

	def post(self, request):
		if request.method == 'POST':
			if 'btnSearch' in request.POST:
				timeslot = request.POST['options']
				rmtype = request.POST['rmtype']
				sched = request.POST['sched']
				prc = request.POST['prc']
				return redirect('/searchresults?timeslot=' + timeslot + '&rmtype=' + rmtype + '&sched=' + sched + '&prc=' + prc)
			else:
				room = Room.objects.get(rmid=request.POST['rmid'])
				request.session['rmid'] = room.rmid
				return redirect('room_info')

class MyIndexLoggedView(View):
	def get(self, request):
		# try:
		logged = Users.objects.get(uid = request.session['uid'])
		rooms = Room.objects.raw("SELECT *, COUNT(tblReserve.rmid_id) as 'count' FROM `tblReserve` RIGHT JOIN tblRoom on tblReserve.rmid_id = tblRoom.rmid group by rmid order by 'count' desc limit 6")
		rooms_all = Room.objects.all();
		# print(request.session['success'])
		if(request.session['success']==1):
			messages.error(request, 'Successfully booked a reservation!')
		context = {
			'logged' : logged,
			'rooms' : rooms,
			'rooms_all' : rooms_all
		}
		return render(request, 'index_logged.html', context)
		# except KeyError:
		# 	pass
		# 	return redirect('my_indexlogged_v')
	def post(self, request):		
		if request.method == 'POST':
			if 'btnLogout' in request.POST:
				try:
					request.session.flush()
				except KeyError:
					pass
				return redirect('my_index_view')
			elif 'btnSearch' in request.POST:
				timeslot = request.POST['options']
				rmtype = request.POST['rmtype']
				sched = request.POST['sched']
				prc = request.POST['prc']
				return redirect('home/searchresults?timeslot=' + timeslot + '&rmtype=' + rmtype + '&sched=' + sched + '&prc=' + prc)
			else:
				room = Room.objects.get(rmid=request.POST['rmid'])
				request.session['rmid'] = room.rmid
				return redirect('room_info_logged')
		
class RoomInfo(View):
	def get(self, request):
		room = Room.objects.get(rmid = request.session['rmid'])
		context = {
			'room' : room
		}
		return render(request, 'room_info.html', context)
class RoomInfoLogged(View):
	def get(self, request):
		request.session['success'] = 0
		try:
			room = Room.objects.get(rmid = request.session['rmid'])
			logged = Users.objects.get(uid = request.session['uid'])
			context = {
				'logged' : logged,
				'room' : room
			}
			return render(request, 'room_info-logged.html', context)

		except KeyError:
			pass
			return redirect('room_info')
	def post(self, request):		
		if request.method == 'POST':
			if 'btnLogout' in request.POST:
				try:
					request.session.flush()
				except KeyError:
					pass
				return redirect('my_index_view')

			elif 'btnReserve' in request.POST:
				rmid = request.POST.get("rmid")
				uid = request.POST.get("uid")
				sched = request.POST.get("sched")
				schedstr = datetime.strptime(sched, "%m-%d-%Y").date() #string to 'date' datatype
				schedformat = schedstr.strftime("%Y-%m-%d") #schedstr format
				tmslt = request.POST.get("tmslt")
				
				form = Reserve(resdate = schedformat, tmslt = tmslt, 
							uid_id = uid, rmid_id = rmid, pending=True)
				form.save()
				request.session['success'] = 1
				return redirect('my_indexlogged_view')
class MySearchResultsView(View):
	def get(self, request):
		try:
			timeslot = request.GET['timeslot']
			rmtype = request.GET['rmtype']
			sched = request.GET['sched']
			prc = request.GET['prc']
			temps = Room.objects.raw("SELECT * FROM tblRoom WHERE rmid IN(select * FROM ( SELECT rmid FROM tblRoom UNION ALL SELECT rmid_id FROM tblReserve WHERE tblReserve.tmslt=%s  AND tblReserve.resdate=%s)tbl GROUP BY rmid HAVING count(*) = 1 ORDER BY rmid)AND tblRoom.prc>=%s AND tblRoom.rmtype=%s", [timeslot, sched, prc, rmtype])
			rooms = Room.objects.raw("SELECT *, COUNT(tblReserve.rmid_id) as 'count' FROM `tblReserve` RIGHT JOIN tblRoom on tblReserve.rmid_id = tblRoom.rmid group by rmid order by 'count' desc limit 6")
			rooms_all = Room.objects.all();
			context = {
				'rooms' : rooms,
				'rooms_all' : rooms_all,
				'temps' : temps
			}
			return render(request, 'index-searchresult.html', context)
		except:
			return redirect("my_index_view")
     
	def post(self, request):
		if request.method == 'POST':
			if 'btnVisit' in request.POST:
				room = Room.objects.get(rmid=request.POST['rmid'])
				request.session['rmid'] = room.rmid
				return redirect('room_info')
			elif 'btnSearch' in request.POST:
				timeslot = request.POST.get('options', False)
				rmtype = request.POST.get('rmtype', False)
				sched = request.POST.get('sched', False)
				prc = request.POST.get('prc', False)
				return redirect('/searchresults?timeslot=' + timeslot + '&rmtype=' + rmtype + '&sched=' + sched + '&prc=' + prc)
			else:
				return redirect('my_index_view')
class MyIndexLogged_Reservations(View):
	def get(self, request):
		logged = Users.objects.get(uid = request.session['uid'])
		urev = Room.objects.raw("SELECT a.*, b.* FROM tblRoom a inner join tblReserve b on a.rmid = b.rmid_id where b.uid_id=%s and pending=TRUE order by resmadedate desc limit 1", [request.session['uid']])
		ureserve = Reserve.objects.raw("SELECT a.*, b.rmname, b.prc, b.rmimg FROM tblReserve a inner join tblRoom b on a.rmid_id = b.rmid where a.uid_id=%s order by resmadedate desc", [request.session['uid']])
		context = {
			'logged' : logged,
			'urev' : urev,
			'ureserve' : ureserve
		}
		return render(request, 'index_logged-reservations.html', context)
	def post(self, request):
		form = ReserveForm(request.POST)		
		if request.method == 'POST':
			if 'btnLogout' in request.POST:
				try:
					request.session.flush()
				except KeyError:
					pass
				return redirect('my_index_view')
			elif 'btnCancelReserve' in request.POST:
				resid = request.POST.get("resid")
				Reserve.objects.filter(resid=resid).delete()
				return redirect('my_indexlogged-reservations_view')
				

class MyIndexLogged_AccountSettings(View):
	def get(self, request):
		try:
			error = request.GET['err']
			messages.error(request, 'Password is incorrect.')
			request.session['conf'] = 0
			logged = Users.objects.get(uid = request.session['uid'])
			context = {
				'logged' : logged,
				'error' : error
			}
			return render(request, 'index_logged-account-settings.html', context)
		except:
			logged = Users.objects.get(uid = request.session['uid'])
			request.session['conf'] = 0
			context = {
				'logged' : logged,
			}
			return render(request, 'index_logged-account-settings.html', context)
	def post(self, request):	
			if request.method == 'POST':
				if 'btnLogout' in request.POST:
					try:
						request.session.flush()
					except KeyError:
						pass
					return redirect('my_index_view')
				elif 'btnConfirm' in request.POST:
					conf = Users.objects.get(uid = request.session['uid'])
					pword = request.POST['pword']
					if(pword == conf.pword):
						request.session['conf'] = 1
						return redirect('my_indexlogged-accountedit_view')
					else:
						return redirect('/home/accountsettings?err=1')
class MyIndexLogged_AccountEdit(View):
	def get(self, request):
		logged = Users.objects.get(uid = request.session['uid'])
		context = {
			'logged' : logged,
		}
		if(request.session['conf']==1):
			return render(request, 'index_logged-account-edit.html', context)
		else: 
			return redirect('my_indexlogged-accountsettings_view')	
	def post(self, request):
			if request.POST:
				if 'btnUpdate' in request.POST:
					uid = request.session['uid']
					fname = request.POST.get("fname")
					lname = request.POST.get("lname")
					email = request.POST.get("email")
					pword = request.POST.get("pword")
					add = request.POST.get("add")
					mobile = request.POST.get("mobile")
					Users.objects.filter(uid=uid).update(fname=fname,lname=lname,pword=pword,email=email,add=add,mobile=mobile)
					return redirect('my_indexlogged-accountsettings_view')
      
class MyIndexLogged_SearchResultsView(View):
	def get(self, request):
		request.session['success'] = 0
		try:
			timeslot = request.GET['timeslot']
			rmtype = request.GET['rmtype']
			sched = request.GET['sched']
			prc = request.GET['prc']
			logged = Users.objects.get(uid = request.session['uid'])
			rooms = Room.objects.raw("SELECT *, COUNT(tblReserve.rmid_id) as 'count' FROM `tblReserve` RIGHT JOIN tblRoom on tblReserve.rmid_id = tblRoom.rmid group by rmid order by 'count' desc limit 6")
			rooms_all = Room.objects.all();
			temps = Room.objects.raw("SELECT * FROM tblRoom WHERE rmid IN(select * FROM ( SELECT rmid FROM tblRoom UNION ALL SELECT rmid_id FROM tblReserve WHERE tblReserve.tmslt=%s  AND tblReserve.resdate=%s)tbl GROUP BY rmid HAVING count(*) = 1 ORDER BY rmid)AND tblRoom.prc>=%s AND tblRoom.rmtype=%s", [timeslot, sched, prc, rmtype])
			context = {
				'logged' : logged,
				'rooms' : rooms,
				'rooms_all' : rooms_all,
				'temps' : temps
			}
			return render(request, 'index_logged-searchresult.html', context)
		except KeyError:
			pass
			return redirect('my_searchresults_view')

	def post(self, request):
		form = ReserveForm(request.POST)		
		if request.method == 'POST':
			if 'btnLogout' in request.POST:
				try:
					request.session.flush()
				except KeyError:
					pass
				return redirect('my_index_view')
			elif 'btnSearch' in request.POST:
				timeslot = request.POST.get('options', False)
				rmtype = request.POST.get('rmtype', False)
				sched = request.POST.get('sched', False)
				prc = request.POST.get('prc', False)
    
				# print("timeslot:", timeslot, "room type:" + rmtype, "sched:", sched, "prc:", prc)
				# p = Room.objects.raw("select * from tblRoom where rmtype=%s and sched=%s and tmslt=%s and prc=%s",[rmtype] )
				# temp = Room.objects.raw("select * from tblRoom right join tblReserve on tblReserve.rmid_id = tblRoom.rmid where tblReserve.tmslt='%s' AND tblRoom.rmtype='%s' AND tblReserve.resdate='%s' AND tblRoom.prc>=%s", timeslot, rmtype, sched, prc)
				return redirect('/searchresults?timeslot=' + timeslot + '&rmtype=' + rmtype + '&sched=' + sched + '&prc=' + prc)
			elif 'btnReserve' in request.POST:
				rmid = request.POST.get("rmid")
				uid = request.POST.get("uid")
				sched = request.POST.get("sched")
				schedstr = datetime.strptime(sched, "%m-%d-%Y").date() #string to 'date' datatype
				schedformat = schedstr.strftime("%Y-%m-%d") #schedstr format
				tmslt = request.POST.get("tmslt")
				
				form = Reserve(resdate = schedformat, tmslt = tmslt, 
							uid_id = uid, rmid_id = rmid, pending=True)
				form.save()
				request.session['success'] = 1
				return redirect('my_indexlogged_view')
			elif 'btnVisit' in request.POST:
				room = Room.objects.get(rmid=request.POST['rmid'])
				request.session['rmid'] = room.rmid
				# print(request.session['rmid'])
				return redirect('room_info_logged')
			else:
				return redirect('my_index_view')

class MyAdminDashboardView(View):
	def get(self, request):
		users = Users.objects.all()
		room = Room.objects.raw("SELECT *, COUNT(tblReserve.rmid_id) as 'count' FROM `tblReserve` RIGHT JOIN tblRoom on tblReserve.rmid_id = tblRoom.rmid group by rmid order by count desc limit 1")
		if request.method == 'GET' and ('month' and 'week' and 'day') in request.GET:
			mon = request.GET['month']
			wk = request.GET['week']
			dy = request.GET['day']
			# print("month:", mon, "| week:", wk, "| day:" , dy)
			if((mon and wk and dy)!= ''):
				exyear = datetime.strptime(mon, "%Y-%m").year #string to 'date' datatype
				exmonth = datetime.strptime(mon, "%Y-%m").month#string to 'date' datatype
				monthname = calendar.month_name[exmonth]
				wk_exweek = datetime.strptime(wk, "%Y-%m-%d").isocalendar().week
				wk_exyear = datetime.strptime(wk, "%Y-%m-%d").year
				day_exday = datetime.strptime(dy, "%Y-%m-%d").day
				day_exdayf = datetime.strptime(dy, "%Y-%m-%d").date()
				day_exdayformat = day_exdayf.strftime("%B %d, %Y")
				filt_m = Reserve.objects.raw("SELECT resid, monthname(resdate) as monthname, COUNT(*) as count FROM `tblReserve` where year(resdate) = '%s' AND month(resdate) = '%s'", [exyear, exmonth])
				filt_w = Reserve.objects.raw("SELECT resid, week(resdate) as week, COUNT(*) as count FROM `tblReserve` where year(resdate) = '%s' and week(resdate) = '%s'", [wk_exyear, wk_exweek])
				filt_d = Reserve.objects.raw("SELECT resid, COUNT(*) as count FROM `tblReserve` where year(resdate) = '%s' and month(resdate) = '%s' AND day(resdate) = '%s'", [exyear, exmonth, day_exday])
				
			context = {
				'users'	: users,
				'room' : room,
				'yearmon' : exyear,
				'yearwk' : wk_exyear,
				'month' : mon,
				'monthname' : monthname,
				'week' : wk,
				'weekx' : wk_exweek,
				'day' : dy,
				'dayx' : day_exdayformat,
				'filt_m' : filt_m,
				'filt_w' : filt_w,
				'filt_d' : filt_d,
			}
			return render(request, 'admin.html', context)
		else:
			mon = 0
			wk = 0
			dy = 0
			mydate = datetime.now()
			monthname = mydate.strftime("%B")

			exyear = datetime.now().year #string to 'date' datatype
			exmonth = datetime.now().month#string to 'date' datatype
			monthname = calendar.month_name[exmonth]
			wk_exweek = datetime.now().isocalendar().week
			wk_exyear = datetime.now().year
			day_exday = datetime.now().day
			day_exdayf = datetime.now().date()
			day_exdayformat = day_exdayf.strftime("%B %d, %Y")
			filt_m = Reserve.objects.raw("SELECT resid, monthname(resdate) as monthname, COUNT(*) as count FROM `tblReserve` where year(resdate) = '%s' AND month(resdate) = '%s'", [exyear, exmonth])
			filt_w = Reserve.objects.raw("SELECT resid, week(resdate) as week, COUNT(*) as count FROM `tblReserve` where year(resdate) = '%s' and week(resdate) = '%s'", [wk_exyear, wk_exweek])
			filt_d = Reserve.objects.raw("SELECT resid, COUNT(*) as count FROM `tblReserve` where year(resdate) = '%s' and month(resdate) = '%s' AND day(resdate) = '%s'", [exyear, exmonth, day_exday])
			
			context = {
			'users'	: users,
			'room' : room,
			'yearmon' : exyear,
			'yearwk' : wk_exyear,
			'month' : mon,
			'monthname' : monthname,
			'week' : wk,
			'weekx' : wk_exweek,
			'day' : dy,
			'dayx' : day_exdayformat,
			'filt_m' : filt_m,
			'filt_w' : filt_w,
			'filt_d' : filt_d,
			}
			return render(request, 'admin.html', context)
	def post(self, request):
		if request.method != 'POST':
			return redirect('my_admindashboard_view')	
		else:	
			mon = request.POST['month']
			wk = request.POST['week']
			day = request.POST['day']
			return redirect('/dashboard?month=' + mon + '&week=' + wk + "&day=" + day)
			
class MyUsersView(View):
	def get(self, request):
		users = Users.objects.all()
		context = {
			'users'	: users
		}
		return render(request, 'users.html', context)

	def post(self, request):
		# form = RoomForm(request.POST)		
		if request.method == 'POST':
			if 'btnDelete' in request.POST:
				uid = request.POST.get("uid")
				Users.objects.filter(uid=uid).delete()
				return redirect('my_users_view')

			elif 'btnUpdate' in request.POST:
				uid = request.POST.get("uid")
				fname = request.POST.get("fname")
				lname = request.POST.get("lname")
				email = request.POST.get("email")
				pword = request.POST.get("pword")
				add = request.POST.get("add")
				mobile = request.POST.get("mobile")
				Users.objects.filter(uid=uid).update(fname=fname,lname=lname,pword=pword,email=email,add=add,mobile=mobile)
				return redirect('my_users_view')

			elif 'btnCreate' in request.POST:
				fname = request.POST.get("fname")
				lname = request.POST.get("lname")
				email = request.POST.get("email")
				pword = request.POST.get("pword")
				add = request.POST.get("add")
				mobile = request.POST.get("mobile")
				form = Users(fname=fname,lname=lname,pword=pword,email=email,add=add,mobile=mobile)
				form.save()
				return redirect('my_users_view')

class MyReservationsView(View):
	def get(self, request):
		reserve = Reserve.objects.all()
		users = Users.objects.all()
		rooms = Room.objects.all()
		context = {
			'reserve'	: reserve,
			'users' : users,
			'rooms' : rooms
		}
		return render(request, 'reservation.html', context)

	def post(self, request):
		# form = RoomForm(request.POST)		
		if request.method == 'POST':
			if 'btnDelete' in request.POST:
				resid = request.POST.get("resid")
				Reserve.objects.filter(resid=resid).delete()
				return redirect('my_reservations_view')
			elif 'btnUpdate' in request.POST:
				resid = request.POST.get("resid")
				fname = request.POST.get("fname")
				uid = Users.objects.filter(fname=fname).values_list('uid')	
				rmname = request.POST.get("rmname")
				rmid = Room.objects.filter(rmname=rmname).values_list('rmid')	
				sched = request.POST.get("sched")
				schedstr = datetime.strptime(sched, "%m-%d-%Y").date() #string to 'date' datatype
				schedformat = schedstr.strftime("%Y-%m-%d") #schedstr format
				tmslt = request.POST.get("tmslt")
				Reserve.objects.filter(resid=resid).update(rmid_id=rmid,uid_id=uid,resdate=schedformat,tmslt=tmslt)
				return redirect('my_reservations_view')
			elif 'btnCreate' in request.POST:
				# resid = request.POST.get("resid")
				fname = request.POST.get("fname")
				uid = Users.objects.filter(fname=fname).values_list('uid')	
				rmname = request.POST.get("rmname")
				rmid = Room.objects.filter(rmname=rmname).values_list('rmid')	
				sched = request.POST.get("sched")
				schedstr = datetime.strptime(sched, "%m-%d-%Y").date() #string to 'date' datatype
				schedformat = schedstr.strftime("%Y-%m-%d") #schedstr format
				tmslt = request.POST.get("tmslt")
				form = Reserve(rmid_id=rmid,uid_id=uid,resdate=schedformat,tmslt=tmslt, pending=True)
				form.save()
				return redirect('my_reservations_view')

class MyRoomsView(View):
	def get(self, request):
		rooms = Room.objects.all()
		context = {
			'rooms'	: rooms
		}
		return render(request, 'rooms.html', context)

	def post(self, request):
		form = RoomForm(request.POST)		
		if request.method == 'POST':
			if 'btnDelete' in request.POST:
				rmid = request.POST.get("rmid")
				Room.objects.filter(rmid=rmid).delete()
				return redirect('my_rooms_view')
			elif 'btnUpdate' in request.POST:
				rmid = request.POST.get("rmid")
				rmtype = request.POST.get("rmtype")
				rmname = request.POST.get("rmname")
				prc = request.POST.get("prc")
				cap = request.POST.get("cap")
				rmimg = request.POST.get("rmimg")
				Room.objects.filter(rmid=rmid).update(rmname=rmname,prc=prc,cap=cap,rmimg=rmimg)
				return redirect('my_rooms_view')
			elif 'btnCreate' in request.POST:
				rmnum = ""
				rmid = request.POST.get("rmid")
				rmtype = request.POST.get("rmtype")
				temp = Room.objects.filter(rmtype=rmtype).count()
				count = temp + 1
				if count<10:
					if rmtype == "Standard":
						rmnum = "S" + "0" + str(count)
					elif rmtype == "Deluxe":
						rmnum = "D" + "0" + str(count)
					elif rmtype == "Premium":
						rmnum = "P" + "0" + str(count)
				else:
					if rmtype == "Standard":
						rmnum = "S" + str(count)
					elif rmtype == "Deluxe":
						rmnum = "D" + str(count)
					elif rmtype == "Premium":
						rmnum = "P" + str(count)
				rmname = request.POST.get("rmname")
				prc = request.POST.get("prc")
				cap = request.POST.get("cap")
				rmimg = request.POST.get("rmimg")
				form = Room(rmtype=rmtype, rmnum=rmnum, rmname=rmname,prc=prc,cap=cap,rmimg=rmimg)
				form.save()
				return redirect('my_rooms_view')
				
class MyLoginView(View):
	def get(self,request):
		users = Users.objects.all()
		context = {
				'users'	: users	
		}
		return render(request, 'login.html', context)

	def post(self, request):
		email = request.POST['email']
		pword = request.POST['pword']
		for instance in Users.objects.all():
			if request.POST['email'] == "admin@asaunlimited.com" and request.POST['pword'] == "admin":
				return redirect('my_admindashboard_view')
			elif instance.email == email:
				if instance.pword == pword:
					request.session['uid'] = instance.uid
					# print(request.session['uid'])
					return redirect('my_indexlogged_view')
				else:
					messages.error(request, 'Email or password is incorrect.')
					return redirect('my_login_view')
			else:
				continue
	
		messages.error(request, 'User does not exist')
		return redirect('my_login_view') 
				
class MySignUpView(View):
	def get(self, request):
		users = Users.objects.all()
		context = {
				'users' : users	
		}
		return render(request, 'signup.html', context)
	
	def post(self, request):
		form = UsersForm(request.POST)
		if request.method == 'POST':
			if form.is_valid():
				users = Users.objects.all()
				fname = request.POST.get("fname")
				lname = request.POST.get("lname")
				pword = request.POST.get("pword")
				email = request.POST.get("email")
				add = request.POST.get("add")
				mobile = request.POST.get("mobile")
				for u in users:
					if (u.email == request.POST['email']):
						messages.error(request, "The entered email already has an existing account.")
						return redirect('my_signup_view')
						
				form = Users(fname = fname, lname = lname, 
							pword = pword, email = email, add = add, 
							mobile = mobile)
				form.save()
				user = Users.objects.get(email=request.POST.get("email"))
				
				request.session['uid'] = user.uid;
				return redirect('my_indexlogged_view')

			else:
				messages.error(request, "The entered email already has an existing account.")
				return redirect('my_signup_view')


	