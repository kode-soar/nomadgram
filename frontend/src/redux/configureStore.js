import { createStore, combineReducers, applyMiddleware } from "redux";
import users from "redux/modules/users";
import thunk from "redux-thunk";
import { connectRouter, routerMiddleware } from "connected-react-router";
import { createBrowserHistory } from "history";
import { i18nState } from "redux-i18n"
import { composeWithDevTools } from "redux-devtools-extension"

const history = createBrowserHistory();
const middlewares = [thunk, routerMiddleware(history)];
const env = process.env.NODE_ENV;

if (env === "development") {
	const { logger } = require("redux-logger");
	middlewares.push(logger);
}

const reducer = combineReducers({
	users,
	router: connectRouter(history),
	i18nState
});

let store;

if (env === "development") {
	store = (initialState) => createStore(reducer, composeWithDevTools(applyMiddleware(...middlewares)));
} else {
	store = (initialState) => createStore(reducer, applyMiddleware(...middlewares));
	// 함수(...middlewares) : array를 (a, b, c) 형태로 반환(unpack)해서 멀티 파라미터로 입력
	// middlewares -> [thunk]
	// ...middlewares -> thunk
}
// dev면 리액토트론에 스토어 생성
// prod이면 리덕스에 스토어 생성

export { history };

export default store();



