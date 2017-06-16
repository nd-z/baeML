import React from 'react';
import ReactDOM from 'react-dom';
import {Link} from 'react-router-dom';
import createHistory from 'history/createBrowserHistory';
import FbSDK from './fbSDKLoader';
import './css/login.css';

// const history = createHistory()
class LoginComponent extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			loggedIn: false,
			name: ""
		}
		this.getLoginState = this.getLoginState.bind(this);
		this.statusChangeCallback = this.statusChangeCallback.bind(this);
		this.login = this.login.bind(this);
	}

	//loads the FB JS SDK
	componentDidMount() {
		// fade in the logo
		var logo = ReactDOM.findDOMNode(this.refs.logo);
		logo.style.opacity = 0;
		window.requestAnimationFrame(function() {
			logo.style.transition = "opacity 2500ms";
			logo.style.opacity = 1;
		});

		window.FB = FbSDK.loadFbSDK();

		//attaches these methods to window so they can be called by FB SDK
		window['getLoginState'] = this.getLoginState;
		window['statusChangeCallback'] = this.statusChangeCallback;
	}

	//calls the API to retrieve info about user, changes loggedIn
	//and message
	login() {
		window.FB.api('/me', (response) => {
			this.setState({
				loggedIn: true, 
				name: response.name
			});
			this.props.history.push('/feed');
		});
	}

	//query status of user, either prompts to login or proceeds
	statusChangeCallback(response){
		if (response.status === 'connected') {
			this.login(); 
		} else if (response.status === 'not_authorized') {
			console.log("login thru fb");
		} else {
			console.log("handle not being logged into fb");
		}
	}

	//calls FB API's getLoginStatus
	getLoginState() { 
		window.FB.getLoginStatus(function(response) {
			this.statusChangeCallback(response);
		});
	}

	//renders the landing page
	render () {
		if (this.state.loggedIn === true)
			this.props.history.push('/feed');
		return (<div className="headerbox">
				<img src={require('./imgs/logo.png')} ref="logo" alt={"logo"}/>
				<div className="text-center">
					<p>Knows you better than your SO</p>
					<p id="small">Login below to start getting recommendations</p>
					<div className="fb-login-button" 
						data-max-rows="1" 
						data-size="large" 
						data-button-type="login_with" 
						data-show-faces="false" 
						data-auto-logout-link="false" 
						data-use-continue-as="false"
						data-onlogin="getLoginState();">
					</div>
				</div>
			</div>)
	}
}

export default LoginComponent;