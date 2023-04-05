import axios from "axios";
import { getCsrfToken } from "./auth";

var base64 = require("base-64");

var username = localStorage.getItem("username");
var password = localStorage.getItem("password");
getCsrfToken();
var token = localStorage.getItem("token");
var busername = base64.encode(username);
var bpassword = base64.encode(password);

export let reqInstance = axios.create({
	headers: {
		"X-CSRFToken": token,
	},
	baseURL: `${process.env.REACT_APP_HOST_NAME}/`,
	auth: {
		username: username,
		password: password,
	},
});

export let axiosInstance = axios.create({
	headers: {
		"X-CSRFToken": token,
	},
	auth: {
		username: username,
		password: password,
	},
});

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
		case process.env.REACT_APP_HOST_NAME + "//":
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
		case "https://killme.herokuapp.com//":
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
