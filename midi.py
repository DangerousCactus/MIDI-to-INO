chunkSize = 16                              #chunk size = 8 bytes = 16 chars in hex
import binascii                             #one byte can fit 2 hex characters in it
from binascii import hexlify

midifile = open('despacito.midi', 'rb')

content = midifile.read()
contenthex = hexlify(content)

def getHeader(content):
    index = content.find(hexlify(b'MThd'))
    length = int(content[index + 8:index + 16], 16)
    return content[index: index + chunkSize + length*2]

def getFormat(content):
    return getHeader(content)[16:20]

def getNTracks(content):
    return getHeader(content)[20:24]

def getTickdiv(content):
    return getHeader(contenthex)[24:28]

if __name__ == "__main__":
    # print(getHeader(contenthex)) 
    # print(getFormat(contenthex))
    # print(getNTracks(contenthex))
    # print(getTickdiv(contenthex))
    #getChunk(contenthex, 5)
    pass
