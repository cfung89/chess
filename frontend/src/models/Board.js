import { getPossibleBishopMoves, getPossibleKingMoves, getPossibleKnightMoves, getPossiblePawnMoves, getPossibleQueenMoves, getPossibleRookMoves, getCastlingMoves } from "../referee/rules";
import { PieceType, TeamType } from "../Types";
import { Pawn } from "./Pawn";
import { Piece } from "./Piece";
import { Position } from "./Position";
import getMoves from "../server/GetMoves";
import start from "../server/Start";

start();

export class Board {
    pieces;
    totalTurns;
    winningTeam;

    constructor(pieces, totalTurns) {
        this.pieces = pieces;
        this.totalTurns = totalTurns;
    }

    get currentTeam() {
        return this.totalTurns % 2 === 0 ? TeamType.OPPONENT : TeamType.OUR;
    }

    calculateAllMoves() {
        //const moves = getMoves();
        for (const piece of this.pieces) {
            /*
            const calculatedMoves = [];
            moves.then((value) => {
                console.log(value);
                for (let key in value) {
                    const origX = parseInt(key[1]);
                    const origY = parseInt(key[4]);
                    console.log(origX, origY);
                    if (piece.position.x === origX && piece.position.y === origY) {
                        console.log(origX, origY);
                        for (let i = 0; i < value[key].length; i++) {
                            const arr = value[key][i];
                            const newPos = new Position(arr[0], arr[1]);
                            calculatedMoves.push(newPos);
                            //console.log(calculatedMoves);
                        }
                    }
                    //console.log(key[1], key[4]);
                    //console.log(value[key]);
                    //console.log(value[key][0], value[key][1]);
                }
            });
            //piece.possibleMoves = this.calculatedMoves;
            */
            piece.possibleMoves = this.getValidMoves(piece, this.pieces);
        }

        // Calculate castling moves
        for (const king of this.pieces.filter(p => p.isKing)) {
            if (king.possibleMoves === undefined) continue;

            king.possibleMoves = [...king.possibleMoves, ...getCastlingMoves(king, this.pieces)];
            //console.log(king.possibleMoves);
        }

        // Check if the current team moves are valid
        this.checkCurrentTeamMoves();

        // Remove the possible moves for the team that is not playing
        for (const piece of
            this.pieces.filter(p => p.team !== this.currentTeam)) {
            piece.possibleMoves = [];
        }

        // Check if the playing team still has moves left
        // Otherwise, checkmate!
        if (this.pieces.filter(p => p.team === this.currentTeam)
            .some(p => p.possibleMoves !== undefined && p.possibleMoves.length > 0)) return;

        this.winningTeam = (this.currentTeam === TeamType.OUR) ? TeamType.OPPONENT : TeamType.OUR;
    }

    checkCurrentTeamMoves() {
        // Loop through all the current team's pieces
        for (const piece of this.pieces.filter(p => p.team === this.currentTeam)) {
            if (piece.possibleMoves === undefined) continue;

            // Simulate all the piece moves
            for (const move of piece.possibleMoves) {
                const simulatedBoard = this.clone();

                // Remove the piece at the destination position
                simulatedBoard.pieces = simulatedBoard.pieces.filter(p => !p.samePosition(move));

                // Get the piece of the cloned board
                const clonedPiece = simulatedBoard.pieces.find(p => p.samePiecePosition(piece));
                clonedPiece.position = move.clone();

                // Get the king of the cloned board
                const clonedKing = simulatedBoard.pieces.find(p => p.isKing && p.team === simulatedBoard.currentTeam);

                // Loop through all enemy pieces, update their possible moves
                // And check if the current team's king will be in danger
                for (const enemy of simulatedBoard.pieces.filter(p => p.team !== simulatedBoard.currentTeam)) {
                    enemy.possibleMoves = simulatedBoard.getValidMoves(enemy, simulatedBoard.pieces);

                    if (enemy.isPawn) {
                        if (enemy.possibleMoves.some(m => m.x !== enemy.position.x
                            && m.samePosition(clonedKing.position))) {
                            piece.possibleMoves = piece.possibleMoves?.filter(m => !m.samePosition(move));
                        }
                    } else {
                        if (enemy.possibleMoves.some(m => m.samePosition(clonedKing.position))) {
                            piece.possibleMoves = piece.possibleMoves?.filter(m => !m.samePosition(move));
                        }
                    }
                }
            }
        }
    }

    getValidMoves(piece, boardState) {
        switch (piece.type) {
            case PieceType.PAWN:
                return getPossiblePawnMoves(piece, boardState);
            case PieceType.KNIGHT:
                return getPossibleKnightMoves(piece, boardState);
            case PieceType.BISHOP:
                return getPossibleBishopMoves(piece, boardState);
            case PieceType.ROOK:
                return getPossibleRookMoves(piece, boardState);
            case PieceType.QUEEN:
                return getPossibleQueenMoves(piece, boardState);
            case PieceType.KING:
                return getPossibleKingMoves(piece, boardState);
            default:
                return [];
        }
    }

    playMove(enPassantMove, validMove, playedPiece, destination) {
        const pawnDirection = playedPiece.team === TeamType.OUR ? 1 : -1;
        const destinationPiece = this.pieces.find(p => p.samePosition(destination));

        // If the move is a castling move do this
        if (playedPiece.isKing && destinationPiece?.isRook
            && destinationPiece.team === playedPiece.team) {
            const direction = (destinationPiece.position.x - playedPiece.position.x > 0) ? 1 : -1;
            const newKingXPosition = playedPiece.position.x + direction * 2;
            this.pieces = this.pieces.map(p => {
                if (p.samePiecePosition(playedPiece)) {
                    p.position.x = newKingXPosition;
                } else if (p.samePiecePosition(destinationPiece)) {
                    p.position.x = newKingXPosition - direction;
                }

                return p;
            });

            this.calculateAllMoves();
            return true;
        }

        if (enPassantMove) {
            this.pieces = this.pieces.reduce((results, piece) => {
                if (piece.samePiecePosition(playedPiece)) {
                    if (piece.isPawn)
                        piece.enPassant = false;
                    piece.position.x = destination.x;
                    piece.position.y = destination.y;
                    piece.hasMoved = true;
                    results.push(piece);
                } else if (
                    !piece.samePosition(new Position(destination.x, destination.y - pawnDirection))
                ) {
                    if (piece.isPawn) {
                        piece.enPassant = false;
                    }
                    results.push(piece);
                }

                return results;
            }, []);

            this.calculateAllMoves();
        } else if (validMove) {
            //UPDATES THE PIECE POSITION
            //AND IF A PIECE IS ATTACKED, REMOVES IT
            this.pieces = this.pieces.reduce((results, piece) => {
                // Piece that we are currently moving
                if (piece.samePiecePosition(playedPiece)) {
                    //SPECIAL MOVE
                    if (piece.isPawn)
                        piece.enPassant =
                            Math.abs(playedPiece.position.y - destination.y) === 2 &&
                            piece.type === PieceType.PAWN;
                    piece.position.x = destination.x;
                    piece.position.y = destination.y;
                    piece.hasMoved = true;
                    results.push(piece);
                } else if (!piece.samePosition(destination)) {
                    if (piece.isPawn) {
                        piece.enPassant = false;
                    }
                    results.push(piece);
                }

                // The piece at the destination location
                // Won't be pushed in the results
                return results;
            }, []);

            this.calculateAllMoves();
        } else {
            return false;
        }

        return true;
    }

    clone() {
        return new Board(this.pieces.map(p => p.clone()),
            this.totalTurns);
    }
}