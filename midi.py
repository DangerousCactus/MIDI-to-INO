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

def getTickdiv(content):                    #number of sub-divisions of a quarter note
    return getHeader(contenthex)[24:28]

def getMTrack(content):
    index = content.find(hexlify(b'MTrk'))
    length = int(content[index + 8:index + 16], 16)
    return content[index: index + chunkSize + length*2]

def printHex(content):
    out = ""
    while len(content) > 0:
        out += str(content[:8]) + " "
        content = content[8:]
    print(out)

def unpackMTrack(content):
    content = content[16:]
    while len(content) > 0:
        #strip off time offset
        x = content[2:3]
        if content[2:4] in [b'ff', b'f0',b'f7']:
            length = int(content[6:8], 16)
            print(content[:8 + length * 2])
            content = content[8 + length * 2:]
        
        elif content[2:3] in [b'8', b'9', b'a', b'b']:
            print(content[:8])
            content = content[8:]
        
        elif content[2:3] in [b'c', b'd', b'e']:
            print(content[:6])
            content = content[6:]

if __name__ == "__main__":
    #printHex(getHeader(contenthex)) 
    #printHex(getFormat(contenthex))
    #print(getNTracks(contenthex))
    #print(getTickdiv(contenthex))
    #printHex(getMTrack(contenthex))
    unpackMTrack(getMTrack(contenthex))

    pass
