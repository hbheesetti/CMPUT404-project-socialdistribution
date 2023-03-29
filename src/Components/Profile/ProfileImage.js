import React, { useEffect, useState } from "react";
import { Avatar } from "rsuite";
import { getProfileImageUrl } from "../utils/auth";

function PROFILEIMAGE({ size }) {
	const [url, setUrl] = useState("");

	useEffect(() => {
		if (getProfileImageUrl() === "") {
			setUrl("https://i.imgur.com/J95WCOD.jpg");
		}
	}, []);

	return (
		<Avatar style={{ float: "left" }} circle src={url} size={size}></Avatar>
	);
}

export default PROFILEIMAGE;
