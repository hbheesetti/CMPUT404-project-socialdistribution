import React, { useState } from "react";
import {
	Avatar,
	Button,
	Modal,
	Input,
	InputGroup,
	useToaster,
	Message,
} from "rsuite";
import { ToastContainer, toast } from "react-toastify";
import SearchIcon from "@rsuite/icons/Search";
import { reqInstance, createReqInstance } from "../utils/axios";
import { getAuthorId, getCurrentUser } from "../utils/auth";

function ADD_FRIEND_MODAL({ open, handleClose }) {
	const [displayName, setName] = useState("");
	const [foreign_author, setForeign] = useState({});
	const [users, setusers] = useState([]);
	const toaster = useToaster();

	async function sendreq(obj) {
		const AUTHOR_ID = getAuthorId(null);
		const url2 = obj.id + "/inbox";
		const user = JSON.parse(localStorage.getItem("user"));
		const axiosInstance = createReqInstance(obj.host);
		user["id"] = AUTHOR_ID;
		delete user["type"];
		const params = {
			type: "Follow",
			actor: user,
			object: obj,
			summary: "A Follow Request",
		};
		return axiosInstance({ method: "post", url: url2, data: params })
			.then((res) => {
				toaster.push(
					<Message type="success">Friend Request Sent</Message>,
					{
						placement: "topEnd",
						duration: 5000,
					}
				);
				handleClose();
			})
			.catch((err) => {
				if (err.status == 400) {
					toaster.push(<Message type="error">{err}</Message>, {
						placement: "topEnd",
						duration: 5000,
					});
				} else if (err.status == 404) {
					toaster.push(<Message type="error">{err}</Message>, {
						placement: "topEnd",
						duration: 5000,
					});
				}
			});
	}
	// This function gets the author info and sends the friend req to the author
	async function handleAddFriendClick() {
		// url = authors/authors/${AUTHOR_ID}/followers/${foreign_author_id}/;
		// reqInstance({ method: "put", url: url });
		const url = `authors/displayName/${displayName}/`;
		await reqInstance({ method: "get", url: url }).then(async (res) => {
			setusers(res.data);
		});
	}

	const item = (obj) => {
		return (
			<div
				key={obj.id}
				style={{
					height: "50px",
					border: "0.5px solid lightgrey",
					borderRadius: "10px",
					marginTop: "5px",
				}}
			>
				<div style={{ padding: "5px" }}>
					<Avatar
						style={{ float: "left", marginBotton: "5px" }}
						circle
						src={obj["profileImage"]} //{follow[actor][profileImage]} replace this with the actors profile image url
					/>
					<h5
						style={{
							marginLeft: "10px",
							float: "left",
						}}
					>
						{obj["displayName"]} {" ("}
						{obj["host"]} {") "}
					</h5>
				</div>
				<div>
					<Button
						style={{ float: "right", marginRight: "10px" }}
						appearance="primary"
						onClick={() => sendreq(obj)}
					>
						Follow
					</Button>
				</div>
			</div>
		);
	};

	return (
		<Modal open={open} onClose={handleClose}>
			<Modal.Header>
				<h3>Add Friend</h3>
			</Modal.Header>
			<Modal.Body>
				<InputGroup>
					<Input
						placeholder={"display name"}
						value={displayName}
						onChange={(e) => setName(e)}
					/>
					<Button onClick={handleAddFriendClick}>Search</Button>
				</InputGroup>
				{users.map((obj) => item(obj))}
			</Modal.Body>
			<Modal.Footer>
				<Button onClick={handleClose} appearance="primary">
					Close
				</Button>
			</Modal.Footer>
		</Modal>
	);
}

export default ADD_FRIEND_MODAL;
