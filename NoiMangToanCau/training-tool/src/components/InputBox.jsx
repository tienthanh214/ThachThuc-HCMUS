import { useEffect, useRef, useState } from "react";

export default function InputBox({handleEnter}) {
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
			required
			autoFocus
			maxLength={1}
			minLength={1}
			value={value}
			onChange={(e) => setValue(e.target.value)}
            onKeyDown={(e) => handleKeyDown(e)}
            style={{fontSize: 32, width: 128, textAlign: 'center'}}
		/>
	);
}
