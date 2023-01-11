import PyInstaller.__main__
import subprocess

PyInstaller.__main__.run([
    'build.spec'

])

subprocess.call(["sh", "./builddmg.sh"])
