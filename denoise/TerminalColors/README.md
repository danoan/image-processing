# TerminalColors

## What is it for ?

(Python) TerminalColors is a simple, small library for outputting/printing colored text to terminal-stdout.

## Example

```python
#!/usr/bin/env python

from TerminalColors import *

cprint('This text is', RED, ' red', RESET, ' and ', RED, BOLD, 'bold', RED, '.')
error('This is a simple, small error message.')
```
