import React from 'react';
import ReactDOM from 'react-dom';
import '../css/App.css';
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
      window.FB.getLoginStatus((response) => { 
        if (response.status === 'connected') {
            window.FB.logout((response) => {});
            console.log("logout");
            this.props.history.push('/', {loggedIn: false});
          }
        });
  }

  render() { 
    return (<div id="fbLogout">
    <button className="fbButton" onClick={(e) => this.fbLogout()}>
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
    // this.getProfileInfo = this.getProfileInfo.bind(this);
  }

  
  componentDidMount() {
    window['getProfileInfo'] = this.getProfileInfo

    var component = ReactDOM.findDOMNode(this);
    component.style.opacity = 0;
    window.requestAnimationFrame(function() {
      component.style.transition = "opacity 2000ms";
      component.style.opacity = 1;
    });
    
  //if undefined, then reload SDK and call API from there
  if (window.FB === undefined){
      window.fbAsyncInit = () => {
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
        
      window.FB.getLoginStatus((response) => {
        if (response.status === 'connected') { // the user is logged in and has authenticated the app
          //update name on feed
          this.getProfileInfo();
        } else {
        // redirect user
        }
      });
      window.onpopstate = this.onBackButtonEvent;
      }
    } else { //otherwise just call directly from the API
      this.getProfileInfo();
    }
  }

  //retrieves the profile information
  getProfileInfo() {
    console.log("hi")
    window.FB.api('/me', (response) => { 
          this.setState({
            name: response.name
          });
        });
        
      //update picture on feed
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