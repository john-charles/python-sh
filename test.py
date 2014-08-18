#!/usr/bin/env python

import unittest, tempfile

import os
from os.path import join, exists

from fs import fs, save, load, exists as fs_exists, FSException

class Test_FS_A_Really_Simple_Wrapper(unittest.TestCase):
    
    def setUp(self):        
        self.test_root = tempfile.mkdtemp()
        
    def test_it_joins_complex_paths(self):
        
        path = fs("join", "/home/user", ('dir_one', 'dir_two'), "file.txt")        
        self.assertEqual(path, "/home/user/dir_one/dir_two/file.txt")
        
    def test_it_joins_paths_starting_in_tild(self):
        
        path = fs("join", "~/Desktop")
        
        self.assertEqual(path, os.path.expanduser('~/Desktop'))
    
    def test_mkdirp_creates_directories(self):
        
        test_path = join(self.test_root, "1/2/3/4/5/6/7/8/9/10")
        
        fs("mkdir -p", test_path)
        
        self.assertTrue(exists(test_path))
        
    def test_mkdirp_creates_dirs_with_complex_paths(self):
        
        test_path = join(self.test_root, "one/two/three/four")
        
        fs("mkdir -p", self.test_root, "one", ("two", "three"), "four")
        
        self.assertTrue(exists(test_path))
        
    def test_mkdirp_doesnt_fail_if_dirs_already_exist(self):        
        test_path = join(self.test_root, "a/b/c/d/e/f/g")
        
        fs("mkdir -p", test_path)
        fs("mkdir -p", test_path)
        
        self.assertTrue(exists(test_path))
        
    def test_mkdirp_throws_an_exception_when_a_file_exists(self):
        test_path = join(self.test_root, "a1/b2/c3/d4")
        
        open(join(self.test_root, "a1"), "wb").close()
        self.assertRaises(FSException, lambda: fs("mkdir -p", test_path))
        
    def test_exists(self):
        test_path = fs("join", self.test_root, "n1/n2/n3/n4/n5/n6")
        
        fs("mkdir -p", test_path)        
        self.assertTrue(fs("exists", test_path))
        
    def test_it_can_save_a_string_to_a_file(self):        
        test_string = "This is a test"
        
        save(self.test_root, "test_file.txt", test_string)        
        self.assertTrue(fs_exists(self.test_root, "test_file.txt"))
        
    def test_it_can_read_from_a_file_to_a_string(self):
        test_content = "This is some test content!"
        test_path = fs('join', self.test_root, 'a_file.txt')
        
        f = open(test_path, 'wb')
        f.write(test_content)
        f.close()
        
        self.assertEqual(load(test_path), test_content)
        
        
        
        
        
    
        
        
if __name__ == '__main__':
    unittest.main()
        
        
        
        
        
        
    
    



