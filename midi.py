import binascii  # one byte can fit 2 hex characters in it
from binascii import hexlify

chunkSize = 16  # chunk size = 8 bytes = 16 chars in hex

notes = {
    '24': 'C1', '30': 'C2', '3C': 'C3', '48': 'C4', '54': 'C5', '60': 'C6', '6C': 'C7',	'78': 'C8',
    '25': 'CS1', '31': 'CS2', '3D': 'CS3', '49': 'CS4', '55': 'CS5', '61': 'CS6', '6D': 'CS7', '79': 'CS8',
    '26': 'D1', '32': 'D2', '3E': 'D3', '4A': 'D4', '56': 'D5', '62': 'D6', '6E': 'D7', '7A': 'D8',
    '27': 'DS1', '33': 'DS2', '3F': 'DS3', '4B': 'DS4', '57': 'DS5', '63': 'DS6', '6F': 'DS7', '7B': 'DS8',
    '28': 'E1', '34': 'E2', '40': 'E3', '4C': 'E4', '58': 'E5', '64': 'E6', '70': 'E7',	'7C': 'E8',
    '29': 'F1', '35': 'F2', '41': 'F3', '4D': 'F4', '59': 'F5', '65': 'F6', '71': 'F7', '7D': 'F8',
    '2A': 'FS1', '36': 'FS2', '42': 'FS3', '4E': 'FS4', '5A': 'FS5', '66': 'FS6', '72': 'FS7',	'7E': 'FS8',
    '2B': 'G1', '37': 'G2', '43': 'G3', '4F': 'G4', '5B': 'G5', '67': 'G6', '73': 'G7', '7F': 'G8',
    '2C': 'GS1', '38': 'GS2', '44': 'GS3', '50': 'GS4', '5C': 'GS5', '68': 'GS6', '74': 'GS7',
    '2D': 'A1', '39': 'A2', '45': 'A3', '51': 'A4', '5D': 'A5', '69': 'A6', '75': 'A7',
    '2E': 'AS1', '3A': 'AS2', '46': 'AS3', '52': 'AS4', '5E': 'AS5', '6A': 'AS6', '76': 'AS7',
    '23': 'B0', '2F': 'B1', '3B': 'B2', '47': 'B3', '53': 'B4', '5F': 'B5', '6B': 'B6', '77': 'B7'
}


def getHeader(content):
    index = content.find(hexlify(b'MThd'))
    length = int(content[index + 8:index + 16], 16)
    return content[index: index + chunkSize + length*2]


def getFormat(content):
    return int(getHeader(content)[16:20], 16)


def getNTracks(content):
    return int(getHeader(content)[20:24], 16)


def getTickdiv(content):  # number of sub-divisions of a quarter note, this song has 480
    return int(getHeader(content)[24:28], 16)


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


def generateArduinoTimings(timings, lengthOfQuarterNote, tickDiv):
    outTimings = []
    for timing in timings:
        outTimings.append(
            round(timing * lengthOfQuarterNote/tickDiv))  # round?
    return outTimings


def generateArduinoCommands(commands):
    tones = []
    for command in commands:
        tones.append(notes.get(command.upper()))
    return tones


def removeToneOff(timings, commands):
    indicesToRemove = []
    for i in range(len(commands)):
        if commands[i][-2:] == '00':
            indicesToRemove.append(i)

    for i in range(len(indicesToRemove)-1, -1, -1):
        timings[indicesToRemove[i]-1] += timings.pop(indicesToRemove[i])
        commands.pop(indicesToRemove[i])

    for i in range(len(commands)):
        commands[i] = commands[i][2:4]

    return timings, commands


def removeRepeatedCommands(timings, commands):
    indicesToRemove = []

    for i in range(len(timings)):
        if timings[i] == 0:
            indicesToRemove.append(i)

    for i in range(len(indicesToRemove)-1, -1, -1):
        timings.pop(indicesToRemove[i])
        commands.pop(indicesToRemove[i] - 1)

    return timings, commands


def deltaTimeToInt(dTime):
    binTime = format(int(dTime, 16), '0>' + str(len(dTime) * 4)+'b')
    parsedBinTime = ""
    while len(binTime) > 0:
        binTime = binTime[1:]
        parsedBinTime += binTime[:7]
        binTime = binTime[7:]
    return (int(parsedBinTime, 2))


def generateInoFile(timings, commands, filename):
    f = open(filename, 'w')
    pitches = open('pitches.h', 'r')

    for line in pitches.readlines():
        f.write(line)
    f.write("\n")

    f.write('int tonePin = 11;' + "\n")

    out = ""
    for command in commands:
        out += command + ','
    out = out[:-1]
    f.write('int tones[] = {' + out + '};' + "\n")

    out = ""
    for timing in timings:
        out += str(timing) + ','
    out = out[:-1]
    f.write('int delays[] = {' + out + '};' + "\n")

    f.write(
        "void song() {\nfor(int i = 0; i < sizeof(delays)/sizeof(delays[0]); i++){\ntone(tonePin, tones[i], delays[i]);\ndelay(delays[i] + 25);}}\nvoid setup() {}\nvoid loop() {song();}")
    f.close()


def makeSong(name, bpm):
    BPM = bpm
    lengthOfQuarterNote = 60000/BPM  # in MS

    midifile = open(name + '.midi', 'rb')
    content = midifile.read()
    midifile.close()
    contenthex = hexlify(content)

    tickDiv = getTickdiv(contenthex)

    timings, commands = unpackMTrack(getMTrack(contenthex))
    timings, commands = removeMetaEvents(timings, commands)
    timings = generateArduinoTimings(timings, lengthOfQuarterNote, tickDiv)
    timings, commands = removeRepeatedCommands(timings, commands)
    timings, commands = removeToneOff(timings, commands)
    commands = generateArduinoCommands(commands)
    generateInoFile(timings, commands, name + '.ino')


songs = [['allstar', 200], ['despacito', 120], ['numberone', 120]]

for song in songs:
    makeSong(song[0], song[1])