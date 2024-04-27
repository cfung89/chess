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
	console.log("hi")
	/*
	fetch("http://127.0.0.1:5000/create", {
		method: "POST",
		body: JSON.stringify({fen: fen}),
		headers: {"Content-type": "application/json"}
	})
		.then((response) => response.json())
		.then((json) => console.log(json));
	*/

	return (
		<>	
			<div className='app username'>hi</div>
			<div id="app">
				<Chessboard fen={fen} />
			</div>
		</>
  	);
}

export default App
