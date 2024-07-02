# Chess KRK-Endgame AI

## Overview

This project implements a chess KRK endgame AI using a game tree search algorithm with heuristics to determine wheter positions are better or worse.
It provides a minimalistic UI to play against the program. The program plays as white with a material advantage. All concepts and many methods are
direct implementations of 'Huberman, Barbara Jane. A program to play chess end games. No. 65. Stanford University, 1968.' According to this dissertation the program cannot lose.

The project was done for academic purposes.

## Features

- Set up custom board configurations.
- Automatically find a good move for the given board configuration and force the win for the program.
- Provides a simple web interface for interaction.
- Possibility to show the search tree.

## Requirements

- Can be found in requirements.txt

## Deployment

The program can be deployed locally by following the steps below: 

1. Clone the repository:

    ```bash
    git clone https://github.com/nikli2507/krk_chess_game
    cd krk_chess_game
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python app.py
    ```

4. Open your browser and go to `http://http://127.0.0.1:8080/`

Or on the Google Cloud:

Instead of step 3 and 4 do:

1. Build the docker image:

    ```bash
    docker build -t krk_chess_game .
    ```

2. Tag the image to your cloud project:

    ```bash
    docker tag krk_chess_game gcr.io/<project_id>/krk_chess_game
    ```

3. Push the image to your cloud project

    ```bash
    docker push gcr.io/<project_id>/krk_chess_game
    ```

4. Run the image in a container in the Google Cloud UI

## API Endpoints

All endpoints are automatically called from the UI.

- `GET /setup`: Returns the FEN string of the default board.
- `POST /custom_setup`: Returns the FEN string of the given FEN or KRK piece positions. Resets the current search tree root.
- `POST /move`: Returns a good move for the given board position. Internally saves the tree.
