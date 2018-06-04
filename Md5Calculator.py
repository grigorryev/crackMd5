import threading
import pyopencl as cl
import numpy as np
import time

from sys import exit

class Md5Calculator(threading.Thread):
    def __init__(self, oclDevice, passwordGenerator, targetHash, statisticsDelegate):
        threading.Thread.__init__(self)
        self.context = cl.Context(devices=[oclDevice], dev_type=None)
        self.deviceName = oclDevice.get_info(cl.device_info.NAME)
        self.cqueue = cl.CommandQueue(self.context)
        self.passwordGenerator = passwordGenerator
        self.statisticsDelegate = statisticsDelegate
        self.targetHash = targetHash

        #  compile code
        kernelCode = open('md5.cl', 'r').read()
        self.kernel = cl.Program(self.context, kernelCode).build()

        self.setBuffers(10000)
        self.currentSpeed = 0

    def run(self):
        while(self.passwordGenerator.generatePasswords(self.inArray) and not self.statisticsDelegate.isPasswordFound):
            speed = self.calculateBundle()
            self.checkOutput()
            self.adjustBundleSize(speed)

    def calculateBundle(self):
        time1 = time.time()
        cl.enqueue_copy(self.cqueue, self.inBuf, self.inArray).wait()
        self.kernel.calculateMd5Hashes(self.cqueue, self.inArray.shape, None, self.inBuf, self.outBuf)
        cl.enqueue_copy(self.cqueue, self.outArray, self.outBuf).wait()
        time2 = time.time()
        # speed
        return self.bundleSize / (time2 - time1)

    def setBuffers(self, bundleSize):
        # prepare input buffers
        self.bundleSize = bundleSize

        passwordDtype = [("size_bytes", 'i4'), ("password","a60")]
        self.inArray = np.zeros(self.bundleSize, dtype=passwordDtype)
        self.inBuf = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=self.inArray)

        # prepare output buffers
        self.outArray = np.zeros(self.bundleSize, dtype=[('v','>u4', 4)])
        self.outBuf = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY, self.outArray.nbytes)


    def adjustBundleSize(self, newSpeed):
        if (newSpeed > self.currentSpeed):
            self.setBuffers(int(self.bundleSize * 1.5))
        self.currentSpeed = newSpeed

    def checkOutput(self):
        for index, result in enumerate(self.outArray):
            hashblocks = result['v']
            md5HexString = ''.join(hex(block)[2:] for block in hashblocks)
            if(md5HexString == self.targetHash):
                self.statisticsDelegate.onPasswordFound(self.inArray[index]['password'].decode('utf8'))

        self.statisticsDelegate.onStatistics(self.deviceName, int(self.currentSpeed))

    def dump(self, message):
        print(self.deviceName + ':  ' + str(message))
