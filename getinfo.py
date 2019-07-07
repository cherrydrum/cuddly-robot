import subprocess
def getinfo():
    out = subprocess.Popen(['C:\Program Files (x86)\Deluge\deluge-console.exe', 'info'], stdout=subprocess.PIPE)
    out = out.communicate()[0]

    a = out.decode('utf-8')
    a = a.split('\r\n \r\n')

    torrents = []

    for i in a:
        outputs = {}
        response = [q for q in i.split('\r\n') if q and q != ' ']
        try:
            if 'Progress' in response[7]:
                outputs['status'] = ('downloading', str(response[7].split(' ')[1]), str(response[2].split('ETA: ')[1]) )
                text = ': '.join(response[0].split(': ')[1:])
                if len(text.split(' ')) > 10:
                    text = ' '.join(text.split(' ')[:10])
                outputs['name'] = text
                torrents.append(outputs)
        except:
            pass
    return torrents
