TwitBot
=======

A simple twitter bot which tweets lines from a text file.

To use:

1. install python-twitter & all the modules it needs

2. if you don't already have an account to use & the credentials to go with (from dev.twitter.com), get that sorted

3. populate totweet.txt with the tweets you want to send, one on each line. Current facts are from various threads on reddit.com

4. in login.py, replace 'Consumer Key' etc. with your keys and tokens

5. run RunBot.py, and hope for the best!

(if it throws an error saying it can't import 'mylogin' that's because I've forgotten to change it from my personal 'mylogin' file with my own credentials in to the generic 'login' where the user can place theirs. Just replace "import mylogin" in RunBot.py with "import login" and drop me a note. Thanks!)



