import { BASE } from "../Constants";

export default function getMoves() {
    async function fetchMoves() {
        let obj;
        const res = await fetch(`${BASE}/legalmoves`);
        obj = await res.json();
        //console.log(obj);
        return obj;
    }

    return fetchMoves()
}