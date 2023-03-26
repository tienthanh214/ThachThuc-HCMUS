import { useEffect, useRef, useState } from "react";

export default function InputBox({handleEnter, length}) {
	const inputRef = useRef();
	const [value, setValue] = useState("");

    useEffect(() => {
        inputRef.current.focus()
    }, [])

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleEnter(value)
            setValue('')
        }
    }

	return (
		<input
            ref={inputRef}
			type="text"
			required={true}
			autoFocus
			maxLength={length}
			minLength={length}
			value={value}
			onChange={(e) => setValue(e.target.value)}
            onKeyDown={(e) => handleKeyDown(e)}
            style={{fontSize: 32, width: 128, textAlign: 'center'}}
		/>
	);
}
