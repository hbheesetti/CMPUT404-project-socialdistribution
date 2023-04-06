import React, { useState } from "react";
import { Button, Avatar, Panel, useToaster, Message } from "rsuite";
import { reqInstance } from "../utils/axios";
import { getAuthorId } from "../utils/auth";
import PROFILEIMAGE from "../Profile/ProfileImage";

function FOLLOWREQ({ obj }) {
	const [follow, setFollow] = useState(obj);
	const toaster = useToaster();
	const [accepted, setAccepted] = useState(false);

	async function acceptFriend() {
		const curr_author_id = getAuthorId(null);
		var FAID = getAuthorId(obj.actor.id);
		const url2 = obj;

		const params = { accepted: accepted };
		const url = `authors/${curr_author_id}/followers/${FAID}/`;

		return reqInstance({ method: "put", url: url, data: params })
			.then((res) => {
				deleteFollow();
				toaster.push(
					<Message type="success">
						{res.data.displayName} now follows you
					</Message>,
					{
						placement: "topEnd",
						duration: 5000,
					}
				);
			})
			.catch((err) => {
				toaster.push(<Message type="error">{err}</Message>, {
					placement: "topEnd",
					duration: 5000,
				});
			});
	}

	async function deleteFollow() {
		const curr_author_id = getAuthorId(null);
		var FAID = getAuthorId(obj.actor.id);
		const url2 = obj;

		const params = { actor_id: FAID };
		const url = `authors/${curr_author_id}/sendreq/`;
		return reqInstance({ method: "delete", url: url, data: params })
			.then((res) => { 
			})
			.catch((err) => {
				toaster.push(<Message type="error">{err}</Message>, {
					placement: "topEnd",
					duration: 5000,
				});
			});
	}

	const getUrl = () => {
		if (follow["actor"]["profileImage"] === "") {
			return "https://i.imgur.com/J95WCOD.jpg";
		} else {
			return follow["actor"]["profileImage"];
		}
	};

	return (
		<Panel
			bordered
			style={{
				marginBottom: "5px",
			}}
		>
			<div>
				<Avatar
					style={{ float: "left", marginBotton: "5px" }}
					circle
					src={getUrl()} //{follow[actor][profileImage]} replace this with the actors profile image url
				/>
				<div
					style={{
						marginLeft: "50px",
						fontFamily: "Times New Roman",
						fontWeight: "bold",
						fontSize: "20px",
					}}
				>
					{follow["summary"]}
				</div>
			</div>

			<div style={{ marginTop: "10px" }}>
				<Button block onClick={acceptFriend} appearance="primary">
					Accept
				</Button>
				<Button block onClick={deleteFollow}>
					Deny
				</Button>
			</div>
		</Panel>
	);
}

export default FOLLOWREQ;
