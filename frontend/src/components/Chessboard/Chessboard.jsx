import React, {useRef} from 'react';
import Tile from '../Tile/Tile';
import './Chessboard.css';

const pieces = [];

for(let i = 0; i < 8; i++) {
	pieces.push({image: "assets/bp.png", x: i, y: 6})
	pieces.push({image: "assets/wP.png", x: i, y: 1})
}
pieces.push({image: "assets/br.png", x: 0, y: 7})
pieces.push({image: "assets/br.png", x: 7, y: 7})
pieces.push({image: "assets/wR.png", x: 0, y: 0})
pieces.push({image: "assets/wR.png", x: 7, y: 0})

pieces.push({image: "assets/bn.png", x: 1, y: 7})
pieces.push({image: "assets/bn.png", x: 6, y: 7})
pieces.push({image: "assets/wN.png", x: 1, y: 0})
pieces.push({image: "assets/wN.png", x: 6, y: 0})

pieces.push({image: "assets/bb.png", x: 2, y: 7})
pieces.push({image: "assets/bb.png", x: 5, y: 7})
pieces.push({image: "assets/wB.png", x: 2, y: 0})
pieces.push({image: "assets/wB.png", x: 5, y: 0})

pieces.push({image: "assets/bq.png", x: 3, y: 7})
pieces.push({image: "assets/bk.png", x: 4, y: 7})
pieces.push({image: "assets/wQ.png", x: 3, y: 0})
pieces.push({image: "assets/wK.png", x: 4, y: 0})

const ranks = ["1", "2", "3", "4", "5", "6", "7", "8"];
const files = ["a", "b", "c", "d", "e", "f", "g", "h"];

let activePiece = null;


export default function Chessboard() {
	const chessboardRef = useRef(null);

	function grabPiece(e) {
		const element = e.target;
		if(element.classList.contains("chess-piece")) {
			const x = e.clientX - 50;
			const y = e.clientY - 50;
			element.style.position = "absolute";
			element.style.left = `${x}px`;
			element.style.top = `${y}px`;

			activePiece = element;
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
		if(activePiece){
			activePiece = null;
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