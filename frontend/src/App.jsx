import './App.css';
import Chessboard from './components/Chessboard/Chessboard';


/*
function decryptFen(fen) {
	const board = fen.split("/");
	return board;
}
*/

function App() {
	let fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
	/*

	fetch("http://127.0.0.1:5000/create", {
		method: "POST",
		body: JSON.stringify({fen: fen}),
		headers: {"Content-type": "application/json"}
	})
		.then((response) => response.json())
		.then((json) => console.log(json));
	//console.log(response)
*/
	return (
		<>	
			<div id="app">
				<Chessboard fen={fen} />
			</div>
		</>
				//<p className='text username'>Player 2</p>
				//<p className='text username'>Player 1</p>
  	);
}

export default App
