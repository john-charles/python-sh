#!/usr/bin/env python

import unittest, tempfile

import os
from getpass import getuser
from os.path import join, exists, expanduser

from sh import sh, SHException

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
        
    def test_joining_a_dot_path(self):
        
        path = sh("join", "./abc", "def")
        self.assertEqual(path, "./abc/def")

    def test_it_joins_windows_paths(self):

        path = sh("join", "c:/my_dir", "my_file.txt")
        self.assertEqual(path, "c:/my_dir/my_file.txt")


    def test_it_converts_all_wslashes_to_uslashes(self):

        path = sh("join", "c:\\my_dir\\my_sub")
        self.assertEqual(path, "c:/my_dir/my_sub")

    def test_it_joins_deep_paths_with_backslashes(self):

        path = sh("join", "c:\\my_file", "a\\b\\c\\d")
        self.assertEqual("c:/my_file/a/b/c/d", path)

    def test_it_doesnt_butcher_paths(self):
        raw_path = "c:/users/jcsoko~1/appdata/local/temp/tmpkfex8c/test_file.bin"

        path = sh("join", raw_path)
        self.assertEqual(raw_path, path)


class TestBasicStasticalFunctions(unittest.TestCase):

    def setUp(self):
        self.test_root = tempfile.mkdtemp()

    
    def test_it_knows_if_something_is_a_file_or_a_dir(self):
        
        self.assertTrue(sh("isdir", self.test_root))
        self.assertFalse(sh("isfile", self.test_root))

        
class TestBasicDirectoryOperations(unittest.TestCase):
    
    def setUp(self):
        self.test_root = tempfile.mkdtemp()

    def test_it_knows_when_something_exists(self):
        os.rmdir(self.test_root)

        self.assertFalse(sh("exists", self.test_root))
        self.assertEqual(sh("exists", self.test_root), exists(self.test_root))

        
    def test_it_can_create_a_directory(self):
        
        sh("mkdir", self.test_root, "test_dir")
        self.assertTrue(exists(join(self.test_root, "test_dir")))
        
    def test_it_raises_when_a_path_doesnt_exist(self):
        with self.assertRaises(SHException):
            sh("mkdir", self.test_root, "test_dir", "target_dir")
            
    def test_has_a_p_flag_which_creates_subdirs(self):
        
        sh("mkdir -p", self.test_root, "test_dir", "target_dir")
        self.assertTrue(exists(join(self.test_root, "test_dir", "target_dir")))

    def test_it_can_recursively_create_dirs_with_weird_args(self):

        test_dir = join("a", "b", "c", "d")
        sh("mkdir -p", self.test_root, test_dir)

        self.assertTrue(exists(sh('join', self.test_root, test_dir)))

        
    def test_throws_exception_when_file_exists_as_parent(self):
        
        test_dir = join(self.test_root, "test_dir")
        open(test_dir, "wb").close()
        
        with self.assertRaises(SHException):
            sh("mkdir -p", test_dir, "target_dir")
        
        self.assertFalse(exists(join(test_dir, "target_dir")))
        
    def test_it_can_remove_a_file(self):
        
        test_file = join(self.test_root, "test_file.bin")
        
        open(test_file, "wb")
        self.assertTrue(exists(join(self.test_root, "test_file.bin")))
        
        sh("rm", test_file)
        
        self.assertFalse(exists(test_file))

    def test_it_can_remove_a_single_empty_directory(self):

        target = "target"

        sh("mkdir", self.test_root, target)
        self.assertTrue(sh("isdir", self.test_root, target))
        self.assertTrue(sh("exists", self.test_root, target))

        sh("rm", self.test_root, target)
        self.assertFalse(sh("exists", self.test_root, target))



    def test_it_can_remove_a_file_recursively(self):

        test_dir = join("a", "b", "c", "d")
        sh("mkdir -p", self.test_root, test_dir)

        self.assertTrue(sh("exists", self.test_root, test_dir))

        sh("cd", self.test_root)
        sh("rm -r", ".", test_dir)

        self.assertFalse(sh("exists", self.test_root, test_dir))
        
    def test_it_manages_current_dir(self):
        
        sh("cd", self.test_root)
        self.assertEqual(self.test_root, os.getcwd())

    def test_it_can_list_the_content_of_a_directory(self):

        content = sh("ls", self.test_root)
        self.assertTrue(len(content) == 0)

    def test_it_can_list_a_dir_with_things(self):

        sh("mkdir", self.test_root, "test1");
        sh("mkdir", self.test_root, "test2");

        content = sh("ls", self.test_root)
        self.assertTrue(len(content) == 2)
        self.assertIn("test1", content)
        self.assertIn("test2", content)

    def test_it_can_list_the_cwd(self):

        sh("mkdir", self.test_root, "test1");
        sh("mkdir", self.test_root, "test2");

        sh("cd", self.test_root)

        content = sh("ls")
        self.assertTrue(len(content) == 2)
        self.assertIn("test1", content)
        self.assertIn("test2", content)

class TestFileOperations(unittest.TestCase):

    def setUp(self):

        self.test_root = tempfile.mkdtemp()

    def test_it_can_write_to_a_file(self):
        
        content = "This is some file content"
        sh("save", self.test_root, "test_file.txt", content)

        with open(join(self.test_root, "test_file.txt"), 'rb') as file:
            self.assertEqual(content, file.read())

    def test_it_raises_a_shell_exc_saving_to_a_file_with_missing_deep_paths(self):

        with self.assertRaises(SHException):
            sh("save", self.test_root, "missing", "test_file.txt", "Bal!")



    def test_it_can_load_from_a_file(self):
        
        content = "Uber test content"
        sh("save", self.test_root, "test_file.txt", content)

        self.assertEqual(sh("load", self.test_root, "test_file.txt"), content)

if __name__ == '__main__':
    unittest.main()
    
    



