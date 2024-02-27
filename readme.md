This is more of a note for myself to not overcomplicate the next time I am
implementing a parser.

`parse.py` is 150 lines of code for a fully self-contained lexer and parser
that handles associativity, precedence, grouping, prefix, infix, and suffix
operators for a simple arithmetic grammar. To try it out, use:

```
python3 parse.py '2 + - ( 3 ! ^ 4 ) * 5 - 2 / 6'
```

Because it's not the interesting part, the lexer is extremely rudamentary, and
all the tokens need to be separated by whitespace.

It's actually extremely surprising to me that the meat of the parser is just 3
functions and the entire thing can be implemented in about 50 lines of code. A
while loop and a bit of recursion.

None of this is original work, I have just collected random bits and pieces
from various sources and condensed them into a single file and minimized the
amount of code. Sources I have taken from:

 - https://journal.stuffwithstuff.com/2011/03/19/pratt-parsers-expression-parsing-made-easy/
 - https://github.com/munificent/bantam/
 - https://www.youtube.com/watch?v=fIPO4G42wYE
