import os.path
import datetime
import pysftp
import json
from os import walk

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

config_file = 'config-inhouse.json'
private_key = 'privateKeyForCrawler.pem'
remote_path = '/home/crawler/app/'
localpath =  ROOT_DIR + '\\Paste_File_Here\\'
# filename = ['NONTEST.txt']
filename = []
for (dirpath, dirnames, filenames) in walk(localpath):
    filename.extend(filenames)
    break

cnopts = pysftp.CnOpts(knownhosts='known_hosts')
now = datetime.datetime.now()


with open(config_file) as config_file:
    config = json.load(config_file)

for server in config['servers']:
    try:
        with pysftp.Connection(host=server['ip'], username=server['username'], private_key=private_key, cnopts=cnopts) as sftp:
            for file in filename:
                check_file = remote_path + file
                backup_folder = remote_path + 'backup/'
                if sftp.exists(check_file):
                    if not sftp.exists(backup_folder):
                        sftp.mkdir(backup_folder)
                    renamed_file = check_file + str('_') + now.strftime("%Y_%m_%d_%H%M%S")
                    sftp.rename(check_file, backup_folder + renamed_file.split('/')[-1])
                    sftp.put(localpath + file, check_file)
                    print(server['name']+ " : Backed up and coppied new file " + file + " to " + remote_path)
                else:
                    sftp.put(localpath + file, check_file)
                    print(server['name']+ " : Coppied file " + file + " to " + remote_path)
        sftp.close()
            
    except Exception as e:
        print(e)
