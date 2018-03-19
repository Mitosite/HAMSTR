from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import reset_queries

from align.models import * # specify imported functions for ease of untangling later
from align.forms import * # specify imported functions for ease of untangling later
from align.tasks import * # specify imported functions for ease of untangling later
import align.static.align.pyscripts.mitositefuncs as msf
from align.submission_methods import handle_uploaded_single_file, handle_uploaded_paired_file
import os
import sys
import subprocess
import smtplib
from email.mime.text import MIMEText as text



#pages in choose app

def index(request):
	return render(request, 'align/choose.html')

def single(request):
	return render(request, 'align/single.html')

def paired(request):
	return render(request, 'align/paired.html')

def loading(request):
	return render(request, 'align/loading.html')

def choose(request):
	return render(request, 'align/choose.html')

def tutorial(request):
	return render(request, 'align/tutorial.html')

def about(request):
	return render(request, 'align/about.html')

def programmes(request):
	return render(request, 'align/programmes.html')

def testresult(request):
	return render(request, 'align/testresult.html')

def results(request):
	return render(request, '../static/align/')

def styletest(request):
	return render(request, 'align/styletest.html')


#Site processes

outlogfilename = "/dev/null"

staticpath = "/project/home17/whb17/public_html/django-framework/mitosite/align/static/align/"

uploadpath = staticpath + "uploads/"

