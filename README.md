Youtrack_Bitbucket_Broker
=========================

# Purpose #
This is a flask broker that will listen for POST hooks from your bitbucket repository, process them and post them as a comment to youtrack.

# Requirements #
To use this brokr you need:

*Flask

*Python 2.7

*[Pytrack](https://github.com/crimsondesigns/PyTrack)

*Requests

*Youtrack 4.0 and newer (This has not been tested on anything before 4.0)

# Usage #
Download this and Pytrack into the same directory for ease of use.
On line 116:

    p = pytrack(<YOUTRACK_URL>, <YOUTRACK_PORT>, <USERNAME>, <PASSWORD>)
  
Change the variables to "http://YourYouTrackURL", 1234(Your Port), "Username", "Password"

When you commit your code you'll need to include the ticket number in the commit message.

Based on my experience they look like: "XXX-000". Any number of characters followed by a dash and the associated number.

You can change the regex on line 37 to meet your needs here.
