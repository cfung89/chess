import React, {useState, useRef, useEffect} from 'react';
import Tile from '../Tile/Tile';
import './Chessboard.css';

const pieces = [];

const ranks = ["1", "2", "3", "4", "5", "6", "7", "8"];
const files = ["a", "b", "c", "d", "e", "f", "g", "h"];

const initialBoardState = [];
for(let i = 0; i < 8; i++) {
	initialBoardState.push({image: "assets/bp.png", x: i, y: 6})
	initialBoardState.push({image: "assets/wP.png", x: i, y: 1})
}
initialBoardState.push({image: "assets/br.png", x: 0, y: 7})
initialBoardState.push({image: "assets/br.png", x: 7, y: 7})
initialBoardState.push({image: "assets/wR.png", x: 0, y: 0})
initialBoardState.push({image: "assets/wR.png", x: 7, y: 0})

initialBoardState.push({image: "assets/bn.png", x: 1, y: 7})
initialBoardState.push({image: "assets/bn.png", x: 6, y: 7})
initialBoardState.push({image: "assets/wN.png", x: 1, y: 0})
initialBoardState.push({image: "assets/wN.png", x: 6, y: 0})

initialBoardState.push({image: "assets/bb.png", x: 2, y: 7})
initialBoardState.push({image: "assets/bb.png", x: 5, y: 7})
initialBoardState.push({image: "assets/wB.png", x: 2, y: 0})
initialBoardState.push({image: "assets/wB.png", x: 5, y: 0})

initialBoardState.push({image: "assets/bq.png", x: 3, y: 7})
initialBoardState.push({image: "assets/bk.png", x: 4, y: 7})
initialBoardState.push({image: "assets/wQ.png", x: 3, y: 0})
initialBoardState.push({image: "assets/wK.png", x: 4, y: 0})

export default function Chessboard() {
	const [activePiece, setActivePiece] = useState(null);
	const [gridX, setGridX] = useState(0);
	const [gridY, setGridY] = useState(0);
	const [pieces, setPieces] = useState(initialBoardState);
	const chessboardRef = useRef(null);

	function grabPiece(e) {
		const element = e.target;
		const chessboard = chessboardRef.current;
		if(element.classList.contains("chess-piece") && chessboard) {
			setGridX(Math.floor((e.clientX - chessboard.offsetLeft) / 100));
			setGridY(Math.abs(Math.ceil((e.clientY - chessboard.offsetTop - 800) / 100)));

			const x = e.clientX - 50;
			const y = e.clientY - 50;
			element.style.position = "absolute";
			element.style.left = `${x}px`;
			element.style.top = `${y}px`;

			setActivePiece(element);
		}
	}

	function movePiece(e) {
		const chessboard = chessboardRef.current;
		if(activePiece && chessboard) {
			const minX = chessboard.offsetLeft - 25;
			const minY = chessboard.offsetTop - 25;
			const maxX = chessboard.offsetLeft + chessboard.clientWidth - 75;
			const maxY = chessboard.offsetTop + chessboard.clientHeight - 90;
			const x = e.clientX - 50;
			const y = e.clientY - 50;
			activePiece.style.position = "absolute";

			if (x < minX) {
				activePiece.style.left = `${minX}px`
			} else if (x > maxX) {
				activePiece.style.left = `${maxX}px`
			} else {
				activePiece.style.left = `${x}px`
			}

			if (y < minY) {
				activePiece.style.top = `${minY}px`
			} else if (y > maxY) {
				activePiece.style.top = `${maxY}px`
			} else {
				activePiece.style.top = `${y}px`
			}
		}
	}

	function dropPiece(e) {
		const chessboard = chessboardRef.current;
		if(activePiece && chessboard){
			const x = Math.floor((e.clientX - chessboard.offsetLeft) / 100);
			const y = Math.abs(Math.ceil((e.clientY - chessboard.offsetTop - 800) / 100));

			setPieces((value) => {
				const pieces = value.map(p => {
					if (p.x === gridX && p.y === gridY) {
						p.x = x;
						p.y = y;
					}
					return p;
				});
				return pieces;
			});
			setActivePiece(null);
		}
	}

	let board = [];

	//Loads everything from bottom left to top right
	for (let j = ranks.length-1; j >= 0; j--) {
		for (let i = 0; i < files.length; i++) {
			let image = undefined;

			pieces.forEach(p => {
				if (p.x === i && p.y === j) {
					image = p.image
				}
			});

			board.push(<Tile key={`${j}, ${i}`} coords={j + i + 2} image={image} />);
		}
	}
	return <div 
				onMouseMove={e => movePiece(e)} 
				onMouseDown={e => grabPiece(e)} 
				onMouseUp={e => dropPiece(e)}
				ref={chessboardRef}
				id="chessboard"
			>
				{board}
			</div>
}
