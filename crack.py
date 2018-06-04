import argparse
import pyopencl as cl

from Md5Cracker import Md5Cracker
from PasswordsGenerator import StupidPasswordsGenerator, DictionaryPasswordsGenerator

parser = argparse.ArgumentParser()
parser.add_argument('--hash')
parser.add_argument('--dict')
parser.add_argument('--devices')
parser.add_argument('--showdevices', default=False, action="store_true")

args = parser.parse_args()
if (args.showdevices):
    print('Devices available:')
    devices = cl.get_platforms()[0].get_devices()
    for i, device in enumerate(devices):
        print(i, ': ', device.get_info(cl.device_info.NAME))

elif (args.hash):
    hashToFind = args.hash.lower()
    dictPath = args.dict
    devices = args.devices

    passwordsGenerator = DictionaryPasswordsGenerator(dictPath) if dictPath else StupidPasswordsGenerator()
    cracker = Md5Cracker(hashToFind, passwordsGenerator, devices.split(','))
    cracker.run()

else:
    print('Wrong args, use --help')
