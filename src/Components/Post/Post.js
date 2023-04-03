import React, { useState, useEffect, useLayoutEffect } from "react";
import { Avatar, Panel, IconButton, Message, useToaster, Button } from "rsuite";
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
import { useNavigate } from "react-router-dom";
import { reqInstance } from "../utils/axios";
import PROFILEIMAGE from "../Profile/ProfileImage";
import CopyIcon from "@rsuite/icons/Copy";
// Component Imports

function POST({ postobj, edit, explore, github }) {
	const [post, set_post] = useState(postobj);
	const [likes, setLikes] = useState({ items: [] });
	const [open, setOpen] = useState(false);
	const toaster = useToaster();
	let navigate = useNavigate();

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
			let imageurl = postobj.origin + 'image';
			return (
				<p style={{ padding: "5px" }}>
					<img src={imageurl} alt="image" />
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
		const origin_author_id = getAuthorId(postobj.author.id);
		const post_id = getAuthorId(postobj.id);
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

	const handleUrlClick = () => {
		const postid = getAuthorId(post["id"]);
		const authorid = getAuthorId(post["author"]["id"]);
		const host = process.env.REACT_APP_HOST_NAME + `/`;
		var path = `author/${authorid}/post/${postid}`;
		var url = host + path;
		navigator.clipboard.writeText(url);
	};

	async function handleDeletePost() {
		const author_id = getAuthorId(null);
		const post_id = getAuthorId(postobj.id);
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
			<IconButton
				style={{ float: "right", marginRight: "10px" }}
				appearance="subtle"
				onClick={handleUrlClick}
				icon={<CopyIcon />}
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
			{!github ?
				<IconButton
					style={{ float: "right", marginRight: "10px" }}
					appearance="subtle"
					onClick={sharePost}
					icon={<ShareIcon />}
				/> : <div />}
			{!github ? <LIKE postObj={postobj} /> : <div />}

			{edit ? delEditBtn : <div />}
		</div>

	);

	return (
		<div>
			<Panel
				bordered
				header={header}
				style={{
					marginBottom: "5px",
					backgroundColor: postobj.is_github ? "#fffdf9" : "white",
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
				<div>
					{explore ? <LIKESMODAL style={{ float: "right", marginRight: "10px" }} postobj={postobj} /> : <div />}
				</div>
				{!github ?
					< Panel bordered collapsible header="Comments">
						<COMMENTS postobj={postobj}></COMMENTS>
					</Panel>
					: <div />}
			</Panel>
			{
				!github ?
					<EDITPOSTMODAL
						open={open}
						obj={postobj}
						handleClose={handleModalClose}
					/> : <div />
			}
		</div >
	);
}

export default POST;
