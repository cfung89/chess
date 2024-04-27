import "./Tile.css";

export default function Tile({coords, image}) {
    if(coords % 2 === 0) {
        return (
            <div className="tile black-tile">
                {image && <div style={{backgroundImage: `url(${image})`}} className="chess-piece"></div>}
            </div>
        );
    } else {
        return (
            <div className="tile white-tile">
                {image && <div style={{backgroundImage: `url(${image})`}} className="chess-piece"></div>}
            </div>
        );
    }
}