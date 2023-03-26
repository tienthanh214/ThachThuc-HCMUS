import GameWrapper from "./GameWrapper";
import { genBinValue } from "../utils/random";

export default function BinToHex() {
    const MAX_CHAR_PLAY = 35;

	const onCheckCorrect = (binValue, userInputValue) => {
        return parseInt(binValue, 2) === parseInt(userInputValue, 10)
    }

	return <GameWrapper gameName={"Convert 4 bit below to hex"}
		genQuestion={() => genBinValue(0, 15)}
		checkCorrect={onCheckCorrect}
		numOfQuestion={MAX_CHAR_PLAY}
		answerLength={2}
	/>;
}