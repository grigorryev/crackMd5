import pyopencl as cl
import threading

from Md5Calculator import Md5Calculator

class Md5Cracker:
    def __init__(self, targetHash, passwordsGenerator, devicesToUse):
        self.targetHash = targetHash
        self.passwordsGenerator = passwordsGenerator
        self.statistics = {}
        self.calculators = []
        self.lock = threading.Lock()
        self.isPasswordFound = False
        self.printingInterval = 1
        self.statsRegistered = 0

        devices = cl.get_platforms()[0].get_devices()
        for index, device in enumerate(devices):
            if (str(index) in devicesToUse):
                calculator = Md5Calculator(device, self.passwordsGenerator, targetHash, self)
                self.calculators.append(calculator);

    def run(self):
        for calculator in self.calculators:
            calculator.start()

        for calculator in self.calculators:
            calculator.join()

    def onStatistics(self, deviceName, speed):
        self.lock.acquire(blocking=1)
        self.statistics[deviceName] = speed

        if(self.timeToPrintStats()):
            print('\n\nSpeeds:')
            print('_' * 80)
            for device, speed in self.statistics.items():
                print('{}:{} {} passwords/sec'.format(device, ' ' * (60 - len(device)), speed))

        self.lock.release()

    def onPasswordFound(self, password):
        self.lock.acquire(blocking=1)

        print('Yeah booooy, your password: ', password)
        self.isPasswordFound = True

        self.lock.release()

    def timeToPrintStats(self):
        self.statsRegistered = (self.statsRegistered + 1) % self.printingInterval
        return not self.statsRegistered
