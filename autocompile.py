#!/usr/bin/env python
#
# Usage:
#   ./autocompile.py path ext1,ext2,extn cmd
#
# Blocks monitoring |path| and its subdirectories for modifications on
# files ending with suffix |extk|. Run |cmd| each time a modification
# is detected. |cmd| is optional and defaults to 'make'.
#
# Example:
#   ./autocompile.py /my-latex-document-dir .tex,.bib "make pdf"
#
# Dependancies:
#   Linux, Python 2.6, Pyinotify
#
import subprocess
import sys
import pyinotify

class OnWriteHandler(pyinotify.ProcessEvent):
    def __init__(self, cwd, extension, cmd):
        self.cwd = cwd
        self.extensions = extension.split(',')
        self.cmd = cmd

    def _run_cmd(self):
        print '==> Modification detected'
        subprocess.call(self.cmd.split(' '), cwd=self.cwd)

    def _do_notify(self):
        subprocess.call(["notify-send", "doc updated"], cwd=self.cwd)

    def process_default(self, event): pass

    def process_IN_MODIFY(self, event):
        if all(not event.name.endswith(ext) for ext in self.extensions):
            return
        self._run_cmd()
        fname = event.name
        cmd = self.cmd
        self._do_notify()
        print '==> detected change in "%s", ran "%s" -- done!' % (fname, cmd)

def auto_compile(path, extension, cmd):
    wm = pyinotify.WatchManager()
    handler = OnWriteHandler(cwd=path, extension=extension, cmd=cmd)
    notifier = pyinotify.Notifier(wm, default_proc_fun=handler)
    wm.add_watch(path, 4095, rec=True, auto_add=True)

    print '==> Started monitoring "%s" for changes (type ^C to exit)' % path
    while True:  
        try:  
            if notifier.check_events():  
                notifier.read_events()  
                notifier.process_events()  
        except KeyboardInterrupt:  
            notifier.stop()  
            break  
    print '==> Stopped monitoring'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print >> sys.stderr, "Command line error: missing argument(s)."
        sys.exit(1)

    # Required arguments
    path = sys.argv[1]
    extension = sys.argv[2]

    # Optional argument
    cmd = 'make'
    if len(sys.argv) == 4:
        cmd = sys.argv[3]

    # Blocks monitoring
    auto_compile(path, extension, cmd)
