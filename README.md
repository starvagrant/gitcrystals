# Git Crystals
## A Text Based Game Based on The git versional control program

The following contains a program, gitcrystals.py, the purpose of which is
to be a text-based video game that uses git as it's system for managing
save data. This is to serve the following purposes.

1. For beginning users of git, it provides a relatively simple way to
practice using a version of git designed with beginners in mind. While
git internals are sound, the terminology and interface provided to an
initial user is muddy and confusing. All commands in git are in english,
not the "git"-ese that inhabits technical documentation like man pages.
2. For current users of git, this should be a fun puzzle game with the
unusual mechanic of having game information saved in a repository 
rather than a file. You will have to use git's ability to enable non-
linear workflow to solve game problems and discover the game's multiple
endings.

## Dependencies

The program requires a relatively up-to-date python 3 interpreter with 
standard library and a relatively update to date version of git installed 
on your system. My current dev machine is a dual-booting OS-X 10.12/
Ubuntu 18.04 system, and I'm developing this program for Linux first.
As such, the program should work on any linux system with python 3.6+
and git 2.17+. As the program comes further along I will start testing
on other operating systems, python versions, and git versions. To the
extent that they become available. I currently have no means of testing
on MS-Windows.

## On Git Configs / External Git Usage

The program uses python as a wrapper to call git commands installed on
the system. The means an unusual or unexpected git configuration might
cause the program to not work. It will create a genuine repository to
save your game data. It is not recommended that you use regular git
on this repository. It may leave the repository in a state that I
am unable to account for programatically. *IF* you become comfortable
with the program and know what you are doing, you might exit the
program to manually resolve a merge conflict. Internally the game
always resolves conflicts via the 'ours' or 'theirs' strategies.

## How the CLI program differs from command line git

1. There are a great reduction in the available commands.
2. Some commands are aliased to emphasize what's actually
being done. Add a change to the staging area is accomplished
by git stage, and removing a file from the staging area is
accomplished by git unstage.
3. The program actually explains changes when using git diff.
Rather than displaying a patch file, it explains which files
are changed in what commit. While learning to read a patch
file is genuinely helpful later in your git usage, it is
a distraction during learning.
4. The game does not allow fast-forward merges. This is to
encourage new users to think of branches as separate lines
of development, even if it results in empty merge commits.
5. Certain options and command syntax are not quite the same.
The game uses the word `file` in place where git would use
`--`. Also, any action that makes command line get say 'are
you sure?' requires the word force. So for example:
    - `git branch -D <some_branch>` becomes `git force delete branch <some_branch>`
    - `git checkout -f <some_branch>` becomes `git force checkout <some_branch>`
    - `git checkout -- <some_file.txt>` becomes `git checkout file <some_file.txt>`

Typing English commands is always preferred to the more flexible
but higher learning curve of git as it would be called in bash.
The game can be set to echo out the real command used in git.
