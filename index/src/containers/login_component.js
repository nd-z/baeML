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
	constructor(props) {
		super(props);
		this.state = {
			isDisabled: false,
			textDisplay: "Login below to start getting recommendations"
		}
		this.login = this.login.bind(this);
		this.displayError = this.displayError.bind(this);
	}

	//handles logging into FB 
	login() {
		this.props.fb.login((response) => {
			if (response.status === 'connected'){
				console.log("should disable")
				this.setState({
					isDisabled: true,
					textDisplay: "Setting up your feed..."
				})
				var userID = response.authResponse.userID
				var accessToken = response.authResponse.accessToken

				axios.get('/api/status/', {
					params: {
						user_ID: userID,
					}
				})
				.then((response) => { 
					if (response.status === 204) {
		        		console.log('new user');
		        		axios.post('/api/init/', {
							user_ID: userID,
							token: accessToken,
							size: Math.round(window.screen.width*.37)
						})
						.then((response) => {
							console.log("hi")	
						})
	        		}
		    	})
				.catch((error) => {
					console.log(error.response)
					this.displayError(error);
				});
			//upon login, call loginstatus to reflect user logged in via FB
			this.props.loginStatus();
			}
		}, {scope: 'public_profile,user_likes'});
	}

	displayError(message){
		this.setState({
			isDisabled: false,
			textDisplay: message
		})
	}

	//renders the landing page
	render () {
		return ( 
			<div> 
				<Logo 
					onLogin={this.login} 
					isDisabled={this.state.isDisabled} 
					textDisplay={this.state.textDisplay}
					location={this.props.location}/> 
			</div>
		)
	}
}

export default LoginComponent;