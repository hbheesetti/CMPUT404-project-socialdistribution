import React, { useState, useEffect, useLayoutEffect } from "react";
import { Input, InputGroup } from "rsuite";
import { createReqInstance } from "../utils/axios";
import { getAuthorId, getCsrfToken } from "../utils/auth";
// Component Imports
import COMMENTLIKE from "./LikeComment";
import axios from "axios";

// This component handles posting and displaying comments on a post
function COMMENTS({ postobj }) {
	const [commentObj, setCommentObj] = useState([]);
	const [postObj, setPostObj] = useState(postobj);
	const [new_comment, set_new_comment] = useState("");

	async function getComments(url) {
		var base64 = require("base-64");
		var username = localStorage.getItem("username");
		var password = localStorage.getItem("password");
		var busername = base64.encode(username);
		var bpassword = base64.encode(password);
		let reqInstance = axios.create({
			headers: {
				Authorization: { username: busername, password: bpassword },
			},
			auth: {
				username: username,
				password: password,
			},
		});
		return reqInstance({
			method: "get",
			url: url,
		})
			.then((res) => {
				if (res.data.comments) {
					setCommentObj(res.data.comments);
				} else if (res.data.results) {
					setCommentObj(res.data.results);
				}
			})
			.catch((err) => console.log(err));
	}

	useEffect(() => {
		if (postobj.type === "post") {
			getComments(postObj.source + "/comments");
		}
	}, []);

	const handleSubmitClick = () => {
		const user = JSON.parse(localStorage.getItem("user"));
		delete user["type"];
		const FAID = getAuthorId(postObj.author.id);
		const params = {
			type: "comment",
			comment: new_comment,
			author: user,
			object: postObj.source,
			contentType: "text/markdown",
		};
		const url = `authors/${FAID}/inbox/`;
		const reqInstance = createReqInstance(postObj.author.host);
		return reqInstance({
			method: "post",
			url: url,
			data: params,
		})
			.then(async (res) => {
				getComments(postObj.source + "/comments");
				set_new_comment("");
			})
			.catch((err) => console.log(err));
	};

	return (
		<div>
			{commentObj.map((obj) => (
				<div
					key={obj.id}
					style={{
						width: "100%",
						border: "0.5px solid lightgrey",
						padding: "2px",
						marginBottom: "2px",
					}}
				>
					{/* <text>{obj.id}</text> */}
					<text
						style={{
							marginLeft: "10px",
							fontWeight: "bold",
						}}
					>
						{obj["author"]["displayName"]}
					</text>
					<text>: {obj["comment"]}</text>
					<COMMENTLIKE obj={obj.id} />
				</div>
			))}

			<InputGroup inside style={{ marginTop: "5px" }}>
				<Input
					onChange={(e) => set_new_comment(e)}
					value={new_comment}
					placeholder="comment"
				/>
				<InputGroup.Button onClick={handleSubmitClick}>
					Submit
				</InputGroup.Button>
			</InputGroup>
		</div>
	);
}

export default COMMENTS;
