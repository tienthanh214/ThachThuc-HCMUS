import { useEffect, useState } from "react";
import InputBox from "../components/InputBox";
import { genHexValue } from "../utils/random";
import "./HexToCharContainer.css";

export default function HexToCharContainer() {
	const MAX_CHAR_PLAY = 3;
	const [hexValue, setHexValue] = useState("Press Enter to start");
	const [point, setPoint] = useState(0);
	const [total, setTotal] = useState(0);
	const [isGameOver, setIsGameOver] = useState(false);

	const [result, setResult] = useState([]);
	const [startTime, setStartTime] = useState(0);
	const [wrongAnswer, setWrongAnswer] = useState([]);
	const [message, setMessage] = useState("");

	const onHandleCompare = (userInputValue) => {
		if (total > 1 && userInputValue === "") return;
		const newHex = genHexValue(32, 126);
		if (total === 0) {
			setMessage('')
			setWrongAnswer([])
			setStartTime(new Date());
			setTotal(1);
			setHexValue(newHex);
			return;
		}
		const isCorrect =
			hexValue === userInputValue.charCodeAt(0).toString(16).toUpperCase();
		const newPoint = point + isCorrect;

		if (!isGameOver) {
			setPoint(newPoint);
			if (!isCorrect) {
				const newWrongAnswer = [
					...wrongAnswer,
					{
						ans: hexValue,
						your: userInputValue,
					},
				];
				setWrongAnswer(newWrongAnswer);
			}
		}
		if (total >= MAX_CHAR_PLAY) {
			setMessage(`Your score: ${newPoint}/${total}`);
			setHexValue("Press Enter to continue");
			const currentGameOver = isGameOver;
			setIsGameOver((isGameOver) => !isGameOver);
			if (currentGameOver) {
				return
			}
				
		} else {
			setHexValue(newHex);
			setTotal((total) => total + 1);
		}
	};

	const appendResult = (curPoint) => {
		const curTime = new Date();
		const elapsedTime = ((curTime - startTime) / 1000).toFixed(1);
		setResult([...result, { point: curPoint, elapsedTime }]);
	};

	const resetGame = () => {
		setPoint(0);
		setTotal(0);
		setIsGameOver(false);
	};

	useEffect(() => {
		if (isGameOver) {
			appendResult(point);
			resetGame();
		}
	}, [isGameOver]);

	return (
		<div className="container">
			<div className="info-area">
				<h3 style={{ color: "green" }}>
					<span style={{ color: "black" }}>Score:</span>
					{point} / {Math.max(total - 1, 0)}
				</h3>
			</div>
			<div className="play-area">
				<h2>Convert HEX below to ASCII </h2>
				<h3 style={{ fontSize: 40, color: "blue" }}>{hexValue}</h3>
				<InputBox handleEnter={onHandleCompare} />
			</div>
			<div className="last-result">{message ? (
				<>
				<h3>
					{message}
				</h3>
				<div className="wrong-list">
					{
						wrongAnswer.map((res, id) => (
							<p key={id} style={{fontSize: 18}}>{id + 1}. <span style={{color: 'green', fontWeight: 'bold'}}>{res.ans}</span> → <span style={{color: 'red'}}>{res.your}</span> </p>
						))
					}
				</div>
				</>

			) : null}</div>
			<div className="result-box">
				{result.map((res, id) => (
					<div key={id} className="result-item">
						<p>
							{" "}
							<b>
								{id + 1}. {res.point} - {res.elapsedTime}s{" "}
							</b>
						</p>
					</div>
				))}
			</div>
		</div>
	);
}
