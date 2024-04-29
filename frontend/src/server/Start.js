const BASE = "http://127.0.0.1:5000/";

export default function start() {
    const fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

    fetch(`${BASE}/create`, {
        method: "POST",
        body: JSON.stringify({fen: fen}),
        headers: {"Content-type": "application/json"}
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log(error));
}