import binascii  # one byte can fit 2 hex characters in it
from binascii import hexlify

chunkSize = 16  # chunk size = 8 bytes = 16 chars in hex
BPM = 89
lengthOfQuarterNote = 60000/BPM #in MS
tickDiv = None

midifile = open('despacitoT.midi', 'rb')

content = midifile.read()
contenthex = hexlify(content)
#print(contenthex)


def getHeader(content):
    index = content.find(hexlify(b'MThd'))
    length = int(content[index + 8:index + 16], 16)
    return content[index: index + chunkSize + length*2]


def getFormat(content):
    return int(getHeader(content)[16:20], 16)


def getNTracks(content):
    return int(getHeader(content)[20:24], 16)


def getTickdiv(content):  # number of sub-divisions of a quarter note, this song has 480
    return int(getHeader(contenthex)[24:28], 16)


def getMTrack(content, start=0):
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
    timings = []
    commands = []
    while len(content) > 0:
        deltaTimeEnd = 2

        while True:
            deltaTime = content[0:deltaTimeEnd]
            if int(deltaTime[-2:], 16) < 128:
                break
            deltaTimeEnd += 2

        deltaTime = deltaTimeToInt(deltaTime)
        timings.append(deltaTime)

        content = content[deltaTimeEnd:]

        if content[:2] not in [b'ff', b'f0', b'f7'] and content[:1] not in [b'8', b'9', b'a', b'b', b'c', b'd', b'e']:
            content = prevOp + content

        if content[:2] in [b'ff', b'f0', b'f7']:
            length = int(content[4:6], 16)
            commands.append(str(content[:6 + length * 2])[2:-1])
            content = content[6 + length * 2:]

        elif content[:1] in [b'8', b'9', b'a', b'b']:
            commands.append(str(content[:6])[2:-1])
            prevOp = content[:2]
            content = content[6:]

        elif content[:1] in [b'c', b'd', b'e']:
            commands.append(str(content[:4])[2:-1])
            prevOp = content[:2]
            content = content[4:]

    return timings, commands

def removeMetaEvents(timings, commands):
    indicesToRemove = []
    for i in range(len(commands)):
        if commands[i][:2] in ['ff', 'f0', 'f7'] or commands[i][:1] in ['a', 'b', 'c', 'd', 'e']:
            indicesToRemove.append(i)

    for i in range(len(indicesToRemove)-1, -1, -1):
        timings.pop(indicesToRemove[i])
        commands.pop(indicesToRemove[i])

    return timings, commands

def generateArduinoTimings(timings):
    outTimings = []
    for timing in timings:
        outTimings.append(timing * lengthOfQuarterNote/tickDiv )
    return outTimings

def generateArduinoCommands(commands):
    return commands

def deltaTimeToInt(dTime):
    binTime = format(int(dTime, 16), '0>' + str(len(dTime) * 4)+'b')
    parsedBinTime = ""
    while len(binTime) > 0:
        binTime = binTime[1:]
        parsedBinTime += binTime[:7]
        binTime = binTime[7:]
    return (int(parsedBinTime, 2))


if __name__ == "__main__":
    #printHex(getHeader(contenthex))
    #print(getFormat(contenthex))
    #print(getNTracks(contenthex))
    tickDiv = getTickdiv(contenthex)
    #printHex(getMTrack(contenthex))
    #printHex(getMTrack(contenthex))
    timings, commands = unpackMTrack(getMTrack(contenthex))
    timings, commands = removeMetaEvents(timings, commands)

    timings = generateArduinoTimings(timings)
    commands = generateArduinoCommands(commands)

    print(timings, commands)

    pass
