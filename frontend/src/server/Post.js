import { HORIZONTAL_AXIS, BASE } from "../Constants";

export default function postMove(original, destination) {
    //Makes a POST request to the server and sends as message the move of the user.
    const move = `${HORIZONTAL_AXIS[original.x]}${original.y+1}${HORIZONTAL_AXIS[destination.x]}${destination.y+1}`;

    fetch(`${BASE}/move`, {
        method: "POST",
        body: JSON.stringify({move: move}),
        headers: {"Content-type": "application/json"}
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log(error));
}