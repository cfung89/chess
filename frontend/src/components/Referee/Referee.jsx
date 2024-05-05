import { useRef, useState } from "react";
import { initialBoard } from "../../Constants";
import { Piece, Position } from "../../models";
import { PieceType, TeamType } from "../../Types";
import Chessboard from "../Chessboard/Chessboard";
import postMove from "../../server/Post";
import getMoves from "../../server/GetMoves";
import start from "../../server/Start";
import botMove from "../../server/BotMove";
import { HORIZONTAL_AXIS } from "../../Constants";

export default function Referee() {
    const [board, setBoard] = useState(initialBoard.clone());
    const [promotionPawn, setPromotionPawn] = useState();
    const modalRef = useRef(null);
    const checkmateModalRef = useRef(null);

    function playMove(playedPiece, destination, bot=false) {
        // If the playing piece doesn't have any moves return
        if (playedPiece.possibleMoves === undefined) return false;

        // Prevent the inactive team from playing
        if (playedPiece.team === TeamType.OUR && board.totalTurns % 2 !== 1) return false;
        if (playedPiece.team === TeamType.OPPONENT && board.totalTurns % 2 !== 0) return false;
        // Bot move
        if (!bot) {
            if (playedPiece.team === TeamType.OPPONENT && board.totalTurns % 2 !== 1) return false;
        }
        let playedMoveIsValid = false;

        const validMove = playedPiece.possibleMoves?.some(m => m.samePosition(destination));

        if (!validMove) return false;

        const enPassantMove = isEnPassantMove(
            playedPiece.position,
            destination,
            playedPiece.type,
            playedPiece.team
        );

        // playMove modifies the board thus we
        // need to call setBoard
        setBoard(() => {
            const clonedBoard = board.clone();
            clonedBoard.totalTurns += 1;
            // Playing the move
            playedMoveIsValid = clonedBoard.playMove(enPassantMove, validMove, playedPiece, destination);

            if(clonedBoard.winningTeam !== undefined) {
                checkmateModalRef.current?.classList.remove("hidden");
            }

            return clonedBoard;
        })

        // This is for promoting a pawn
        let promotionRow = (playedPiece.team === TeamType.OUR) ? 7 : 0;

        if (destination.y === promotionRow && playedPiece.isPawn) {
            modalRef.current?.classList.remove("hidden");
            setPromotionPawn((previousPromotionPawn) => {
                const clonedPlayedPiece = playedPiece.clone();
                clonedPlayedPiece.position = destination.clone();
                return clonedPlayedPiece;
            });
        }

        postMove(playedPiece.position, destination);
        return playedMoveIsValid;
    }

    function isEnPassantMove(initialPosition, desiredPosition, type, team) {
        const pawnDirection = team === TeamType.OUR ? 1 : -1;

        if (type === PieceType.PAWN) {
            if ((desiredPosition.x - initialPosition.x === -1 || desiredPosition.x - initialPosition.x === 1) && desiredPosition.y - initialPosition.y === pawnDirection) {
                const piece = board.pieces.find((p) => p.position.x === desiredPosition.x && p.position.y === desiredPosition.y - pawnDirection && p.isPawn && p.enPassant);
                if (piece) {
                    return true;
                }
            }
        }

        return false;
    }

    function promotePawn(pieceType) {
        if (promotionPawn === undefined) {
            return;
        }

        setBoard((previousBoard) => {
            const clonedBoard = board.clone();
            clonedBoard.pieces = clonedBoard.pieces.reduce((results, piece) => {
                if (piece.samePiecePosition(promotionPawn)) {
                    results.push(new Piece(piece.position.clone(), pieceType,
                        piece.team, true));
                } else {
                    results.push(piece);
                }
                return results;
            }, []);

            clonedBoard.calculateAllMoves();

            return clonedBoard;
        })

        modalRef.current?.classList.add("hidden");
    }

    function promotionTeamType() {
        return (promotionPawn?.team === TeamType.OUR) ? "w" : "b";
    }
    
    function restartGame() {
        checkmateModalRef.current?.classList.add("hidden");
        setBoard(initialBoard.clone());
        start();
    }

    if (board.totalTurns % 2 !== 1) {
        let success = false
        while (!success) {
            const move = botMove();
            move.then((value) => {
                const origPos = new Position(HORIZONTAL_AXIS.indexOf(value.move[0]), parseInt(value.move[1])-1);
                const newPos = new Position(HORIZONTAL_AXIS.indexOf(value.move[2]), parseInt(value.move[3])-1);
                const currentPiece = board.pieces.find((p) => p.samePosition(origPos));
                if (currentPiece) {
                    success = playMove(currentPiece.clone(), newPos, true);
                    if (!success) {console.log("Unsuccessful move")}
                }
            });
        }
    }

    //console.log(board)
    return (
        <>
            <p style={{color: "white", fontSize: "16px", textAlign: "left"}}>Player 2</p>
            <div className="modal hidden" ref={modalRef}>
                <div className="modal-body">
                <img onClick={() => promotePawn(PieceType.ROOK)} src={`/assets/${promotionTeamType()}r.png`} />
                    <img onClick={() => promotePawn(PieceType.BISHOP)} src={`/assets/${promotionTeamType()}b.png`} />
                    <img onClick={() => promotePawn(PieceType.KNIGHT)} src={`/assets/${promotionTeamType()}n.png`} />
                    <img onClick={() => promotePawn(PieceType.QUEEN)} src={`/assets/${promotionTeamType()}q.png`} />
                </div>
            </div>
            <div className="modal hidden" ref={checkmateModalRef}>
                <div className="modal-body">
                    <div className="checkmate-body">
                        <span>The winning team is {board.winningTeam === TeamType.OUR ? "white" : "black"}!</span>
                        <button onClick={restartGame}>Play again</button>
                    </div>
                </div>
            </div>
            <Chessboard playMove={playMove} pieces={board.pieces} />
            <p style={{color: "white", fontSize: "16px", textAlign: "left"}}>Player 1</p>
        </>
    )
}