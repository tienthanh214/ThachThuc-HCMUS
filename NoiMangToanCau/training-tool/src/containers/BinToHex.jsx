import GameWrapper from "./GameWrapper";
import { genBinValue } from "../utils/random";

export default function BinToHex() {
    const MAX_CHAR_PLAY = 35;

	const onCheckCorrect = (binValue, userInputValue) => {
		let bin = parseInt(binValue, 2);
		if (bin < 10)
        	return bin === parseInt(userInputValue, 10);
		
		userInputValue = userInputValue.toUpperCase();
		return userInputValue.length < 2 && userInputValue.charCodeAt(0) - ("A").charCodeAt(0) + 10 === bin;
    }

	return <GameWrapper gameName={"Convert 4 bit below to hex"}
		genQuestion={() => genBinValue(0, 15)}
		checkCorrect={onCheckCorrect}
		numOfQuestion={MAX_CHAR_PLAY}
		answerLength={2}
	/>;
}