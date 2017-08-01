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
					//if user has been init before, log them in
					if (response.status === 200){
						this.props.loginStatus();
					} else if (response.status === 204) {
						//otherwise, new user, init them
		        		console.log('new user');
		        		axios.post('/api/init/', {
							user_id: userID,
							token: accessToken,
							size: Math.round(window.screen.width*.37)
						}).then((response)=>console.log(response.status))

						//run call every 45s to check if it is complete yet
						var interval = 45 * 1000
						var interval_id = setInterval(()=> {
							console.log("checking...")
							axios.get('/api/status/', {
								params: {
									user_ID: userID,
								}
							}).then((response) => {
								//on complete, redirect to login
								if (response.status === 200){
									console.log("yay!")
									this.props.loginStatus();
									clearInterval(interval_id)
								} else {
									console.log("nope")
								}
							})
						}, interval)
	        		}
		    	})
				.catch((error) => {
					console.log(error.response)
					var message =  "An error occurred in retrieving your feed, please try again later.";
					if (typeof(error.response) !== undefined){
						message = error.response.data.message;
					}
					this.displayError(message);
				});
			//upon login, call loginstatus to reflect user logged in via FB
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