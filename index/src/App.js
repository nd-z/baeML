import React from 'react';
import ReactDOM from 'react-dom';
import './css/App.css';
import FbSDK from './fbSDKLoader';
//set up framework for feed
//tested bootstrap
//img

window.FB = FbSDK.loadFbSDK();
function Article() {
    return (
      <div className="col-md-8">
        <div className="article">
          <h1> this represents an article </h1>
          <p> read more about the article at this LINK </p>
        </div>
        <div className="article">
          <h1> this represents an article </h1>
          <p> read more about the article at this LINK </p>
        </div>
      </div>
    );
}


function Sidebar(props) {
    return (
      <div className="col-md-4 sidebar">
        <img id="logo" alt="baeML logo" src={require('./imgs/logo.png')}  />
        <h1> welcome to your personal news feed,</h1>
        <h1>{props.name}</h1>
        <img id="profilepic" alt="Profile pic" src={props.imgurl} />
        <Logout history={props.history}/>
      </div>
    );
}

class Logout extends React.Component {
  constructor(props) {
    super(props);
    this.fbLogout = this.fbLogout.bind(this);
  }

  fbLogout(){
        window.FB.logout(function (response) {
        });
        console.log("logout");
        this.props.history.push('/');
  }

  render() { 
    return (<div id="fbLogout">
    <button className="fb_button fb_button_medium" onClick={(e) => this.fbLogout()}>
   Logout</button></div>)
  }

}

class Feed extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      name: "",
      profilepic: ""
    }
  }

  componentDidMount() {
    var component = ReactDOM.findDOMNode(this);
    component.style.opacity = 0;
    window.requestAnimationFrame(function() {
      component.style.transition = "opacity 2000ms";
      component.style.opacity = 1;
    });
    this.getProfileInfo();
    window.onpopstate = this.onBackButtonEvent;
  }

  getProfileInfo(){
    window.FB.api('/me', (response) => {
      this.setState({ 
        name: response.name
      });
    });
    
    window.FB.api('/me/picture?type=large', (response) => {
      this.setState({ 
        profilepic: response.data.url
      });
    });
  }
  onBackButtonEvent(e){
    window.location.reload();
  }

  render() {
    
    return (
      <div className="row">
        <Sidebar name={this.state.name} imgurl={this.state.profilepic} history={this.props.history}/>
        <Article />
      </div>
    );
  }

  
}
export default Feed;