import GameWrapper from "./GameWrapper";
import { getRandomInt } from "../utils/random";

export default function DecToHex() {
    const MAX_CHAR_PLAY = 30;

	const onCheckCorrect = (decValue, userInputValue) => {
        return parseInt(userInputValue, 16) === decValue
    }

	return <GameWrapper gameName={"Convert decimal below to hex"}
		genQuestion={() => getRandomInt(0, 255)}
		checkCorrect={onCheckCorrect}
		numOfQuestion={MAX_CHAR_PLAY}
		answerLength={3}
	/>;
}