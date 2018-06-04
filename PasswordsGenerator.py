import random
import threading
import string

class PasswordsGenerator:
    def __init__(self):
        self.lock = threading.Lock()

    def generatePasswords(self, buffer):
        self.lock.acquire(blocking=1)
        passwordsGenerated = 0
        for index, entry in enumerate(buffer):
            try:
                newPassword = self.getNextPassword()
                buffer[index] = (len(newPassword), newPassword)
                passwordsGenerated += 1
            except StopIteration:
                break

        self.lock.release()
        return passwordsGenerated

class StupidPasswordsGenerator(PasswordsGenerator):
    def __init__(self):
        super().__init__()

    def getNextPassword(self):
        length = random.randint(1, 20)
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


class DictionaryPasswordsGenerator(PasswordsGenerator):
    def __init__(self, dictFilePath):
        super().__init__()
        self.dict = open(dictFilePath, 'r')

    def getNextPassword(self):
        return next(self.dict).strip()
