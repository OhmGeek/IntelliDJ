# IntelliDJ
## What this does
This project takes a Spotify playlist, and finds the most optimum ordering of said playlist, so that song transitions involve similar songs.

This works using the EchoNest Track API, coupled with genetic algorithms, to generate an ideal mix.

## Problems
While developing this, I discovered that libspotify was depreciated, and so playing the created playlists became more difficult. The solution was to get the information about each track and then manually create a playlist with this information. Creation of playlists can be automated, but playing them cannot be.

Algorithm problems were also present:
  - When two mixes are crossed over, duplication of tracks can occur. This can be resolved by adjusting the breed function to ignore any duplicates.
  - Each generation should involve more than one iteration of the breeding of two mixes. A simple loop is needed here to fix the issue!
  - Exceptions should be used when errors occur. More validation is also needed to make the program more usable. This project is merely an experiment and so the code was designed as a quick proof of concept rather than a robust and stable program.


