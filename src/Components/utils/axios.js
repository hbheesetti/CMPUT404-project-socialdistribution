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
		Authorization: { username: busername, password: bpassword },
	},
	baseURL: `https://sociallydistributed.herokuapp.com/`,
	auth: {
		username: username,
		password: password,
	},
});
