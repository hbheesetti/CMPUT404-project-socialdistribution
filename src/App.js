import { BrowserRouter, Routes, Route } from "react-router-dom";
import SIGN_IN from "./Components/SignIn/Sign_in";
import INBOX from "./Components/Post/inbox";
import PROFILE from "./Components/Profile/Profile";
import EXPLORE from "./Components/Explore/Explore";
import SINGLEPOST from "./Components/Post/SinglePost";
import GITHUB from "./Components/Explore/github";

function App() {
	return (
		<div className="App">
			<BrowserRouter>
				<Routes>
					<Route path="/signin" exact element={<SIGN_IN />} />
					<Route path="/" exact element={<INBOX />} />
					<Route path="/profile" exact element={<PROFILE />} />
					<Route path="/explore" exact element={<EXPLORE />} />
					<Route
						path="/author/:author/post/:post_id"
						exact
						element={<SINGLEPOST />}
					/>
					<Route path="github" exact element={<GITHUB />} />
				</Routes>
			</BrowserRouter>
		</div>
	);
}

export default App;
