import os
import sys
import shutil
from datetime import datetime

HOW_OLD = 3 # days
WHERE_OCTOPUS_APPS_ARE = "c:\Octopus\Applications\Development"

paths = [
	"C:\confirmit_logs",
	#"C:\temp",
]
all_files = []
to_be_deleted = []

def should_be_deleted(file_path):
	delta = datetime.now() - datetime.fromtimestamp(os.path.getctime(file_path))
	if delta.days > HOW_OLD:
		print ("File '%s' set to be deleted" % file_path)
		to_be_deleted.append(file_path)

def get_all_files_in_folder(path):
	for path, subdirs, files in os.walk(path):
		for name in files:
			all_files.append(os.path.join(path, name))
    

def delete_old_octopus_apps():
	folder = WHERE_OCTOPUS_APPS_ARE
	if not os.path.exists(folder):
		print("Directory '%s' doesn't exist" % folder)
		return
	# get list of apps
	octo_apps = os.listdir(folder)
	#octo_apps = ["Confirmit.Hub.Service",]
	for app in octo_apps:
		print(app)
		print(folder)
		new_path = "/".join((folder, app))
		if not os.path.exists(new_path) or not os.path.isdir(new_path):
			print("Directory '%s' doesn't exist" % new_path)
			continue
		# get list of folders in app
		sub_folders = os.listdir(new_path)
		if len(sub_folders) > 1:
			newest_subfolder = None
			for sub_folder in sub_folders:
				print ("Subfolder we're looking at now: %s" % sub_folder)
				sub_folder_path = "/".join((new_path, sub_folder))
				sub_folder_creation_date = get_folder_creation_date(sub_folder_path)
				if ((newest_subfolder is None) or (sub_folder_creation_date > get_folder_creation_date("/".join((new_path, newest_subfolder))))):
					newest_subfolder = sub_folder
			print("newest subfolder for %s app is %s" % (app, newest_subfolder))
			for sub_folder in sub_folders:
				if sub_folder != newest_subfolder:
					print("will delete following subfolder %s" % sub_folder)
					to_be_deleted.append("/".join((new_path, sub_folder)))
		
	
	
	# delete the older folder

def get_folder_creation_date(path):
	return datetime.fromtimestamp(os.path.getctime(path))
	
for path in paths:
	get_all_files_in_folder(path)

for file in all_files:
	print ("checking file '%s'" % file)
	should_be_deleted(file)

delete_old_octopus_apps()
        
print("%d files to be deleted" % len(to_be_deleted))

for d in to_be_deleted:
	print("will delete '%s' now" % d)
	try:
		if os.path.isdir(d):
			shutil.rmtree(d)
		else:
			os.remove(d)
	except:
		print ("Got following error, but will ignore it: ", sys.exc_info()[0])
