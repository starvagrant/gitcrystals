#!/usr/bin/env python3

import project.gitglobals as G
import project.command_wrapper as cw
import unittest

class Tests(unittest.TestCase):

    def setUp(self):
        command = [G.GIT, '-C',G.repodir,'checkout','--force', G.current_branch]
        process = cw.run_process(command)

        command = [G.GIT, '-C',G.repodir,'reset','--hard', G.current_commit_sha]
        process = cw.run_process(command)

        # delete all branches but G.current_branch
        command = [G.GIT, '-C',G.repodir,'show-ref','--heads']
        process = cw.run_process(command)
        output = process.stdout
        branches = output.split('\n')
        if len(branches) > 1:  
            sub_string = "/" + G.current_branch
            for branch in branches:
                if branch.find(sub_string) == -1:
                    index = branch.rfind('/')
                    branch_name = branch[index+1:]
                    command = [G.GIT, '-C',G.repodir,'branch','-D', branch_name]
                    process = cw.run_process(command)

    def test_reset_repo(self):
        command = [G.GIT, '-C',G.repodir,'rev-list','HEAD']
        process = cw.run_process(command)
        expected = process.stdout

        with open(G.repodir + '/location.json', 'a') as f:
            f.write('# Test Addition')

        command = [G.GIT, '-C',G.repodir,'add','location.json']
        process = cw.run_process(command)

        command = [G.GIT, '-C',G.repodir,'commit','-m', 'Test commit']
        process = cw.run_process(command)

        G.reset_repo()

        command = [G.GIT, '-C',G.repodir,'rev-list','HEAD']
        process = cw.run_process(command)
        new_rev_list = process.stdout

        self.assertEqual(new_rev_list, expected)

    def test_repo_with_extra_commits(self):
        with open(G.repodir + '/location.json', 'a') as f:
            f.write('# Test Addition')

        command = [G.GIT, '-C',G.repodir,'add','location.json']
        process = cw.run_process(command)

        command = [G.GIT, '-C',G.repodir,'commit','-m', 'Test commit']
        process = cw.run_process(command)

        with self.assertRaises(Exception) as cm:
            G.test_clean_repo()
        exception_message = str(cm.exception)
        expected = "Extra commits found in test repository, please reset"

        self.assertEqual(exception_message, expected)

    def test_repo_with_file_changes(self):
        with open(G.repodir + '/location.json', 'a') as f:
            f.write('# Test Addition')

        with self.assertRaises(Exception) as cm:
            G.test_clean_repo()
        exception_message = str(cm.exception)
        expected = "Working Directory or Index Not Clean. Please clear"

        self.assertEqual(exception_message, expected)

    def test_repo_with_staged_changes(self):
        with open(G.repodir + '/location.json', 'a') as f:
            f.write('# Test Addition')

        command = [G.GIT, '-C',G.repodir,'add','location.json']
        process = cw.run_process(command)

        with self.assertRaises(Exception) as cm:
            G.test_clean_repo()
        exception_message = str(cm.exception)
        expected = "Working Directory or Index Not Clean. Please clear"

        self.assertEqual(exception_message, expected)

    def test_repo_with_extra_branches(self):
        command = [G.GIT, '-C',G.repodir,'branch','gittest']
        process = cw.run_process(command)

        with self.assertRaises(Exception) as cm:
            G.test_clean_repo()
        exception_message = str(cm.exception)
        expected = "Unnecessary Branches, Please Delete"

        self.assertEqual(exception_message, expected)

    def test_change_location_file(self):
        with open(G.repodir + '/location.json', 'w') as f:
            f.write('{\n    "location":"Git Crystal"\n}\n\n')
        G.change_location_file('Mountain Gate')

        command = [G.GIT, '-C',G.repodir,'status','--short']
        process = cw.run_process(command)
        output = process.stdout
        expected = ""

        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
