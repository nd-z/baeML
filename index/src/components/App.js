import React from 'react';
import ReactDOM from 'react-dom';
import '../css/App.css';
import {combineReducers} from 'redux';
//set up framework for feed
//tested bootstrap
//img

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
        <img id="logo" alt="baeML logo" src={require('../imgs/logo.png')}  />
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

// function confirmexit(){
//     window.location.href='/';
    
//   }

// export const feed = ();

class Feed extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      name: "",
      profilepic: ""
    };
  }

  
  componentDidMount() {
    var component = ReactDOM.findDOMNode(this);
    component.style.opacity = 0;
    window.requestAnimationFrame(function() {
      component.style.transition = "opacity 2000ms";
      component.style.opacity = 1;
    });
    
  
    
    window.fbAsyncInit = function() {
      window.FB.init({
        appId      : '1992517710981460',
        cookie     : true,  // enable cookies to allow the server to access 
                        // the session
        xfbml      : true,  // parse social plugins on this page
        version    : 'v2.9' // use graph api version 2.8
   });

    (function(d, s, id) {
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return;
      js = d.createElement(s); js.id = id;
      js.src = "https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.9&appId=1992517710981460";
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

/**BUG: somehow, i get a response when i reload /feed but not when i'm redirected from / **/
      
    window.FB.getLoginStatus(function(response) {
      alert('getting login status');
      if (response.status === 'connected') { // the user is logged in and has authenticated the app
        alert('connected, retrieving profile info');  /***REACHES THIS!! **/
        //update name on feed
        window.FB.api('/me', (response) => {
          this.setState({ /**BUG: THIS.SETSTATE IS NOT A FUNCTION**/
            name: response.name
          });
        });
        
        //update picture on feed
        window.FB.api('/me/picture?type=large', (response) => {
          this.setState({ /**BUG: THIS.SETSTATE IS NOT A FUNCTION**/
            profilepic: response.data.url
          });
        });
        alert('done retrieving'); /***REACHES THIS!! **/
      } else {
      // redirect user
      }
    });

    window.onpopstate = this.onBackButtonEvent;
    // window.onbeforeunload = confirmexit();

  }

}


  
  

  onBackButtonEvent(e){
    window.location.reload();
    alert("Jej");
  }

  // reducer(fbName, profilePic){
  //   return Object.assign({}, {
  //       name: fbName, 
  //       profilepic: fbPic
  //     })
  // }
  
  

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