#!/usr/bin/env python3

from project.command_wrapper import run_process
import unittest

class Tests(unittest.TestCase):

    def test_command_wrapper(self):
        process = run_process(['echo','yoyoyo'])
        self.assertEqual(process.stdout, 'yoyoyo\n')

if __name__ == '__main__':
    unittest.main()
