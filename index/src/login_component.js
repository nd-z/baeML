import React from 'react';
import './css/login.css';

function LoginButton(props){
	return(
		<button onClick={props.onClick} className="fbButton">Continue with Facebook</button>
		)
}

function Logo(props) { 
	return (<div>
			{!props.loggedIn ? 
			<div className="headerbox">
				<img src={require('./imgs/logo.png')} alt={"logo"}/>
				<div className="text-center">
					<p>Knows you better than your SO</p>
					<p id="small">Login below to start getting recommendations</p>
					<LoginButton onClick={props.onLogin}/>
				</div>
			</div> : 
			<p>Loading your feed...</p>}
			</div>)
}

class LoginComponent extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			loggedIn: true,
		}
		this.login = this.login.bind(this);
		this.getLoginState = this.getLoginState.bind(this);
		this.statusChangeCallback = this.statusChangeCallback.bind(this);
	}

	//query status of user, either prompts to login or proceeds
	statusChangeCallback(response){
		if (response.status === 'connected') {
			this.props.history.push('/feed');
		} else {
			this.setState({loggedIn: false});
		}
	}

	login() {
		window.FB.login((response) => {
			if (response.status === 'connected'){
				this.props.history.push('/feed');
			}
		}, {scope: 'public_profile,email'});
	}

	//calls FB API's getLoginStatus
	getLoginState() { 
		console.log(window.FB)
		window.FB.getLoginStatus(function(response) {
			window.statusChangeCallback(response);
		});
	}

	componentDidMount() {
		//attaches these methods to window so they can be called by FB SDK
		window['getLoginState'] = this.getLoginState;
		window['statusChangeCallback'] = this.statusChangeCallback;

		window.fbAsyncInit = function() {
               window.FB.init({
                appId            : '1992517710981460',
                autoLogAppEvents : true,
                xfbml            : true,
                cookie           : true,
                status     		 : true,
                version          : 'v2.9'
              });
              window.FB.AppEvents.logPageView();
              this.getLoginState();
            };
            (function(d, s, id) {
              var js, fjs = d.getElementsByTagName(s)[0];
              if (d.getElementById(id)) return;
              js = d.createElement(s); js.id = id;
              js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.9&appId=1992517710981460";
              fjs.parentNode.insertBefore(js, fjs);
            }(document, 'script', 'facebook-jssdk'));
	}

	//renders the landing page
	render () {
		return (
			<Logo loggedIn={this.state.loggedIn} onLogin={this.login}/>
		)
	}
}

export default LoginComponent;