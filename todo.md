## Ideas for Refactoring Git Project

1. There is no need to couple the game logic and the git
logic. In a previous incarnation placing them in separate
classes allowed the game to enter two states (one while
dead, the other alive). Having the following structure

    GameCli
    GitCli
    cmd.Cmd()

will allow for simpler tests, easier implements of different
git shells for the same game, different games that use the
same structure, git shell, etc.

2. Standardize calls to the subprocess module. I discovered
there was a way in which all my calls to the computer's outside
git installation worked corrected and another one that didn't.
I need to standardize how the system's external git is called.
I'm also interested in changing the systems I use so the game
can be used directly from a Mac with git (i.e. python 2.7)
While I defined support as a goal for the 1.0 release, the
least I could do is call processes the same way on POSIX
systems.

3. Simplify end user syntax with wrapper functions. To avoid
a small amount of work, I gave names to every function, instead
of parsing spaces, and ended up with commands like listbranches
I had a naming scheme which I removed, it might be a good place
to start. The point here being to remove the "git-ese" or the
alternate syntax used in bash and general english.

4. Perhaps give the user the ability to specify git's normal
CLI syntax rather than the syntax I'm working on to make the
game easier to learn for new git users. Given that internally
I'm calling git as it would be called on the command line, this
should be too hard.

5. I should have a way to make sure the user's git works as
intended. This game in the wild with have to contend with a
number of different settings. While this is a strength, there
may have to be some settings placed in the repo. I'm especially
thinking about the CRLF and LF line endings at this point, because
it will eventually become an issue.

6. Remove print statements wherever possible, and use internal
functions for printing. While this may do little but wrap a
function around print statements, it will give me the opportunity
to test things cleaner.

7. The game plot idea I have for git crystals is somewhat uninspired,
in comparison to how different the game is in general. At some point
I'll be interested in more than saving a princess from a dragon, but
it does give me a good point to start out with.
