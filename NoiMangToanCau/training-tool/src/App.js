import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import CharToBin from "./containers/CharToBit";
import HexToChar from "./containers/HexToChar";

function App() {
	return (
		<div className="App">
			<div className="App-body">
				<Routes>
					{/* <Route exact path='/'/> */}
					<Route path="/hex2char" Component={HexToChar} />
					<Route path="/char2bin" Component={CharToBin} />
				</Routes>
			</div>
		</div>
	);
}

export default App;
