import binascii

midifile = open('despacito.midi', 'rb')

content = midifile.read()
print(binascii.hexlify(content))