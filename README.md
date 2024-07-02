# Chess KRK-Endgame AI

## Overview

The application implements an AI playing King-Rook-King-endgames. The AI plays with the material advantage against an arbitrary user. All concepts and some methods are direct implementations from 'Huberman, Barbara Jane. A program to play chess end games. No. 65. Stanford University, 1968.', which is a dissertation proposing a strategy to play certain chess endgames. Especially chapter 3 (definition of better and worse) and 4 (rook and king against king) are used. The paper also describes how an AI playing different endgames than KRK can work, but this program only implements the KRK approach.
The basic idea of the dissertation is to define functions better and worse to create a heuristic how good a board position is in comparison to another. The program starts with the current position and compares it to theoretical future board positions. It does this via tree search. If the AI finds a branch where it can force a better position, then it makes the move leading to a position in this branch. The worse function is used for branch pruning. The main part of the implementation is the tree search algorithm and the implementation of better and worse. Internally they use sub-heuristics called stages and measures, described in more detail in the mentioned dissertation. 


The project was done for academic purposes.

## Features

- Play against the AI
- See heuristic information: current stage, measure, distance to mate when playing optimal, the total number of white moves
- Setup a custom board position
- See the current search tree used to find a good move
- Access the Flask-API if needed

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

- `GET /setup`: Returns the FEN string of the default board and corresponding heuristic information. Resets the current search tree root.
- `POST /custom_setup`: Returns the FEN string of the given KRK piece positions and corresponding heuristic information. Resets the current search tree root.
- `POST /move`: Returns a good move for the given board position, corresponding heuristic information and a HTML visualization of the search tree. Internally saves the tree.
