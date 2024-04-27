import './Display.css';
import Chessboard from '../Chessboard/Chessboard';

export default function Display({fen}) {
	return (
		<>	
            <p className='text username'>Player 2</p>
            <Chessboard fen={fen} />
            <p className='text username'>Player 1</p>
		</>
			//<div className='text infobox'>test</div>
  	);
}
