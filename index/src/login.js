import React from 'react';
import ReactDOM from 'react-dom';
import './css/login.css';

class LoginComponent extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			loggedIn: true,
		}
		this.getLoginState = this.getLoginState.bind(this);
		this.statusChangeCallback = this.statusChangeCallback.bind(this);
	}

	//query status of user, either prompts to login or proceeds
	statusChangeCallback = (response) =>{
		if (response.status === 'connected') {
			this.props.history.push('/feed');
		} else { 
			console.log("uhh")
			this.setState({
				loggedIn: false, 
			});
		}
	}

	//calls FB API's getLoginStatus
	getLoginState() { 
		window.FB.getLoginStatus((response) => {
			this.statusChangeCallback(response);
		});
	}

	componentWillMount() {
		//attaches these methods to window so they can be called by FB SDK
		window['getLoginState'] = this.getLoginState;
		window['statusChangeCallback'] = this.statusChangeCallback;

		window.fbAsyncInit = () => {
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

	componentDidMount() {
        // fade in the logo
		var logo = ReactDOM.findDOMNode(this.refs.logo);
		logo.style.opacity = 0;
		window.requestAnimationFrame(function() {
			logo.style.transition = "opacity 2500ms";
			logo.style.opacity = 1;
		});
	}

	//renders the landing page
	render () {
		var fbButton = (<div className="fb-login-button" data-max-rows="1" data-size="large" data-button-type="login_with" data-show-faces="false" data-auto-logout-link="false" data-use-continue-as="false"data-onlogin="getLoginState();"></div>)
		console.log(this.state.loggedIn);
		return (<div className="headerbox">
				<img src={require('./imgs/logo.png')} ref="logo" alt={"logo"}/>
				<div className="text-center">
					<p>Knows you better than your SO</p>
					<p id="small">Login below to start getting recommendations</p>
					{fbButton}
				</div>
			</div>)
	}
}

export default LoginComponent;