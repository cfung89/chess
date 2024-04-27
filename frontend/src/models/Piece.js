import { Position } from "./Position";

export class Piece {
    image; //string
    position; //Position
    type; //PieceType;
    colour; //TeamType;
    possibleMoves; // Position[]
    hasMoved; // boolean

    constructor(position, type, colour, hasMoved, possibleMoves = []) {
        this.image = `assets/images/${colour}${type}.png`;
        this.position = position;
        this.colour = colour;
        this.team = team;
        this.possibleMoves = possibleMoves;
        this.hasMoved = hasMoved;
    }
}