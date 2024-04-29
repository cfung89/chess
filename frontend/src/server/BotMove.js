import { BASE } from "../Constants";

export default function botMove() {
    async function fetchBotMove() {
        let obj;
        const res = await fetch(`${BASE}/botmove`);
        obj = await res.json();
        console.log(obj);
        return obj;
    }
    const move = fetchBotMove();
    return move;
}
