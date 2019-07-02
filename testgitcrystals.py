#!/usr/bin/env python3

from gitcrystals import GitCrystalsCmd
import unittest
import subprocess
import gitconstants as G
import command_wrapper as cw
from jsondata import JsonData


current_commit_sha='e3562f3142fdebdb367eb2375b002bccdbf7b713'
current_branch='data'

def reset_repo():
    command = [G.GIT, '-C','game-repo','checkout',current_branch]
    process = cw.run_process(command)

    command = [G.GIT, '-C','game-repo','reset','--hard', current_commit_sha]
    process = cw.run_process(command)

    branches = []
    command = [G.GIT, '-C','game-repo','--show-ref', '--heads']
    process = cw.run_process(command)
    output = process.stdout
    output_lines = output.split('\n')
    if '' in output_lines:
        output_lines.pop()
    for line in output_lines:
        branches.append(re.sub(r'[0-9a-f]{40} refs/heads/','', line))
    for branch in branches:
        if branch != 'data':
            command = [G.GIT, '-C','game-repo','branch','-D', branch]
            process = cw.run_process(command)

def test_clean_repo():
    command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'rev-list', current_branch]
    process = cw.run_process(command)
    output = process.stdout
    if not output.split('\n')[0]==current_commit_sha:
        print(output.split('\n')[0])
        print("Extra commits found in test repository, please reset")
        return False

    command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'status', '--short']
    process = cw.run_process(command)
    output = process.stdout
    if not output=='':
        print("Working Directory or Index Not Clean. Please clear")
        return False

    command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'show-ref', '--heads']
    process = cw.run_process(command)
    output = process.stdout
    lines = output.split('\n')
    if not lines[-1:]==['']: # last element will be empty string if only one ref
        print('Unnecessary Branches, Please Delete')
        return False

    return True

