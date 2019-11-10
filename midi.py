chunkSize = 16                              #chunk size = 8 bytes = 16 chars in hex
import binascii                             #one byte can fit 2 hex characters in it
from binascii import hexlify

midifile = open('despacitoT.midi', 'rb')

content = midifile.read()
contenthex = hexlify(content)
#print(contenthex)
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

def getMTrack(content, start = 0):
    index = content[:].find(hexlify(b'MTrk'), start)
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
    prevOp = ""
    while len(content) > 0:
        #strip off time offset
        x = 2
        
        while True:
            deltaTime = content[0:x]
            if int(deltaTime[-2:], 16) < 128:
                break
            x += 2

        content = content[x:]

        if content[:2] not in [b'ff', b'f0',b'f7'] and content[:1] not in [b'8', b'9', b'a', b'b', b'c', b'd', b'e']:
            content = prevOp + content


        if content[:2] in [b'ff', b'f0',b'f7']:
            length = int(content[4:6], 16)
            print(str(deltaTime) + str(content[:6 + length * 2]))
            content = content[6 + length * 2:]
        
        elif content[:1] in [b'8', b'9', b'a', b'b']:
            print(str(deltaTime) + str(content[:6]))
            prevOp = content[:2]
            content = content[6:]
        
        elif content[:1] in [b'c', b'd', b'e']:
            print(str(deltaTime) + str(content[:4]))
            prevOp = content[:2]
            content = content[4:]
        

if __name__ == "__main__":
    #printHex(getHeader(contenthex)) 
    #printHex(getFormat(contenthex))
    #print(getNTracks(contenthex))
    #print(getTickdiv(contenthex))
    #printHex(getMTrack(contenthex))
    #printHex(getMTrack(contenthex))
    unpackMTrack(getMTrack(contenthex))
    pass


