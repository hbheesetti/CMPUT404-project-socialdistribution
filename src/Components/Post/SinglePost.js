import React, { useState, useEffect, useLayoutEffect } from "react";
import {
	Avatar,
	Panel,
	IconButton,
	Message,
	useToaster,
	Nav,
	Navbar,
} from "rsuite";
import ThumbsUpIcon from "@rsuite/icons/legacy/ThumbsUp";
import ShareIcon from "@rsuite/icons/legacy/Reply";
import COMMENTS from "./Comment";
import "./Post.css";
import ReactMarkdown from "react-markdown";
import LIKE from "./Like";
import EditIcon from "@rsuite/icons/Edit";
import TrashIcon from "@rsuite/icons/Trash";
import EDITPOSTMODAL from "../Modals/EditPostModal";
import LIKESMODAL from "../Modals/LikesModal";
import { getAuthorId } from "../utils/auth";
import { useNavigate, useParams } from "react-router-dom";
import { reqInstance } from "../utils/axios";
import PROFILEIMAGE from "../Profile/ProfileImage";
import { unsetCurrentUser } from "../utils/auth";
import ADD_FRIEND_MODAL from "../Modals/AddFriendModal";
import "./Post.css";
import { createReqInstance } from "../utils/axios";
// Component Imports

function SINGLEPOST({ explore }) {
	const [post, set_post] = useState({ author: { profileImage: "" }, id: "" });
	const [likes, setLikes] = useState({ items: [] });
	const [open, setOpen] = useState(false);
	const [addOpen, setAddOpen] = useState(false);
	const [curPage, setCurPage] = useState("singlePost");
	const toaster = useToaster();
	let navigate = useNavigate();
	let { author, post_id } = useParams();

	useLayoutEffect(() => {
		if (!localStorage.getItem("loggedIn")) {
			navigate("/signin");
		} else {
			let host = "";
			reqInstance({ method: "get", url: `authors/${author}` }).then(
				(res) => {
					if (res.status === 200) {
						console.log(res.data);
						host = res.data.host;
						let reqInstance = createReqInstance(host);
						let url = getUrl();
						reqInstance({ method: "get", url: url })
							.then((res) => {
								console.log(res);
								if (res.status == 200) {
									set_post(res.data);
								}
							})
							.catch((err) => {
								navigate("/");
								notifyFailedPost(
									"We couldnt find the post you were looking for or the post doesnt exist"
								);
							});
					}
				}
			);
		}
	}, []);

	const getUrl = (host) => {
		let url = `/posts/authors/${author}/posts/${post_id}`;
		if (host === "https://yoshi-connect.herokuapp.com/") {
			url = `authors/${author}/posts/${post_id}`;
		} else if (host === "https://social-distro.herokuapp.com/") {
			url = `api/authors/${author}/posts/${post_id}`;
		}
		return url;
	};

	const body = () => {
		if (post["contentType"] === "text/plain") {
			return <p style={{ padding: "5px" }}>{post["content"]}</p>;
		}

		if (post["contentType"] === "text/markdown") {
			return (
				<ReactMarkdown style={{ padding: "5px", height: "100px" }}>
					{post["content"]}
				</ReactMarkdown>
			);
		}

		// handle images
		if (
			post["contentType"] === "image/jpeg" ||
			post["contentType"] === "image/png"
		) {
			let tempAuthorId = (post.author.id + "").split("/").slice(-1);
			let tempPostId = (post.id + "").split("/").slice(-1);
			let HOST = "https://sociallydistributed.herokuapp.com/";
			let posturl =
				HOST +
				"posts/authors/" +
				tempAuthorId +
				"/posts/" +
				tempPostId +
				"/image";
			return (
				<p style={{ padding: "5px" }}>
					<img src={posturl} alt="image" />
				</p>
			);
		}
	};

	const handleOpen = () => {
		setOpen(true);
	};

	const handleModalClose = () => {
		setOpen(false);
	};

	const notifySuccessPost = () => {
		toaster.push(
			<Message type="success">Successful edited this post</Message>,
			{
				placement: "topEnd",
				duration: 5000,
			}
		);
	};

	const notifySuccessDeletePost = () => {
		toaster.push(
			<Message type="success">Successfully deleted this post</Message>,
			{
				placement: "topEnd",
				duration: 5000,
			}
		);
	};

	async function sharePost() {
		const author_id = getAuthorId(null);
		const origin_author_id = getAuthorId(post.author.id);
		const post_id = getAuthorId(post.id);
		const url = `posts/authors/${origin_author_id}/posts/${post_id}/share/${author_id}/`;
		reqInstance({ method: "post", url: url })
			.then((res) => {
				if (res.status === 200) {
					notifySuccessPost();
				} else {
					notifyFailedPost(res.data);
				}
			})
			.catch((err) => console.log(err));
	}

	const notifyFailedPost = (error) => {
		toaster.push(<Message type="error">{error}</Message>, {
			placement: "topEnd",
			duration: 5000,
		});
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

	const handleAddFriendOpen = () => {
		setAddOpen(true);
	};

	const handleAddFriendModalClose = () => {
		setAddOpen(false);
	};

	const handleInboxClick = () => {
		navigate("/");
	};

	async function handleDeletePost() {
		const author_id = getAuthorId(null);
		const post_id = getAuthorId(post.id);
		const url = `posts/authors/${author_id}/posts/${post_id}/`;
		reqInstance({ method: "delete", url: url })
			.then((res) => {
				if (res.status === 204) {
					notifySuccessDeletePost();
				} else {
					notifyFailedPost(res.data);
				}
			})
			.catch((err) => console.log(err));
	}

	const delEditBtn = (
		<div>
			<IconButton
				style={{ float: "right", marginRight: "10px" }}
				appearance="subtle"
				onClick={handleOpen}
				icon={<EditIcon />}
			/>
			<IconButton
				style={{ float: "right", marginRight: "10px" }}
				appearance="subtle"
				onClick={handleDeletePost}
				icon={<TrashIcon />}
			/>
		</div>
	);

	// need to make a get request to get the post obj and set post obj to that.

	const header = (
		<div
			style={{
				height: "50px",
				borderBottom: "0.5px solid grey",
			}}
		>
			<Avatar
				style={{ float: "left" }}
				circle
				src={post["author"]["profileImage"]}
				size="md"
			></Avatar>
			<div
				style={{
					marginLeft: "10px",
					float: "left",
				}}
			>
				{post["author"]["displayName"]}
			</div>
			<IconButton
				style={{ float: "right", marginRight: "10px" }}
				appearance="subtle"
				onClick={sharePost}
				icon={<ShareIcon />}
			/>
			<LIKE postObj={post} />
		</div>
	);

	const likesmodal = <LIKESMODAL postobj={post} />;

	return (
		<div style={{ padding: "10px", width: "60%", margin: "auto" }}>
			<Navbar>
				<Navbar.Brand>Socially Distrubted</Navbar.Brand>
				<Nav pullRight>
					<Nav.Item onClick={handleLogoutClick}>Logout</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Menu
						title="Inbox"
						onClick={handleInboxClick}
					></Nav.Menu>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleGithubClick}>Github</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleProfileClick}>Profile</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleExploreClick}>Explore</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleAddFriendOpen}>
						Add Friend
					</Nav.Item>
				</Nav>
			</Navbar>
			<Panel
				bordered
				header={header}
				style={{
					marginBottom: "5px",
					backgroundColor: post.is_github ? "#fffdf9" : "white",
				}}
			>
				<div style={{ height: "auto" }}>
					<div
						style={{
							marginLeft: "5px",
							fontFamily: "Times New Roman",
							fontWeight: "bold",
							fontSize: "20px",
						}}
					>
						{post["title"]}
					</div>
					<div
						style={{
							marginLeft: "5px",
							fontFamily: "Times New Roman",
							fontWeight: "bold",
							fontSize: "15px",
						}}
					>
						{post["description"]}
					</div>
					{body()}
				</div>
				<Panel bordered collapsible header="Comments">
					<COMMENTS postobj={post}></COMMENTS>
				</Panel>
			</Panel>
			<ADD_FRIEND_MODAL
				open={addOpen}
				handleClose={handleAddFriendModalClose}
			/>
		</div>
	);
}

export default SINGLEPOST;
