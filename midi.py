import os
import binascii  # one byte can fit 2 hex characters in it
from binascii import hexlify

chunkSize = 16  # chunk size = 8 bytes = 16 chars in hex

notes = {       # the notes in hex are converted to arduino friendly notes (same as in pitches.h)
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

# Header - 14 nibbles
# 	4 nibbles - MThd
# 	4 nibbles - length (usually 0006)
# 	2 nibbles - format
# 	2 nibbles - # tracks
# 	2 nibbles -tickdiv

# Body - xxxx nibbles
# 	4 nibbles - MTrk
# 	4 nibbles - length
# 	2-8 nibbles - delta time + event
	
# 	Delta Time:
# 	   If byte is greater or equal to 80h (128 decimal) then the next byte is also part of the VLV,
# 	   else byte is the last byte in a VLV.
	
# 	Events:
# 	    Midi events (status bytes 0x8n - 0xEn)
# 	    Will be followed by 1 or 2 bytes
    
# 	    If the first (status) byte is less than 128 (hex 80), this implies that running status is in effect, 
#       and that this byte is actually the first data byte (the status carrying over from the previous MIDI event). This can only be the case if the immediately previous event was also a MIDI event, i.e. SysEx and Meta events interrupt (clear) running status.
    
# 	    SysEx events (status bytes 0xF0 and 0xF7)
	
# Meta events (status byte 0xFF)


def getHeader(content): 
    '''
    Return the content of the header track, minus the MThd part.
    Arguments:
        content: a binary representation of the MIDI file 
    Returns: 
        a binary representation of the header without the 'MThd'
    '''
    index = content.find(hexlify(b'MThd'))
    length = int(content[index + 8:index + 16], 16)
    return content[index: index + chunkSize + length*2]


def getFormat(content):
    '''
    Return the format of the MIDI file.
    Arguments:
        content: a binary representation of the MIDI file 
    Returns:
        An integer representing the format of the MIDI file (0, 1, or 2)
    '''
    return int(getHeader(content)[16:20], 16)


def getNTracks(content):
    '''
    Return the number of MTrk tracks in the MIDI file.
    Arguments:
        content: a binary representation of the MIDI file 
    '''
    return int(getHeader(content)[20:24], 16)


def getTickdiv(content): 
    '''
    Return the number of sub-divisions of a quarter note. (ticks/quarter note)
    Arguments:
        content: a binary representation of the MIDI file 
    '''
    return int(getHeader(content)[24:28], 16)


def getMTrack(content, start=0):
    '''
    Returns an MTrk track of the MIDI file. 
    Defaults to the first track, the start argument allows the retreival of other tracks
    Arguments:
        content: a binary representation of the MIDI file 
        start (default = 0): when to start the search for the MTrk
    Returns:
        A binary representation of the MTrk 
    '''
    index = content[:].find(hexlify(b'MTrk'), start)
    length = int(content[index + 8:index + 16], 16)
    return content[index: index + chunkSize + length*2]


def printHex(content):
    """Prints and incoming binary string into a hex friendly formant (spaces between chunks of 8 hex chars)."""
    out = ""
    while len(content) > 0:
        out += str(content[:8]) + " "
        content = content[8:]
    print(out)


def unpackMTrack(content):
    '''
    Takes in an MTrk and breaks it down depending on status codes.
    Arguments:
        content: a binary representation of the MTrk
    returns:
        A list containing timings between events
        A list containing the events

    '''
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
    '''
    Removes the events that are not note ON (0x9X) from both a timings and a commands list
    Arguments:
        timings: a list containing timings between events
        commands: a list containing the events
    Returns:
        timings: a list containing timings between events with only note ON statuses
        commands: a list containing the events with only note ON statuses
    '''
    indicesToRemove = []
    for i in range(len(commands)):
        if commands[i][:2] in ['ff', 'f0', 'f7'] or commands[i][:1] in ['a', 'b', 'c', 'd', 'e']:
            indicesToRemove.append(i)

    for i in range(len(indicesToRemove)-1, -1, -1):
        timings.pop(indicesToRemove[i])
        commands.pop(indicesToRemove[i])

    return timings, commands


def generateArduinoTimings(timings, lengthOfQuarterNote, tickDiv):
    '''
    Converts the given timings (in tickDiv format) to millisecond format
    Arguments:
        timings: a list containing timings between events in tickDiv format
        lengthOfQuarterNote: the length of a quarter note in milliseconds
        tickDiv: the number of sub-divisions of a quarter note.
    Returns:
        timings: a list containing timings between events in milliseconds
    '''
    outTimings = []
    for timing in timings:
        outTimings.append(
            round(timing * lengthOfQuarterNote/tickDiv))  # round?
    return outTimings


def generateArduinoCommands(commands):
    '''
    Converts the incoming notes in hexadecimal form to Arduino-friendly form (as defined by pitches.h)
    Arguments:
        commands: a list containing the events in hex form
    Returns:
        commands: a list containing the events in Arduino-friendly form
    '''
    tones = []
    for command in commands:
        tones.append(notes.get(command.upper()))
    return tones


def removeToneOff(timings, commands):
    '''
    Removes the events that are note ON (0x9X) with a velocity of 0 (these are note OFFs)
    Arguments:
        timings: a list containing timings between events
        commands: a list containing the events
    Returns:
        timings: a list containing timings between events with the note OFFs removed
        commands: a list containing the events with the note OFFs removed
    '''
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
    '''
    Removes the chords in a song and only keeps the top note
    Arguments:
        timings: a list containing timings between events
        commands: a list containing the events
    Returns:
        timings: a list containing timings between events with chords removed
        commands: a list containing the events with the chords removed
    '''
    indicesToRemove = []

    for i in range(len(timings)):
        if timings[i] == 0:
            indicesToRemove.append(i)

    for i in range(len(indicesToRemove)-1, -1, -1):
        timings.pop(indicesToRemove[i])
        commands.pop(indicesToRemove[i] - 1)

    return timings, commands


def deltaTimeToInt(dTime):
    '''
    Returns the base-10 integer value represented by a deltaTime
    deltaTimes are a VLV (see comment chunk at the top) thus continuation bits must be removed
    Arguments:
        dTime: a binary representation of a deltaTime
    Returns:
        a integer presenentation of dTime
    '''
    binTime = format(int(dTime, 16), '0>' + str(len(dTime) * 4)+'b')
    parsedBinTime = ""
    while len(binTime) > 0:
        binTime = binTime[1:]
        parsedBinTime += binTime[:7]
        binTime = binTime[7:]
    return (int(parsedBinTime, 2))


def generateInoFile(timings, commands, filename):
    '''
    Generates a runnable .ino file for arduino given the formatted MIDI data.
    The .ino file is placed in the same directory as this code.
    Arguments:
        timings: a list containing timings between events
        commands: a list containing the events
        filename: the filename of the .ino file
    '''
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

    f.write("void song() {  bool playing = true;    for (int i = 0; i < sizeof(delays) / sizeof(delays[0]); i++) {    tone(9, tones[i], delays[i]);    delay(delays[i] + 25);    if (analogRead(A0) <= 950) break;  }}void setup() {}void loop() {  if (analogRead(A0) > 950) song();}")
    f.close()


def makeSong(name, bpm, songLen):
    '''
    Converts a MIDI file to an Arduino .ino file that contains a song
    Arguments:
        name: the file name of the .midi file that is in the same directory as this code
        bpm: the Beats Per Minute of the song
    '''
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
    #print(commands, timings, len(timings))
    timings, commands = removeToneOff(timings, commands) #fix, need 3 vars, delay, length, and tone
    commands = generateArduinoCommands(commands)
    #print(timings, len(timings))
    
    generateInoFile(timings[:songLen], commands[:songLen], name + '.ino')


if __name__ == "__main__":
    if len(os.sys.argv) == 3:
        makeSong(os.sys.argv[1], int(os.sys.argv[2]),int(os.sys.argv[3]))   
    elif len(os.sys.argv) == 1:
        name = input('name: ')
        bpm = input('bpm: ')
        songLen = input('number of notes: ')
        makeSong(name, int(bpm), int(songLen))
    else:
        print("The correct format for using this script is")
        print("python SONG_NAME BPM LEN")
