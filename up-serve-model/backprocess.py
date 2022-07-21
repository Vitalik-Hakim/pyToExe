
import os
import subprocess
import shutil

## This is a constant script that we need to make either in Python or any langauge
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
# It needs to convert the py to exe one after the other whiles waiting for more
while True:
        
    def convertedfile():
        res = os.listdir(UPLOAD_FOLDER)
        print(res)
        for file in res:
            createDirectory = "pyinstaller --onefile {}/{}".format(UPLOAD_FOLDER,file)
            subprocess.call(createDirectory, shell=True)
            exe = file.replace(".py", ".exe")
            full_path = 'dist/{}'.format(exe)
            shutil.move(full_path, DOWNLOAD_FOLDER)
            os.remove('{}/{}'.format(UPLOAD_FOLDER,file))
            shutil.rmtree('build')
            directory = "./"
            files_in_directory = os.listdir(directory)
            filtered_files = [file for file in files_in_directory if file.endswith(".spec")]
            for file in filtered_files:
                path_to_file = os.path.join(directory, file)
                os.remove(path_to_file)

    # Lets check for python files in the uploads directory
    convertedfile()

