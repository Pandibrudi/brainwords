import mindwave, time
import serial

#need for a msg about connection
headset = mindwave.Headset('COM9')


def read_eeg(headset): #takes headset object as argument
    time.sleep(.5)
    print ("Raw value: %s, Attention: %s, Meditation: %s" % (headset.raw_value, headset.attention, headset.meditation))
    print ("Waves: {}".format(headset.waves))
    return headset.attention

while True:
    read_eeg(headset)