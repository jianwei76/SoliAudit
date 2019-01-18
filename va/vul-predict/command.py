#!/usr/bin/env python3

import logging
import subprocess
from subprocess import PIPE


# the class is created for some unusual but possible cases: 
#   1. success, but ec != 0
#   2. error, ec != 0 but errmsg in stdout
#   3. error, but ec = 0 and errmsg in stderr
#   4. the cmd cannot be executed at the same time
class Command:
	
    @staticmethod
    def cmd(cmdline):
        return Command(cmdline)
	
    def __init__(self, cmd):
        self.__cmd = cmd
        self.__timeout_sec = None
        self.__exp_exit_codes = None
        self.__should_check_stderr = False
        self.__lock_obj = None
        self.__encode  = 'UTF-8'
	
    def timeout(self, sec):
        self.__timeout_sec = sec
        return self

    def check(self):
        return self.exp_exit_codes(0).check_stderr();
	
    def exp_exit_codes(self, *ec):
        if ec is not None:
            self.__exp_exit_codes = set(ec)
        return self
	
    def check_stderr(self):
        self.__should_check_stderr = True
        return self
	
    def sync(self, lock_obj):
        self.__lock_obj = lock_obj
        return self

    def encode(self, enc):
        self.__encode=enc
        return self
    
    def run(self):

        proc = self.__sync_exec() if self.__lock_obj is not None else \
             self.__exec()

        is_ec_error = self.__exp_exit_codes and proc.returncode not in self.__exp_exit_codes
        is_stderr_error = self.__should_check_stderr and proc.stderr

        if is_ec_error or is_stderr_error:
            errmsg = proc.stderr if proc.stderr else self.__stdout
            logging.error("run '%s', ec: %s, expect ec: %s, error: %s", self.__cmd, proc.returncode, self.__exp_exit_codes, errmsg);
            raise RuntimeError(errmsg)

        return proc
        #return CmdResponse(ec, self.__stdout, proc.stderr

    def __sync_exec(self):
        with self.__lock_obj:
            return self.__exec()

    def __exec(self):
        return subprocess.run(self.__cmd, shell=True, timeout=self.__timeout_sec, check=False, encoding=self.__encode, universal_newlines=False, stderr=PIPE, stdout=PIPE)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
            format="%(asctime)s.%(msecs)03d [%(levelname)s] [%(module)s] %(message)s", datefmt="%H:%M:%S")

    #print(Command.cmd('ls / | head -n 3').check().run().stdout)
    #print(Command.cmd('ls /xxx | head -n 3').check().run().stdout)
    print(Command.cmd('ping 8.8.8.8').timeout(2).check().run().stdout)

