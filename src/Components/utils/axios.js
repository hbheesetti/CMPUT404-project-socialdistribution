import axios from "axios";
import { getCsrfToken } from "./auth";

var base64 = require("base-64");

var username = localStorage.getItem("username");
var password = localStorage.getItem("password");
getCsrfToken();
var token = localStorage.getItem("token");
// default axios for our server with username andpassword setup
export let reqInstance = axios.create({
	baseURL: `${process.env.REACT_APP_HOST_NAME}/`,
	auth: {
		username: username,
		password: password,
	},
});

// axios without auth setup
export let axiosInstance = axios.create({
	headers: {
		"X-CSRFToken": token,
	},
	auth: {
		username: username,
		password: password,
	},
});

// axios for all the other servers
export let createReqInstance = (baseUrl) => {
	let username, password;
	switch (baseUrl) {
		case process.env.REACT_APP_HOST_NAME + "/":
			username = localStorage.getItem("username");
			password = localStorage.getItem("password");
			return axios.create({
				headers: {
					"X-CSRFToken": token,
				},
				baseURL: baseUrl,
				auth: {
					username: username,
					password: password,
				},
			});
		case "https://sociallydistributed.herokuapp.com/":
			username = "app2team15";
			password = "hari1234";
			return axios.create({
				headers: {
					"X-CSRFToken": token,
				},
				baseURL: baseUrl,
				auth: {
					username: username,
					password: password,
				},
			});
		case "https://ineedsleep.herokuapp.com/":
			username = "app1team15";
			password = "hari1234";
			return axios.create({
				headers: {
					"X-CSRFToken": token,
				},
				baseURL: baseUrl,
				auth: {
					username: username,
					password: password,
				},
			});
		default:
			throw new Error(`Invalid base URL: ${baseUrl}`);
	}
};
