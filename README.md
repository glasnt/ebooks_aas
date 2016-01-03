# eBooks as a Service

Based on the work of [Tom Meagher](https://github.com/tommeagher) and their [Heroku eBooks](https://github.com/tommeagher/heroku_ebooks) code. 

## Purpose

[eBooks accounts](https://en.wikipedia.org/wiki/Horse_ebooks) tweet 'nonsence' content based on a Markov chain of a specific source count. This code sources all these accounts as it's contrent. An ebooks of ebooks, if you will. 

## Tech spec

Using a list of the follows of the `TWEET_ACCOUNT` as the input sources, the code gets at most `PAGE_SIZE * PAGE` of tweets from each account, markov chain's them together, and tweets the result. 

Limitations: it will specifically not tweet if the resultant exactly matches what other bots have tweeted. 

## More about the underlying code

See the `heroku_ebooks_readme.md`
