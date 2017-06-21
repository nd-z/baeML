import React from 'react';
import ReactDOM from 'react-dom';
import '../css/App.css';


class Article extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      loaded_article: false,
      liked: false
    };

    // This binding is necessary to make `this` work in the callback
    this.like = this.like.bind(this);
    this.dislike = this.dislike.bind(this);
  }
  
  like() {
    this.setState({liked: true});
    alert('liked');
  }
  dislike(){
    this.setState({liked: false});
    alert('disliked');

  }
  render() {
    return (
      <div className="col-md-8">
        <div className="article">
          <h1> this represents an article </h1>
          <p> read more about the article at this LINK <br/> <br/> <br/> <br/> <br/> <br/> <br/> <br/> <br/> <br/> </p>
          <button type="button" className="btn like" aria-label="Like" onClick={this.like}>
            <span className="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span>
          </button>
          <button type="button" className="btn dislike" aria-label="Dislike" onClick={this.dislike}>
            <span className="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span>
          </button>
        </div>
      </div>
    );
  }
}




function Sidebar(props) {
    return (
      <div className="col-md-4 sidebar">
        <img id="logo" alt="baeML logo" src={require('../imgs/logo.png')}  />
        <h1> welcome to your news feed,</h1>
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


class Feed extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      loading: true,
      name: "",
      profilepic: "",
    };
  }

  componentDidMount() {
    var component = ReactDOM.findDOMNode(this);
    component.style.opacity = 0;
    window.requestAnimationFrame(function() {
      component.style.transition = "opacity 2000ms";
      component.style.opacity = 1;
    });
    window['getProfileInfo'] = this.getProfileInfo
    
    //if undefined, then reload SDK and call API from there
    if (window.FB === undefined){

      window.fbAsyncInit = () => {
        window.FB.init({
          appId      : '1992517710981460',
          cookie     : true,  // enable cookies to allow the server to access 
                          // the session
          xfbml      : true,  // parse social plugins on this page
          version    : 'v2.9' // use graph api version 2.9
        });

        (function(d, s, id) {
          var js, fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) return;
          js = d.createElement(s); js.id = id;
          js.src = "https://connect.facebook.net/en_US/all.js#xfbml=1&version=v2.9&appId=1992517710981460";
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));

        
        window.FB.getLoginStatus((response) => {
          if (response.status === 'connected') { // the user is logged in and has authenticated the app
            this.getProfileInfo();
          } else {
            alert('Error logging in. Please refresh the page and try again.');
            window.location.reload();
          }
        });
      }
    } else { //if directed from login, just call directly from the API
      this.getProfileInfo();
    }
    window.addEventListener('popstate', function () {
    window.location.reload();});
    window.addEventListener('error', function() {alert('Error loading page. Please refresh.')});

    }
    
  

  //retrieves the profile information
  getProfileInfo() {
    //update name in feed
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
    setTimeout(() => this.setState({ loading: false }), 500); 
  }


  render() {
    if (this.state.loading){
      return(
        <p id="loadingScreen">Loading your personalized newsfeed...</p>
      );
    }

    return (
      <div className="row">
        <Sidebar name={this.state.name} imgurl={this.state.profilepic} history={this.props.history}/>
        <Article />
      </div>
    );
  }
  
}
export default Feed;