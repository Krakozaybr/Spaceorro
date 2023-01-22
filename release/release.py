import os.path
import shutil
import subprocess

cur_dir = os.path.dirname(__file__)
spec_path = os.path.join(cur_dir, 'main.spec')
dest_dir = os.path.join(cur_dir, 'dist/main')
zip_file = os.path.join(cur_dir, 'dist/main.zip')

if os.path.exists(dest_dir):
    shutil.rmtree(dest_dir)
if os.path.exists(zip_file):
    os.remove(zip_file)

x = subprocess.Popen(
    ["pyinstaller", spec_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
out, err = x.communicate()
print('OUTPUT:')
print(out.decode("utf-8"))
print('ERROR:')
print(err.decode("utf-8"))
print('RETURN CODE')
print(x.returncode)

shutil.make_archive(base_name=dest_dir, format='zip', root_dir=dest_dir)

x.wait()
