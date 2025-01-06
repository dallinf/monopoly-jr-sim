A simulation of the [Monopoly Jr. board game](https://www.hasbro.com/en-us/product/monopoly-jr-board-game).

## Usage

```bash
python mjr.py
```

### With UI

```bash
python mjr_ui.py
```

#### Installation

This was a pain on my Mac. I use asdf to manage my Python versions. This is what I did:

1. Install python-tk

```bash
brew install python-tk@3.11
```

2. Install Tcl and Tk

```bash
brew install tcl-tk
```

3. Install pkg-config

```bash
brew install pkg-config
```

4. Install Python

```bash
PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I/opt/homebrew/Cellar/tcl-tk/9.0.1/include/tcl-tk' --with-tcltk-libs='$(pkg-config tk --libs)'" asdf install python 3.11.5
```

5. Test the installation

```bash
python -m tkinter -c "tkinter._text()"
```

## Summary

I play this game with my kids a lot. Sometimes, the game just goes
on and on... So, I wondered how long the average game takes and how often we get an "endless" game. This simulation runs 10,000 games and prints out the results.

## Latest Results

Average turns: 14.1245
Max turns: 1000
Min turns: 4
Average turns for games under 20 turns: 9.6197
Games with turns over 10: 63.20%
Games with turns over 20: 10.82%
Games with turns over 30: 3.72%
Games with turns over 40: 1.69%
Games with turns over 50: 1.03%
Games with turns over 100: 0.33%
Games with no winner: 0.09%
Player 1 wins: 32.93%
Player 2 wins: 26.72%
Player 3 wins: 21.52%
Player 4 wins: 18.74%

## Conclusions

Assuming this simulation is correct...

1. Go first if your kid lets you.
2. 10% of the time, the game has more than 20 turns. You'll want to bail long before that.
