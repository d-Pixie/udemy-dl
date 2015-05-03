import os
import sys
import wget
import subprocess
import requests

class DLException(Exception):
    pass

def download(link, filename):
    if 'youtube.com' in link:
        youtube_dl(link, filename)
    else:
        try:
            curl_dl(link, filename)
        except OSError:
            if not os.path.exists(filename):
                wget.download(link, filename)
            else:
                raise DLException('Failed to download this lecture')


def curl_dl(link, filename):
    command = ['curl', '-C', '-', link, '-o', filename]

    cert_path = requests.certs.where()
    if cert_path:
        command.extend(['--cacert', cert_path])
    else:
        command.extend(['--insecure'])
    subprocess.call(command)


def dl_progress(num_blocks, block_size, total_size):
    progress = num_blocks * block_size * 100 / total_size
    if num_blocks != 0:
        sys.stdout.write(4 * '\b')
    sys.stdout.write('%3d%%' % (progress))


def youtube_dl(link, filename):
    try:
        subprocess.call(['youtube-dl', '-o', filename, link])
    except OSError:
        raise DLException('Install youtube-dl to download this lecture')

