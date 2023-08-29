![Version](https://img.shields.io/badge/python-3.9|3.10|3.11-brightgreen)
[![Coverage Status](https://coveralls.io/repos/github/MathisNcl/lost_cities/badge.svg?branch=master)](https://coveralls.io/github/MathisNcl/lost_cities?branch=master)

# Lost Cities

Welcome to my personal implementation of the Lost Cities card game structure. This is a very entertaining card game created by Reiner Knizia. In this game, you play one-on-one to score as many points as possible. You can play it in 5 or 10 rounds, adding up your scores for each round.

In my implementation, it's possible to play against a computer that follows personal rules.

For the moment, there is no GUI (incoming). I am looking to set up an online interface to play with a friend or against a computer.

[Here to see latest modifications!](CHANGELOG.md)

## Rules

To check the rules: [click here](https://cdn.1j1ju.com/medias/c8/66/47-lost-cities-rulebook.pdf)

## Installation

- Clone repo
- Create venv with python between 3.9 and 3.11 and `make deps`

## How to play?

For graphicqal version, run in your terminal:

```sh
play-lost-gui
```

To play in your command line, run in your terminal:

```sh
play-lost
```

Then choose your name and if you will play against a computer. Enjoy!

## Possible enhancement

- GUI
- Dockerize
- Online
- Computer using reinforcement learning
