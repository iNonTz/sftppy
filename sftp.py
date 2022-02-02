import os.path
import datetime
import pysftp
import json
from os import walk

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

config_normal_server_file = 'config-nonjex-crawler.json'
config_jex_server_file = 'config-jex-crawler.json'
private_key = 'privateKeyForCrawler.pem'
remote_path = '/home/crawler/app/'
localpath =  ROOT_DIR + '\\Paste_File_Here\\'
NormalCrawlerPath =  ROOT_DIR + '\\NormalCrawler\\'
JEXCrawlerPath = ROOT_DIR + '\\JEXCrawler\\'
# filename = ['NONTEST.txt']
filename_jex_crawler = []
filename_normal_crawler = []

for (dirpath, dirnames, filenames) in walk(NormalCrawlerPath):
    filename_normal_crawler.extend(filenames)
    break

for (dirpath, dirnames, filenames) in walk(JEXCrawlerPath):
    filename_jex_crawler.extend(filenames)
    break


cnopts = pysftp.CnOpts(knownhosts='known_hosts')
now = datetime.datetime.now()


def copyFile(filename):
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
if __name__ == '__main__':
    if len(filename_normal_crawler):
        config_file = config_normal_server_file
        copyFile(filename_normal_crawler)

    if len(filename_jex_crawler):
        config_file = config_jex_server_file
        copyFile(filename_jex_crawler)
    try:
        if config_file:
            with open(config_file) as config_file:
                config = json.load(config_file)
    except Exception as e:
        print('Error : ' + str(e))
