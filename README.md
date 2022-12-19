# HATETRIS - in Python
This is the Python emulator of qntm's [HATETRIS](https://qntm.org/files/hatetris/hatetris.html) game.

The Tetris and Genetic Algorithm Tetris solvers are based on hiyuzawa's [tetris_ai](https://github.com/hiyuzawa/tetris_ai).

## Setup
I have tested it with Python 3.9.6 on Windows 10 and macOS 12.6.1.
```shell
# Clone the repository
git clone
cd hatetris-python
# Install dependencies
pip install -r requirements.txt
```

## Usage
**Play mode**: You can play the game with the arrow keys. Almost all the features of the original game are implemented.
If you game over, you can see the score and the number of lines you cleared, and string of hexadecimal to replay.
```shell
python3 play.py
```
**Replay mode**: You can replay the game with the string of hexadecimal.
```shell
python3 replay.py
# Example 11 lines of replay data
Enter the code: ϥقໂɝƐඖДݹஶʈງƷ௨ೲໃܤѢقҾחࢲටฅڗ௨ΡІݪ௨ళȣݹࢴටງ໒௨ஶໃܥ௨റІݮ௨ఴІݥذඡଈݹƍق๓অஒॴแђञඖЅи௨sǶɔۑడПݷޠقԩݹࠉൿຟɓతණງஈশ੬෪অࠑථධٽଫ൝ଆࡨশ૫СܭߜయլݚɶऋഭܭرɤธӃస൯
```
**Genetic Algorithm mode**: You can see the result of the Genetic Algorithm. 
In each generation, the best model's selected and displaying the result of emulation including the score, lines, and the string of hexadecimal.
If you want to stop the process, press Ctrl+C.
```shell
python3 main.py
```

### configurations
You can change the configurations in `config.py`.
The default configurations are:
```python
elitism_pct = 0.2           # percentage of the best individuals to keep
mutation_prob = 0.2         # probability of mutation
weights_mutate_power = 0.5  # power of mutation for weights
```
and the population size settings is in `main.py`:
```python
pop_size = 50 # population size
```

## What I implemented
- `hatetris.py`
  - The HATETRIS AI tetrimino generator (enemy-ai)
    - including the global search method
- `replay_codecs`
  - A python package for encoding and decoding the replay data
  - The encoding and decoding methods are based on the original JavaScript code
  - For details, see [replay_codecs/README.md](replay_codecs/README.md)
