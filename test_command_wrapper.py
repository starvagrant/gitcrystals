#!/usr/bin/env python3

import unittest
import command_wrapper

class test_command_wrapper(unittest.TestCase):

    def test_command_wrapper(self):
        process = command_wrapper.run_process(['echo','yoyoyo'])
        self.assertEqual(process.stdout, 'yoyoyo\n')

unittest.main()
