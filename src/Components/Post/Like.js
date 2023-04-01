import React, { useState, useEffect } from "react";
import { IconButton, useToaster, Message } from "rsuite";
import ThumbsUpIcon from "@rsuite/icons/legacy/ThumbsUp";
import { reqInstance } from "../utils/axios";
import { getAuthorId } from "../utils/auth";

// Component Imports
function LIKE({ postObj }) {
	// const [like, set_like] = useState(likeobj);
	const [new_like, set_new_like] = useState("");
	const toaster = useToaster();
	const postObjUrl = postObj.id;
	// const [users, setusers] = useState([]);
	//Confirm the name of the button
	const handleSubmitClick = () => {
		const FAID = getAuthorId(postObj.author["id"]);
		const author_id = getAuthorId(null);
		const host = postObj.author["host"]
		const user = JSON.parse(localStorage.getItem("user"));
		// const user = JSON.parse(localStorage.getItem("user"));
		const params = {
			type: "Like",
			author_id: user,
			object: postObjUrl,
		};
		const url = `authors/${FAID}/inbox/`;
		
		const reqInstance = createReqInstance(host); // Create axios instance with default base URL
  		reqInstance.post({url:url, baseurl:host, data:params})
    		.then((res) => {
      		toaster.push(
        		<Message type="success">Successful Like</Message>,
        		{
          			placement: 'topEnd',
          			duration: 5000
        		}
      		);
    	})
    	.catch((err) => {
      		toaster.push(
        		<Message type="error">{err}</Message>,
        		{
          			placement: 'topEnd',
          			duration: 5000
        		}
      		);
    	});
		//Confirm what to add into the params and send inbox
		// reqInstance({ method: "post", url: url, data: params })
		// 	.then((res) => {
		// 		toaster.push(
		// 			<Message type="success">Successful Like</Message>,
		// 			{
		// 				placement: "topEnd",
		// 				duration: 5000,
		// 			}
		// 		);
		// 	})
		// 	.catch((err) => {
		// 		toaster.push(<Message type="error">{err}</Message>, {
		// 			placement: "topEnd",
		// 			duration: 5000,
		// 		});
		// 	});
	};

	return (
		<IconButton
			style={{ float: "right", marginRight: "10px" }}
			appearance="subtle"
			icon={<ThumbsUpIcon />}
			onClick={handleSubmitClick}
		/>
	);
}

export default LIKE;
