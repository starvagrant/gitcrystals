#!/usr/bin/env python3

from project.gitcli import GitCmd
from project.jsondata import JsonData
import project.gitglobals as G
import project.command_wrapper as cw
import unittest
import subprocess

class Tests(unittest.TestCase):
    def setUp(self):
        G.reset_repo()
        G.test_clean_repo()

    def tearDown(self):
        G.reset_repo()

    # Test game quits correctly
    def test_do_quit(self):
        git = GitCmd()
        self.assertTrue(git.do_quit(''))

    def test_is_player_alive(self):
        git = GitCmd()
        git.alive.data['alive'] = False
        git.alive.write()
        self.assertFalse(git.is_player_alive())

        git.alive.data['alive'] = True
        git.alive.write()
        self.assertTrue(git.is_player_alive())

    def test_loop_exit(self):
        git = GitCmd()
        git.alive.data['alive'] = True
        git.alive.write()

        git_loop_exits1 = git.do_checkoutfile('alive.json')
        git_loop_exits2 = git.do_checkout('data')
        git_loop_exits3 = git.do_checkoutforce('data')
        git_loop_exits4 = git.do_merge('data')
        git_loop_exits5 = git.do_resolveleft('alive.json')
        git_loop_exits6 = git.do_resolveleft('alive.json')

        self.assertTrue(git_loop_exits1)
        self.assertTrue(git_loop_exits2)
        self.assertTrue(git_loop_exits3)
        self.assertTrue(git_loop_exits4)
        self.assertTrue(git_loop_exits5)
        self.assertTrue(git_loop_exits6)

    def test_do_revlist(self):
        git = GitCmd()
        git.do_revlist('')
        head_commit = git.output.split('\n')[0]
        self.assertEqual(head_commit, G.current_commit_sha)

    def test_branch(self):
        git = GitCmd()
        git.do_branch('newbranch')

        command = [G.GIT, '-C', G.repodir, 'branch']
        process = cw.run_process(command)
        output = process.stdout

        command = [G.GIT, '-C', G.repodir, 'branch', '-D', 'newbranch']
        process = cw.run_process(command)

        expected = "* data\n  newbranch\n"
        self.assertEqual(output, expected)

    def test_listbranches(self):
        git = GitCmd()
        git.do_listbranches('')

        expected = "* data\n"
        self.assertEqual(git.output, expected)

    def test_checkout_same_ref(self):
        git = GitCmd()
        git.do_branch('newbranch')

        command = [G.GIT, '-C', G.repodir, 'checkout','newbranch']
        process = cw.run_process(command)

        git.do_checkout('newbranch')
        git.do_listbranches('')
        expected = "  data\n* newbranch\n"
        actual = git.output

        command = [G.GIT, '-C', G.repodir, 'checkout',G.current_branch]
        process = cw.run_process(command)
        command = [G.GIT, '-C', G.repodir, 'branch', '-d', 'newbranch']
        process = cw.run_process(command)

        self.assertEqual(actual, expected)

    def test_checkout_file(self):
        git = GitCmd()
        with open(G.repodir + '/README.md', 'a') as f:
            f.write("##Test Header")

        git.do_checkoutfile('README.md')

        command = [G.GIT, '-C', G.repodir, 'status','--short']
        process = cw.run_process(command)

        expected = ''
        self.assertEqual(process.stdout, expected)

    def test_stage(self):
        git = GitCmd()
        G.change_location_file("Git Crystal")
        git.do_stage('location.json')

        command = [G.GIT, '-C', G.repodir, 'status','--short']
        process1 = cw.run_process(command)

        G.change_location_file("Mountain Gate")
        command = [G.GIT, '-C', G.repodir, 'reset','HEAD','location.json']
        process2 = cw.run_process(command)

        expected = 'M  location.json\n' # location.json is staged
        self.assertEqual(process1.stdout, expected)

    def test_unstage(self):
        git = GitCmd()
        G.change_location_file("Git Crystal")
        git.do_stage('location.json')
        git.do_unstage('location.json')

        command = [G.GIT, '-C', G.repodir, 'status','--short']
        process = cw.run_process(command)
        G.change_location_file("Mountain Gate")

        expected = ' M location.json\n' # location.json has unstaged changes
        self.assertEqual(process.stdout, expected)

    def test_commit(self):
        git = GitCmd()
        G.change_location_file("Git Crystal")
        git.do_stage('location.json')
        git.do_commit('Player in Git Crystal')

        command = [G.GIT, '-C', G.repodir, 'show-ref','--heads']
        process = cw.run_process(command)
        self.assertNotEqual(process.stdout, G.current_commit_sha + " refs/heads/" + G.current_branch + '\n')

    def test_status_format(self):
        git = GitCmd()
        unstaged_change = git.format_status(' M location.json\n')
        expected = "    unstaged changes: location.json\n"
        self.assertEqual(unstaged_change, expected)
        staged_change = git.format_status('M  location.json\n')
        expected = "    staged changes: location.json\n"
        self.assertEqual(staged_change, expected)

    def test_status(self):
        git = GitCmd()
        git.do_status('')

        expected = 'No changes since last commit\n'
        self.assertEqual(git.output, expected)

        G.change_location_file("Git Crystal")

        git.do_status('')
        expected = "    unstaged changes: location.json\n"
        self.assertEqual(git.output, expected)

        git.do_stage('location.json')
        git.do_status('')
        expected = "    staged changes: location.json\n"
        self.assertEqual(git.output, expected)

        G.change_location_file("Stalagmite Central")
        git.do_status('')
        expected = '    staged changes: location.json\n    unstaged changes: location.json\n'
        self.assertEqual(git.output, expected)

    def test_git_log(self):
        git = GitCmd()
        git.do_log('')

        expected="""commit {} (HEAD -> data)
Author: James Ginns <starvagrant@yahoo.com>
Date:   Thu Jun 27 22:07:42 2019 -0500

    Basic Game Data

commit 75f9ce255a19d4f4b347b679e00ebee2ad027046 (tag: first-commit)
Author: James Ginns <starvagrant@yahoo.com>
Date:   Mon Jun 24 02:46:16 2019 -0500

    Explain the data repository to user
""".format(G.current_commit_sha)

        self.assertEqual(git.output, expected)

    def test_git_graph(self):
        git = GitCmd()
        git.do_graph('')
        expected = """* {} (HEAD -> data) Basic Game Data
* 75f9ce2 (tag: first-commit) Explain the data repository to user
""".format(G.current_commit_sha[:7])

        self.assertEqual(git.output, expected)

    def test_git_diff(self):
        git = GitCmd()

        G.change_location_file("Git Crystal")
        git.do_diff('')

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
        self.assertEqual(git.output, expected)

        git.do_stage('location.json')
        git.do_diffstaged('')
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
        self.assertEqual(git.output, expected)

    def test_git_diffbranch(self):
        git = GitCmd()
        git.do_branch('trial')
        G.change_location_file("Git Crystal")
        git.do_stage('location.json')
        git.do_commit('Player in Git Crystal')
        git.do_diffbranch('')

        expected = "only " + "data,trial are legal branch names\n"
        expected += "usage: diffbranch branch1 branch2\n"
        self.assertEqual(git.output, expected)

        git.do_diffbranch('trial data')
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
        self.assertEqual(git.output, expected)
        command = [G.GIT, '-C', G.repodir, 'branch','-D', 'trial']
        process = cw.run_process(command)

    def test_no_conflict_recursive_merge(self):
        git = GitCmd()
        git.do_merge('')
        expected = "No branch names provided"
        self.assertEqual(git.output, expected)

        git.do_merge('octupus merge')
        expected = "Git Crystals does not support merging mulitple branches"
        self.assertEqual(git.output, expected)

        git.do_branch('trial')
        git.do_checkout('trial')
        G.change_location_file("Git Crystal")
        git.do_stage('location.json')
        git.do_commit('Player in Git Crystal')
        git.do_checkout('data')
        git.do_merge('trial')

        command = [G.GIT, '-C', G.repodir, 'branch','-D', 'trial']
        process = cw.run_process(command)

        expected = """Merge made by the 'recursive' strategy.
 location.json | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
"""
        self.assertEqual(git.output, expected)

    def test_merge_with_conflicts(self):
        git = GitCmd()

        git.do_branch('trial')
        G.change_location_file("Git Crystal")
        git.do_stage('location.json')
        git.do_commit('Player in Git Crystal')
        git.do_checkout('data')
        G.change_location_file("Stalagmite Central")
        git.do_stage('location.json')
        git.do_merge('trial')
        git.do_resolveleft('location.json')
        git.do_resolveright('location.json')
        git.do_stage('location.json')
        git.do_commit('Merge Branch Trial')
        git.do_status('') # Get status message after successful merge resolution.

        command = [G.GIT, '-C', G.repodir, 'branch','-D', 'trial']
        process = cw.run_process(command)

        expected = 'No changes since last commit\n'
        self.assertEqual(git.output, expected)

if __name__ == '__main__':
    unittest.main()
