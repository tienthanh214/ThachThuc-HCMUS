import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import CharToBin from "./containers/CharToBit";
import HexToChar from "./containers/HexToChar";
import HomePage from "./containers/HomePage";
import BinToHex from "./containers/BinToHex";
import DecToHex from "./containers/DecToHex";

function App() {
	const listGame = [
		{name: 'Hex To Char', link: "/hex2char", component: HexToChar},
		{name: 'Char To 5 bit', link: "/char2bin", component: CharToBin},
		{name: '4 Bit To Hex', link: "/bin2hex", component: BinToHex},
		{name: 'Dec To Hex', link: "/dec2hex", component: DecToHex}

	]

	return (
		<div className="App">
			<div className="App-body">
				<Routes>
					<Route exact path='/' element={<HomePage listGame={listGame} />}/>
					{
						listGame.map(game => (
							<Route key={game.name} exact path={game.link} Component={game.component} />
						))
					}
				</Routes>
			</div>
		</div>
	);
}

export default App;
