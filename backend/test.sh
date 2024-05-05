#! /bin/bash
#Initial tests. These tests may no longer be valid anymore since the class was modified a lot since then.

curl -X POST -H "Content-Type: application/json" -d '{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "usr_colour": "1"
}' http://localhost:5000/create

curl -X POST -H "Content-Type: application/json" -d '{
  "move": "d2d4"
}' http://localhost:5000/move

curl -X POST -H "Content-Type: application/json" -d '{
  "move": "g7g6"
}' http://localhost:5000/move
