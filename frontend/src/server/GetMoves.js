import { BASE } from "../Constants";

export default function getMoves() {
    //Sends a GET request to the server. This function is not used.
    async function fetchMoves() {
        let obj;
        const res = await fetch(`${BASE}/legalmoves`);
        obj = await res.json();
        //console.log(obj);
        return obj;
    }

    return fetchMoves()
}