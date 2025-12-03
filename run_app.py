import os
import sys
import webbrowser
import subprocess
import subprocess
from threading import Timer

def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    import sys
    # Determine project root depending on execution mode
    if getattr(sys, 'frozen', False):
        # Running from PyInstaller onefile executable; sys.executable points to the bundled exe location (dist folder)
        project_root = os.path.abspath(os.path.join(os.path.dirname(sys.executable), '..'))
    else:
        # Running from source; __file__ is the script location
        project_root = os.path.abspath(os.path.dirname(__file__))
    os.chdir(project_root)
    Timer(1, open_browser).start()
    subprocess.call([sys.executable, "manage.py", "runserver"])
