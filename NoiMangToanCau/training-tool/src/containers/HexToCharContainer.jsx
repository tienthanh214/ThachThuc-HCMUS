import { genHexValue } from "../utils/random";
import GameWrapper from "./GameWrapper";

export default function HexToCharContainer() {
	const MAX_CHAR_PLAY = 35;

	const onCheckCorrect = (hexValue, userInputValue) => {
		return hexValue === userInputValue.charCodeAt(0).toString(16).toUpperCase();
	}

	return <GameWrapper gameName={"Convert HEX below to ASCII"}
		genQuestion={() => genHexValue(32, 126)}
		checkCorrect={onCheckCorrect}
		numOfQuestion={MAX_CHAR_PLAY}
		answerLength={1}
	/>;
}