def handle_uploaded_single_file(f, path):

	UPLOADED_FILE_1 = path + "input1.fastq"

	with open(UPLOADED_FILE_1, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

	# open upload file for reading
	my_file = open(UPLOADED_FILE_1)

def handle_uploaded_paired_file(f, path):

	UPLOADED_FILE_2 = path + "input2.fastq"

	with open(UPLOADED_FILE_2, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

	# open upload file for reading
	my_file = open(UPLOADED_FILE_2)

def handle_uploaded_adapters(f, path):

	UPLOADED_FILE_3 = path + "adapters.fa"

	with open(UPLOADED_FILE_3, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

	# open upload file for reading
	my_file = open(UPLOADED_FILE_3)

def SingleJob(request):
	upload_message = "Please upload reads in FASTQ format only*:"
	if request.method == 'POST':
		form = SingleJobForm(request.POST, request.FILES)
		print('REQUEST IS FINE')
		if form.is_valid():
			print('!!FORM IS VALID!!')
			
			job_status = 'Verifying file format...' #Informs user files being checked
			#check if name of uploaded file contains '.fastq' or '.fq'
			try:
				file_name = request.FILES['readsfile'].name
				msf.suffixtest(file_name)
			except TypeError:
				upload_message = "This file type is not supported. Please upload 'fastq' or 'fq' files:"
				return render(request, 'align/single.html', {'upload_message': upload_message, 'form':form })
				job_status = ''
			print("File has .fastq suffix")

			#check content of file
			try:
				file_content = request.FILES['readsfile'].readlines()
				msf.formattest(file_content)
			except ValueError:
				upload_message = "File content is incorrectly formatted. Please try a different file."
				return render(request, 'align/single.html', {'upload_message': upload_message, 'form':form})
			print("Lines divisible by 4. File is very likely to be fastq.")

			#Generate user key and directory path
			key = msf.keygen()
			dirpath = uploadpath + key +"/"
			os.mkdir(dirpath) # change directory to new directory
			msf.writetext(key, 'key.txt', dirpath) #Put .txt of key in directory
			print("This job's key is " + key)
			
			#Pass user-selected parameters to the command line in the form of a .txt file
			#Step 1: Aignment to hg19 human reference genome
			s1_aln_choice = form.cleaned_data['s1_aligners']
			#Checks aligner has been selected
			if not s1_aln_choice:
				s1_aln_empty = "Step 1 aligners must be selected:"
				return render(request, 'align/loading.html', {'upload_message': "upload_message",})
			s1_aln_choice = ''.join(s1_aln_choice)
			msf.writetext(s1_aln_choice, 's1_aln_choice.txt', dirpath)
			print("First aligner choice acknowleged")

			#Pass user-selected parameters to the command line in the form of a .txt file
			#Step2: Align mitomapped and numt reads to mt genome
			s2_aln_choice = form.cleaned_data['s2_aligners']
			#Checks aligner has been selected
			if not s2_aln_choice:
				s2_aln_empty = "Step 2 aligners must be selected:"
				return render(request, 'align/loading.html', {'upload_message': "upload_message", 's1_aln_message': s1_aln_message, 's2_aln_empty': s2_aln_empty,})
			s2_aln_choice = ''.join(s2_aln_choice)
			msf.writetext(s2_aln_choice, 's2_aln_choice.txt', dirpath)
			print("Second aligner choice acknowleged")

			#Deal with uploaded file to prepare for pipeline (function above)
			handle_uploaded_single_file(request.FILES['readsfile'], dirpath)
			print("Reads file has been handled and uploaded.")
			
			# Set off job start alert
			user_email = form.cleaned_data['user_email']
			os.chdir(dirpath) # ensure .txt file written into correct directory
			msf.writetext(user_email, 'mailadrs.txt', dirpath) # writes .txt file containing email address to be used by job end alert email
			msf.startalert(user_email, key) #sends email
			print('Job start alert has been successfully sent.')

			# make adapters available as .txt file
			adapter = form.cleaned_data['adapter']
			os.chdir(dirpath) # ensure .txt file written into correct directory
			msf.writetext(adapter, 'adapter.txt', dirpath)
			print("Adapter acknowleged.")

			# Set key environment variable
			os.chdir(dirpath)                   # set directory to given path to new directory
			os.environ['KEY'] = key      # set environment variable to be new directory
			os.system("echo $KEY")			# echo path to command line
			print("Key environment variable set.")

			#Initiate command line
			print("Command line has been initiated.")
			#os.system("source " + staticpath + "shscripts/master.sh")
			#pl_path = staticpath + "pyscripts/singlepipe.py"
			#with open(outlogfilename, "wb") as out: 
			sgl_pipe=["python", staticpath + "pyscripts/singlepipe.py"]
			with open(outlogfilename, "wb") as out: 
				p = subprocess.Popen(sgl_pipe, stdout=out, stderr=subprocess.STDOUT)

			#Transition to job start page displaying user key
			return render(request, 'align/loading.html', {'upload_message': "Uploaded file successfully", 'random_key': key, 'form':form,})


		else:
			print('first else')
			upload_message = "Not a valid file format"
			return render(request, 'align/single.html', {'upload_message': upload_message, 'form':form})
	else:
		print('last else')
		form = SingleJobForm()
		return render(request, 'align/single.html', {'upload_message': upload_message, 'form':form})

def PairedJob(request):
	upload_message = "Please upload reads in FASTQ format only*:"
	if request.method == 'POST':
		form = PairedJobForm(request.POST, request.FILES)
		print('REQUEST IS FINE')
		if form.is_valid():
			print('!!FORM IS VALID!!')
			#end_type = form.cleaned_data['end_type']
			#print('!!!' + endtype + '!!!')
			
			#check if name of uploaded file contains '.fastq' or '.fq'
			#readsfile1
			try:
				file_name = request.FILES['readsfile1'].name
				msf.suffixtest(file_name)
			except TypeError:
				upload_message = "This file type is not supported. Please upload 'fastq' or 'fq' files:"
				return render(request, 'align/single.html', {'upload_message': upload_message, 'form':form })

			#readsfile2
			try:
				file_name = request.FILES['readsfile2'].name
				msf.suffixtest(file_name)
			except TypeError:
				upload_message = "This file type is not supported. Please upload 'fastq' or 'fq' files:"
				return render(request, 'align/paired.html', {'upload_message': upload_message, 'form':form })

			#check content of file
			#readsfile1
			try:
				file_content = request.FILES['readsfile1'].readlines()
				msf.formattest(file_content)
			except ValueError:
				upload_message = "File content is incorrectly formatted. Please try a different file."
				return render(request, 'align/paired.html', {'upload_message': "upload_message", 'form':form})

			#readsfile2
			try:
				file_content = request.FILES['readsfile2'].readlines()
				msf.formattest(file_content)
			except ValueError:
				upload_message = "File content is incorrectly formatted. Please try a different file."
				return render(request, 'align/paired.html', {'upload_message': "upload_message", 'form':form})

			#Generate user key and directory path
			key = msf.keygen()
			uploadpath = "/project/home17/whb17/public_html/django-framework/mitosite/align/static/align/uploads/"
			dirpath = uploadpath + key +"/"
			os.mkdir(dirpath) # change directory to new directory
			msf.writetext(key, 'key.txt', dirpath) #Put .txt of key in directory
			
			#Pass user-selected parameters to the command line in the form of a .txt file
			#Step 1: Aignment to hg19 human reference genome
			s1_aln_choice = form.cleaned_data['s1_aligners']
			s1_aln_choice = ''.join(s1_aln_choice)
			msf.writetext(s1_aln_choice, 's1_aln_choice.txt', dirpath)

			#Pass user-selected parameters to the command line in the form of a .txt file
			#Step2: Align mitomapped and numt reads to mt genome
			s2_aln_choice = form.cleaned_data['s2_aligners']
			s2_aln_choice = ''.join(s2_aln_choice)
			msf.writetext(s2_aln_choice, 's2_aln_choice.txt', dirpath)

			#Deal with uploaded file to prepare for pipeline (function above)
			handle_uploaded_single_file(request.FILES['readsfile1'], dirpath)
			handle_uploaded_paired_file(request.FILES['readsfile2'], dirpath)

			#Deal with adapters (function above)
			handle_uploaded_adapters(request.FILES['adapters'], dirpath)

			# Set off job start alert
			user_email = form.cleaned_data['user_email']
			os.chdir(dirpath) # ensure .txt file written into correct directory
			msf.writetext(user_email, 'mailadrs.txt', dirpath) # writes .txt file containing email address to be used by job end alert email
			msf.startalert(user_email, key) #sends email

			#Initiate command line
			print("Command line has been initiated.")
			#os.system("source " + staticpath + "shscripts/master.sh")
			#pl_path = staticpath + "pyscripts/singlepipe.py"
			#with open(outlogfilename, "wb") as out: 
			sgl_pipe=["python", staticpath + "pyscripts/pairedpipe.py"]
			with open(outlogfilename, "wb") as out: 
				p = subprocess.Popen(sgl_pipe, stdout=out, stderr=subprocess.STDOUT)
			
			#Transition to job start page displaying user key
			return render(request, 'align/loading.html', {'upload_message': "Uploaded file successfully", 'random_key': key, 'form':form }) #
		else:
			print('first else')
			upload_message = "Please upload two different fastq files:"
			return render(request, 'align/paired.html', {'upload_message': upload_message, 'form':form})
	else:
		print('last else')
		form = PairedJobForm()
		return render(request, 'align/paired.html', {'upload_message': upload_message, 'form':form})

def RetrieveJob(request):
	retr_msg = "Enter key to retrieve job:"
	if request.method == 'POST':
		form = RetrieveJobForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				print('!!VALID!!')
				inp_key = form.cleaned_data['input_key']
				print(inp_key)
				#Path for retrieval
				retrpath = uploadpath + inp_key
				print(retrpath)

				#Retrieve user directory
				os.chdir(retrpath)
				os.system('pwd')

				#Open summary text file to display on page
				txtfile = open("summary.txt", "r")
				sum_txt = txtfile.readlines()

				line_list = []

				for line in sum_txt:
					line_list.append(line.rstrip())

				txtline1 = line_list[1]
				txtline2 = line_list[2]
				txtline3 = line_list[3]
				txtline4 = line_list[4]
				txtline5 = line_list[5]
				txtline6 = line_list[6]
				txtline7 = line_list[9]
				txtline8 = line_list[11]
				txtline9 = line_list[12]
				txtline10 = line_list[13]
				txtline11 = line_list[14]
				txtline12 = line_list[15]
				txtline13 = line_list[16]
				txtline14 = line_list[18]
				txtline15 = line_list[19]
				txtline16 = line_list[20]
				txtline17 = line_list[21]
				txtline18 = line_list[23]
				txtline19 = line_list[24]
				txtline20 = line_list[25]
				txtline21 = line_list[26]

				txtline22 = line_list[30]
				txtline23 = line_list[31]
				txtline24 = line_list[32]
				txtline25 = line_list[33]
				txtline26 = line_list[35]
				txtline27 = line_list[36]
				txtline28 = line_list[37]
				txtline29 = line_list[38]
			
				return render(request, 'align/testresult.html', {'retr_msg': retr_msg, 'form':form, 'inp_key':inp_key, 'txtline1': txtline1, 'txtline2': txtline2, 'txtline3': txtline3, 'txtline4': txtline4, 'txtline5': txtline5, 'txtline6': txtline6, 'txtline7': txtline7, 'txtline8': txtline8, 'txtline9': txtline9, 'txtline10': txtline10, 'txtline11': txtline11, 'txtline12': txtline12, 'txtline13': txtline13, 'txtline14': txtline14, 'txtline15': txtline15, 'txtline16': txtline16, 'txtline17': txtline17, 'txtline18': txtline18, 'txtline19': txtline19, 'txtline20': txtline20,
					'txtline21': txtline21, 'txtline22': txtline22, 'txtline23': txtline23, 'txtline24': txtline24, 'txtline25': txtline25, 'txtline26': txtline26, 'txtline27': txtline27, 'txtline28': txtline28, 'txtline29': txtline29,})
			except FileNotFoundError:
				retr_msg = "The key " + inp_key + " does not exist or job is incomplete. Please try again once you have recieved a job completion email alert. Please enter a valid key:"
				return render(request, 'align/retrieve.html', {'retr_msg': retr_msg, 'form':form})
		else:
			print('first else')
			return render(request, 'align/retrieve.html', {'retr_msg': "Key" + inp_key + "does not exist.", 'form':form, "chroms":chroms})
	else:
		print('last else')
		form = RetrieveJobForm()
		return render(request, 'align/retrieve.html', {'retr_msg': retr_msg, 'form': form})


