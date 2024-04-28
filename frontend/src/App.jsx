import './App.css';
import Referee from './components/Referee/Referee'
//import React, {useState, useRef, useEffect} from 'react';
//import {BASE} from './Constants';


/*
function decryptFen(fen) {
	const board = fen.split("/");
	return board;
}
*/



function App() {
	/*
	const [response, setResponse] = useState(null);
	const fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

	fetch(`${BASE}/create`, {
		method: "POST",
		body: JSON.stringify({fen: fen}),
		headers: {"Content-type": "application/json"}
	})
		.then(response => response.json())
		.then(data => setResponse(data))
		.catch(error => console.log(error));
	console.log(response);
				<p className='text username'>Player 2</p>
				<p className='text username'>Player 1</p>
	*/

	return (
		<>	
			<div id="app">
				<Referee />
			</div>
		</>
  	);
}

export default App
