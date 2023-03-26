import { genCharValue } from "../utils/random";
import GameWrapper from "./GameWrapper";

export default function CharToBin() {
	const MAX_CHAR_PLAY = 32;

	const onCheckCorrect = (charValue, userInputValue) => {
        return parseInt(userInputValue, 2) + 32 === charValue.charCodeAt(0)
    }

	return <GameWrapper gameName={"Convert char below to 5 bit"}
		genQuestion={() => genCharValue(32, 63)}
		checkCorrect={onCheckCorrect}
		numOfQuestion={MAX_CHAR_PLAY}
		answerLength={5}
	/>;
}
