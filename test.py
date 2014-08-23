#!/usr/bin/env python

import unittest, tempfile

import os
from getpass import getuser
from os.path import join, exists, expanduser

from sh import sh

class TestJoiningAndManipulatingPaths(unittest.TestCase):
    
    def setUp(self):        
        self.test_root = tempfile.mkdtemp()
        self.user_dir = os.path.expanduser('~')
        self.user_dir = os.path.dirname(self.user_dir)     
    
    def test_it_joins_two_strings(self):
        
        path = sh('join', '/home','user')
        self.assertEqual(path, '/home/user')

    def test_it_doesnt_allow_multiple_slashes(self):
        
        path = sh('join', '/home','/user')
        self.assertEqual(path, '/home/user')

    def test_it_doesnt_allow_multiple_slashes_from_behind(self):
        
        path = sh('join', '/home/', 'user')
        self.assertEqual(path, '/home/user')

    def test_it_can_also_join_sub_lists(self):
        
        path = sh('join', '/home', ('a', 'b'));
        self.assertEqual(path, '/home/a/b')

    def test_it_can_join_on_tild(self):
        
        path = sh('join', '~', 'Desktop')
        self.assertEqual(path, expanduser('~') + '/Desktop')

    def test_it_can_resolve_a_tild_username(self):
        
        path = sh('join', '~' + getuser(), 'Desktop')        
        self.assertEqual(path, self.user_dir + "/" + getuser() + "/Desktop")

    def test_it_can_expand_environment_variables(self):
        os.environ['USER'] = "TestUser"
        path = sh('join', '/home/$USER/Desktop')

        self.assertEqual(path, '/home/TestUser/Desktop')

    def test_it_can_expand_several_environment_variables(self):

        os.environ['USER'] = "TestUser"
        os.environ['OTHER'] = "OtherThing"
        path = sh('join', '/home/$USER/Desktop/$OTHER')

        self.assertEqual(path, '/home/TestUser/Desktop/OtherThing')
        
    def test_it_returns_a_list_with_the_l_options(self):
        
        parts = sh("join -l", "a", "b", "c")
        
        self.assertTrue(isinstance(parts, list))
        self.assertEqual(3, len(parts))
        
    def test_the_l_option_even_splits_inner(self):
        
        parts = sh("join -l", "a", "b/c", "d")
        
        self.assertTrue(isinstance(parts, list))
        self.assertEqual(len(parts), 4)
        
class TestBasicDirectoryOperations(unittest.TestCase):
    
    def setUp(self):        
        self.test_root = tempfile.mkdtemp()
        
    def test_it_can_create_a_directory(self):
        
        sh("mkdir", self.test_root, "test_dir")        
        self.assertTrue(exists(join(self.test_root, "test_dir")))
        
        
    
        
        
if __name__ == '__main__':
    unittest.main()
        
        
        
        
        
        
    
    



