import React from 'react';

const FB = window.FB
class LoginComponent extends React.Component {
	
	constructor(props) {
		super(props);
		this.state = {
			loggedIn: false,
			name: ""
		}
	}

	componentDidMount() {
		window.fbAsyncInit = function() {
	      FB.init({
	        appId            : '1992517710981460',
	        autoLogAppEvents : true,
	        xfbml            : true,
	        version          : 'v2.9'
	      });
	      FB.AppEvents.logPageView();
	    };

	(function(d, s, id) {
	  var js, fjs = d.getElementsByTagName(s)[0];
	  if (d.getElementById(id)) return;
	  js = d.createElement(s); js.id = id;
	  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.9&appId=1992517710981460";
	  fjs.parentNode.insertBefore(js, fjs);
	}(document, 'script', 'facebook-jssdk'));
	}

	login() {
		console.log("success");
		// FB.api('/me', function(response) {
		// 	this.setState((response.name) => {
		// 		return {loggedIn: true, name: response.name};
		// 	});
		// });
	}

	statusChangeCallback(response){
		if (response.status === 'connected') {
			console.log("bring to login page");
			this.login(); 
		} else if (response.status === 'not_authorized') {
			console.log("login thru fb");
		} else {
			console.log("handle not being logged into fb");
		}
	}

	getLoginState() { 
		FB.getLoginStatus(function(response) {
			this.statusChangeCallback(response);
		});
	}

	render () {
		var greeting;
		if (this.state.loggedIn)
			greeting = "Hello there, " + this.state.name;
		else
			greeting = "You are not logged in";

		return (<div><p>{greeting}</p><div className="fb-login-button" 
			data-max-rows="1" 
			data-size="large" 
			data-button-type="login_with" 
			data-show-faces="false" 
			data-auto-logout-link="false" 
			data-use-continue-as="false"
			data-onlogin="getLoginState();">
			</div></div>)
	}
}

export default LoginComponent;