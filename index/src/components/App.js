import React from 'react';
import PropTypes from 'prop-types'
import '../css/App.css';
import '../css/index.css'
import axios from 'axios';

class Article extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      loaded_article: false,
      rating: 10,
      article_id: 11111, //dummy var
      user_id: 22222 //dummy var
    };

    // This binding is necessary to make `this` work in the callback
    this.like = this.like.bind(this);
    this.dislike = this.dislike.bind(this);
    this.setRating = this.setRating.bind(this);
  }

  //called when the like button is pressed; sends article & preference to database
  like() {
    this.setState((prevState) => {
      return {liked: true}; //state changed next time it is rendered
    });
    axios.post('http://private-61500-baeml.apiary-mock.com/{user_id}/{article_id}/like')
    .then(function (response) {
      alert('liked'); //good
    })
    .catch(function (error) {
      alert('error');
    });
    
  }
  //called when the dislike button is pressed; sends data to database
  dislike(){
    this.setState((prevState) => {
      return {liked: false}; //state changed next time it is rendered
    });
    axios.post('http://private-61500-baeml.apiary-mock.com/{user_id}/{article_id}/dislike')
    .then(function (response) {
      alert('disliked'); //good
    })
    .catch(function (error) {
      alert('error');
    });    

  }

  //TODO API call
  setRating(rating){
    console.log(rating);
    this.setState({
      rating: rating
      });
    
  }

  render() {
    const ratings = [1,2,3,4,5,6,7,8,9,10]
    return ( //TODO: if liked  / disliked, modify appearance accordingly
      <div className="col-md-8">
        <div className="article">
          <h1> {this.props.title} </h1>
          <p> {this.props.summary} </p>
          <p> read more about the article at this <a href={this.props.link}>LINK</a> <br/> <br/> <br/> <br/> <br/> <br/> <br/> <br/> <br/> <br/> </p>
          
          <div className='ratings-container' className='text-right'>
            <p > Rate this article: </p>{
            ratings.map((rating, index)=> {
            return(
              <button className='rating' key={index} onClick={(e) => this.setRating(rating)}>{rating}</button>
              )
          })
          }</div>
        </div>
      </div>
    );
  }
}

function ArticleContainer(props){
  return (
    <ul className='article-list'>{props.articles.map((article, index) => {
      return (
        <li key={index} className='article-item'>
          <Article title={article.title} link={article.link} summary={article.summary}/>
        </li>
        )
    })}
    </ul>
    )
}

ArticleContainer.propTypes = {
  articles: PropTypes.array.isRequired,
}

function Sidebar(props) {
    return (
      <div className="col-md-4 sidebar">
        <img id="logo" alt="baeML logo" src={require('../imgs/logo.png')}  />
        <div>
          <h1> welcome to your news feed,</h1>
          <h1>{props.name}</h1>
        </div>
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
      articles: [{
          "title": "example",
          "link": "http://www.cs.cornell.edu/courses/cs2112/2016fa/",
          "summary": "dexter kozen!!!!"
        }]
    };
  }

  componentDidMount() {
    window['getProfileInfo'] = this.getProfileInfo
    //if undefined, then reload SDK and call API from there
    if (window.FB === undefined){
      console.log("wut")
      window.fbAsyncInit = () => {
        window.FB.init({
          appId      : '1992517710981460',
          cookie     : true,  // enable cookies to allow the server to access 
                          // the session
          xfbml      : true,  // parse social plugins on this page
          version    : 'v2.9' // use graph api version 2.9
        });
        this.getProfileInfo();
        (function(d, s, id) {
          var js, fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) return;
          js = d.createElement(s); js.id = id;
          js.src = "https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.9&appId=1992517710981460";
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
      }
    } else {
      this.getProfileInfo();
    }

    window.addEventListener('popstate', function () {
    window.location.reload();});
    window.addEventListener('error', function() {alert('Error loading page. Please refresh.')});

    }
    
  //retrieves the profile information
  getProfileInfo() {
    //scale profile pic to screen resolution
    var size = Math.round(window.screen.width*.37);
    window.FB.getLoginStatus((response) => {
      if (response.status === 'connected') { // the user is logged in and has authenticated the app
        //update name in feed
        window.FB.api('/me', (response) => { 
          this.setState({
            name: response.name
          });
        });

        //update picture on feed
        window.FB.api('/me/picture?height=' + size + '&width=' + size, (response) => {
          this.setState({ 
            profilepic: response.data.url
          });
        });
      } else {
        alert('Error logging in. Please refresh the page and try again.');
        window.location.reload();
      }
    });
    setTimeout(() => this.setState({ loading: false }), 500); 
  }


  render() {
    if (this.state.loading){
      return(
        <img className="headerbox" src={require('../imgs/loading.gif')} alt={"loading"}/>
      );
    }

    return (
      <div className="row">
        <Sidebar name={this.state.name} imgurl={this.state.profilepic} history={this.props.history}/>
        <ArticleContainer articles={this.state.articles} />
      </div>
    );
  }
  
}
export default Feed;