class Tests(unittest.TestCase):

    # Test game quits correctly
    def test_do_quit(self):
        game = GitCrystalsCmd()
        self.assertTrue(game.do_quit(''))

    def test_do_revlist(self):
        reset_repo()
        if test_clean_repo():
            game = GitCrystalsCmd()
            game.do_revlist('')
            head_commit = game.output.split('\n')[0]
            self.assertEqual(head_commit, current_commit_sha)

        reset_repo()

    def test_branch(self):
        reset_repo()
        if test_clean_repo():

            game = GitCrystalsCmd()
            game.do_branch('newbranch')

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'branch']
            process = cw.run_process(command)
            output = process.stdout

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'branch', '-d', 'newbranch']
            process = cw.run_process(command)

            expected = "* data\n  newbranch\n"
            self.assertEqual(output, expected)

        reset_repo()

    def test_listbranches(self):
        reset_repo()
        if test_clean_repo():

            game = GitCrystalsCmd()
            game.do_listbranches('')

            expected = "* data\n"
            self.assertEqual(game.output, expected)

        reset_repo()

    def test_checkout_same_ref(self):
        reset_repo()
        if test_clean_repo():

            game = GitCrystalsCmd()
            game.do_branch('newbranch')

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'checkout','newbranch']
            process = cw.run_process(command)

            game.do_checkout('newbranch')
            game.do_listbranches('')
            expected = "  data\n* newbranch\n"
            actual = game.output

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'checkout',current_branch]
            process = cw.run_process(command)
            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'branch', '-d', 'newbranch']
            process = cw.run_process(command)

            self.assertEqual(actual, expected)

        reset_repo()

    def test_checkout_file(self):
        reset_repo()
        if test_clean_repo():

            game = GitCrystalsCmd()
            with open('game-repo/README.md', 'a') as f:
                f.write("##Test Header")

            game.do_checkoutfile('README.md')

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'status','--short']
            process = cw.run_process(command)

            expected = ''
            self.assertEqual(process.stdout, expected)

        reset_repo()

    def test_go(self):
        reset_repo()
        if test_clean_repo():

            game = GitCrystalsCmd()
            game.do_go('north')
            expected_location = "Git Crystal"
            player_location = game.player.location
            json_file = JsonData("game-repo","location")
            file_location = json_file.data['location']

            self.assertEqual(player_location, expected_location)
            self.assertEqual(file_location, expected_location)

            game.do_go('east')

        reset_repo()

    def test_stage(self):
        reset_repo()
        if test_clean_repo():

            game = GitCrystalsCmd()
            game.do_go('north')
            game.do_stage('location.json')

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'status','--short']
            process1 = cw.run_process(command)

            game.do_go('south')
            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'reset','HEAD','location.json']
            process2 = cw.run_process(command)

            expected = 'M  location.json\n' # location.json is staged
            self.assertEqual(process1.stdout, expected)

        reset_repo()

    def test_unstage(self):
        reset_repo()
        if test_clean_repo():

            game = GitCrystalsCmd()
            game.do_go('north')
            game.do_stage('location.json')
            game.do_unstage('location.json')

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'status','--short']
            process = cw.run_process(command)
            game.do_go('south')

            expected = ' M location.json\n' # location.json has unstaged changes
            self.assertEqual(process.stdout, expected)

        reset_repo()

    def test_commit(self):
        reset_repo()
        if test_clean_repo():

            game = GitCrystalsCmd()
            game.do_go('north')
            game.do_stage('location.json')
            game.do_commit('')

            command = [G.GIT, G.GIT_DIR, G.WORK_TREE, 'show-ref','--heads']
            process = cw.run_process(command)
            self.assertNotEqual(process.stdout, current_commit_sha + " refs/heads/" + current_branch + '\n')

        reset_repo()

    def test_status_format(self):
        game = GitCrystalsCmd()
        unstaged_change = game.format_status(' M location.json\n')
        expected = "    unstaged changes: location.json\n"
        self.assertEqual(unstaged_change, expected)
        staged_change = game.format_status('M  location.json\n')
        expected = "    staged changes: location.json\n"
        self.assertEqual(staged_change, expected)

    def test_status(self):
        reset_repo()
        if test_clean_repo():
            game = GitCrystalsCmd()

            game.do_status('')

            expected = 'No changes since last commit\n'
            self.assertEqual(game.output, expected)

            game.do_go('north')

            game.do_status('')
            expected = "    unstaged changes: location.json\n"
            self.assertEqual(game.output, expected)

            game.do_stage('location.json')
            game.do_status('')
            expected = "    staged changes: location.json\n"
            self.assertEqual(game.output, expected)

            game.do_go('north')
            game.do_status('')
            expected = '    staged changes: location.json\n    unstaged changes: location.json\n'
            self.assertEqual(game.output, expected)

        reset_repo()

    def test_git_log(self):
        reset_repo()
        if test_clean_repo():
            game = GitCrystalsCmd()

            game.do_log('')
            expected="""commit e3562f3142fdebdb367eb2375b002bccdbf7b713 (HEAD -> data)
Author: James Ginns <starvagrant@yahoo.com>
Date:   Thu Jun 27 22:07:42 2019 -0500

    Basic Game Data

commit 75f9ce255a19d4f4b347b679e00ebee2ad027046 (tag: first-commit)
Author: James Ginns <starvagrant@yahoo.com>
Date:   Mon Jun 24 02:46:16 2019 -0500

    Explain the data repository to user
"""

            self.assertEqual(game.output, expected)

    def test_git_graph(self):
        reset_repo()
        if test_clean_repo():
            game = GitCrystalsCmd()

            game.do_graph('')
            expected = """* e3562f3 (HEAD -> data) Basic Game Data
* 75f9ce2 (tag: first-commit) Explain the data repository to user
"""

            self.assertEqual(game.output, expected)

    def test_git_diff(self):
        reset_repo()
        if test_clean_repo():
            game = GitCrystalsCmd()

            game.do_north('')
            game.do_diff('')

            expected = """diff --git a/location.json b/location.json
index 86b52b7..64e45dc 100644
--- a/location.json
+++ b/location.json
@@ -1,4 +1,4 @@
 {
-    "location":"Mountain Gate"
+    "location":"Git Crystal"
 }

"""

            self.assertEqual(game.output, expected)

            game.do_stage('location.json')
            game.do_diffstaged('')
            expected = """diff --git a/location.json b/location.json
index 86b52b7..64e45dc 100644
--- a/location.json
+++ b/location.json
@@ -1,4 +1,4 @@
 {
-    "location":"Mountain Gate"
+    "location":"Git Crystal"
 }
 
"""
            self.assertEqual(game.output, expected)
            reset_repo()

    def test_git_diffbranch(self):
        reset_repo()
        if test_clean_repo():
            game = GitCrystalsCmd()
            game.do_branch('trial')
            game.do_north('')
            game.do_stage('location.json')
            game.do_commit('')
            game.do_diffbranch('')

            expected = "only " + "data,trial are legal branch names\n"
            expected += "usage: diffbranch branch1 branch2\n"
            self.assertEqual(game.output, expected)

            game.do_diffbranch('trial data')
            expected = """diff --git a/location.json b/location.json
index 86b52b7..64e45dc 100644
--- a/location.json
+++ b/location.json
@@ -1,4 +1,4 @@
 {
-    "location":"Mountain Gate"
+    "location":"Git Crystal"
 }
 
"""
            self.assertEqual(game.output, expected)
        reset_repo()
        command = ['git', '-C', 'game-repo', 'branch','-D', 'trial']
        process = cw.run_process(command)

unittest.main()
