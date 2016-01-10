# IntelliDJ

This project takes a Spotify playlist, and finds the most optimum ordering of said playlist, so that song transitions involve similar songs.

This works using the EchoNest Track API, coupled with genetic algorithms, to generate an ideal mix.

Known Problems:
  > Crossover of two mixes can result in duplication of tracks. This should be eliminated in the breed function.
  > Each generation should involve more than one breeding of two mixes. This is simple, just put the code in a loop!
  > Exceptions should be thrown when certain errors occur. Validation is also needed.
