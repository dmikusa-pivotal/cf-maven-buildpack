from subprocess import Popen
from subprocess import PIPE

class CurlCustomDownloader(object):
    def __init__(self, ctx):
        self._ctx = ctx

    def download(self, url, toFile):
        cmd = ["curl", "-s", "-L",
               "-o", toFile,
               "-w", "%{http_code}"]
        if url.find('download.oracle.com') >= 0:
            cmd.append("-b")
            cmd.append("oraclelicense=accept-securebackup-cookie")
        cmd.append(url)
        proc = Popen(cmd, stdout=PIPE)
        output, unused_err = proc.communicate()
        proc.poll()
        if output and \
                (output.startswith('4') or
                 output.startswith('5')):
            raise RuntimeError("curl says [%s], failed to download file %s" % (output, url))
        print "Downloaded [%s] to [%s]" % (url, toFile)
