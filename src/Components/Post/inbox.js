import React, { useEffect, useState, useCallback } from "react";
// Component Imports
import POST from "./Post";
import CREATEPOST from "./CreatePost";
import LIKEINBOX from "./LikeInbox";
import { Navbar, Nav, Panel, useToaster, Message } from "rsuite";
import { useNavigate } from "react-router-dom";
import { reqInstance } from "../utils/axios";
import FOLLOWREQ from "./FollowReq";
import ADD_FRIEND_MODAL from "../Modals/AddFriendModal";
import { getAuthorId, getCsrfToken, unsetCurrentUser } from "../utils/auth";
import COMMENTINBOX from "./CommentInbox";

function INBOX() {
	const [inbox, setInbox] = useState({ items: [] });
	const [curPage, setCurPage] = useState("inbox");
	const [open, setOpen] = useState(false);
	const [state, setState] = useState({ count: 0 });
	let navigate = useNavigate();

	// Get the inbox items from the users inbox
	useEffect(() => {
		if (!localStorage.getItem("loggedIn")) {
			navigate("/signin");
		} else {
			const author_id = getAuthorId(null);
			const url = `authors/${author_id}/inbox`;
			reqInstance({ method: "get", url: url }).then((res) => {
				setInbox(res.data);
			});
		}
	}, []);

	const refreshInbox = useCallback(() => {
		setState(({ count }) => ({ count: count + 1 }));
	});

	const item = (obj) => {
		if (obj.type === "post") {
			return <POST key={obj.id} postobj={obj} explore={true} github={false} />;
		}
		if (obj.type === "Like") {
			return <LIKEINBOX key={obj.id} likeobj={obj} />;
		}
		if (obj.type === "Follow") {
			return <FOLLOWREQ key={obj.id} obj={obj} />;
		}
		if (obj.type === "comment") {
			return <COMMENTINBOX key={obj.id} obj={obj} />;
		}
	};

	const handleProfileClick = () => {
		if (curPage !== "profile") {
			setCurPage("profile");
			navigate("profile");
		}
	};

	const handleExploreClick = () => {
		if (curPage !== "explore") {
			setCurPage("explore");
			navigate("explore");
		}
	};

	const handleGithubClick = () => {
		if (curPage !== "github") {
			setCurPage("github");
			navigate("/github");
		}
	};

	async function handleLogoutClick() {
		reqInstance.post("dlogout/").then((res) => {
			if (res.status === 202) {
				unsetCurrentUser();
				navigate("/signin");
			}
		});
	}

	async function handleClearInboxClick() {
		const author_id = getAuthorId(null);
		const url = `authors/${author_id}/inbox/`;
		await reqInstance({ method: "delete", url: url }).then((res) => {
			if (res.status === 204) {
				setInbox({ items: [] });
			}
		});
	}

	const handleOpen = () => {
		setOpen(true);
	};

	const handleModalClose = () => {
		setOpen(false);
	};

	return (
		<div style={{ padding: "10px", width: "60%", margin: "auto" }}>
			<Navbar>
				<Navbar.Brand>Socially Distrubted</Navbar.Brand>
				<Nav pullRight>
					<Nav.Item onClick={handleLogoutClick}>Logout</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Menu title="Inbox">
						<Nav.Item
							style={{ color: "red" }}
							onClick={handleClearInboxClick}
						>
							Clear Inbox
						</Nav.Item>
					</Nav.Menu>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleGithubClick}>GitHub</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleProfileClick}>Profile</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleExploreClick}>Explore</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleOpen}>Add Friend</Nav.Item>
				</Nav>
			</Navbar>
			<Panel bordered header="New Post" collapsible>
				<CREATEPOST refresh={refreshInbox}></CREATEPOST>
			</Panel>
			{inbox.items && inbox.items.map((obj) => item(obj))}
			<ADD_FRIEND_MODAL open={open} handleClose={handleModalClose} />
		</div>
	);
}

export default INBOX;
