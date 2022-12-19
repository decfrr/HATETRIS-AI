# replay-codecs
This is a Python package for encoding and decoding the replay data of HATETRIS.
All codes are based on the original [HATETRIS](https://github.com/qntm/hatetris/tree/main/src/replay-codecs)
and [base2048 codecs](https://github.com/qntm/base2048).

# Requirements
- numpy

## Usage
```python
from replay_codecs.codec import encode, decode

# encode
# input: list of keyboard events
# output: string of hexadecimal
print(encode(['D', 'D', 'D', 'R', 'U', 'D'])) #'ਹԇ'

# decode
# input: string of hexadecimal
# output: list of keyboard events
print(decode('ਹԇ')) #['D', 'D', 'D', 'R', 'U', 'D']
```

