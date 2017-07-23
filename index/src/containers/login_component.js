import React from 'react';
import axios from 'axios';
import '../css/login.css';
import '../css/index.css'

//fb login button
function LoginButton(props){
	return(
		props.isDisabled ? <p id="small">This may take a few minutes, you will be automatically redirected.</p> :
		<button onClick={props.onClick} className="fbButton">Continue with Facebook</button>
		)
}

//displays the logo
function Logo(props) { 
	return (<div className="headerbox"> 
				<img src={require('../imgs/logo.png')} alt={"logo"}/>
				<div className="text-center">
					<p>Knows you better than your SO</p>
					<p id="small">{props.textDisplay}</p>
					<LoginButton onClick={props.onLogin} isDisabled={props.isDisabled}/>
				</div>
			</div>)
}

class LoginComponent extends React.Component {
	previousLocation = this.props.location
	constructor(props) {
		super(props);
		this.state = {
			loggedIn: true,
			isDisabled: false,
			textDisplay: "Login below to start getting recommendations"
		}
		this.login = this.login.bind(this);
		this.displayError = this.displayError.bind(this);
		this.getLoginState = this.getLoginState.bind(this);
		this.statusChangeCallback = this.statusChangeCallback.bind(this);
	}

	//query status of user, either prompts to login or proceeds
	statusChangeCallback(response){
		if (response.status === 'connected') {
            this.setState({loggedIn: true});
			this.props.history.push('/feed');
		} else {
			this.setState({loggedIn: false});
		}
	}

	//handles logging into FB 
	login() {
		window.FB.login((response) => {
			if (response.status === 'connected'){
				console.log("should disable")
				this.setState({
					isDisabled: true,
					textDisplay: "Setting up your feed..."
				})
				var userID = response.authResponse.userID
				var accessToken = response.authResponse.accessToken
				console.log(userID)
				console.log(accessToken)
				/**log user into our server**/
				axios.get('http://localhost:3333/api/login/', {
					params: {
						user_ID: userID,
					}
				})
				.then((response) => { 
					if (response.status === 200) { //returning user
		        		console.log('contacted server');
		        		this.props.history.push('/feed', response.data); 
		        	} else if (response.status === 204) {
		        		console.log('new user');
		        		axios.post('http://localhost:3333/api/init/', {
							user_ID: userID,
							token: accessToken,
							size: Math.round(window.screen.width*.37)
						})
						.then((response) => {
							console.log("hi")
							this.props.history.push('/feed', response.data);
						})
		        	}
		    	})
				.catch((error) => {
					this.displayError();
				});
			
		}
		}, {scope: 'public_profile,user_likes'});
	}

	displayError(){
		this.setState({
			isDisabled: false,
			textDisplay: "An error occurred in retrieving your feed, please try again later."
		})
	}

	// }
	//calls FB API's getLoginStatus
	getLoginState() { 
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
             

              //get login state after FB SDK is initialized 
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
		//handles reloading the login page after user logout since state is pushed via location state
		const loadingGif = (<img className="headerbox" src={require('../imgs/loading.gif')} alt={"loading"}/>);
		const loggedIn = (this.props.location.state === undefined) ? this.state.loggedIn : this.props.location.state.loggedIn;
		return ( <div> 
			{ !loggedIn ? <Logo loggedIn={loggedIn} 
								onLogin={this.login} 
								isDisabled={this.state.isDisabled} 
								textDisplay={this.state.textDisplay}
								location={this.props.location}/> 
			: loadingGif
			}
			</div>
		)
	}
}

export default LoginComponent;