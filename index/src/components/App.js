import React from 'react';
import PropTypes from 'prop-types'
import '../css/App.css';
import '../css/index.css'
import axios from 'axios';

class Article extends React.Component {

  constructor(props){
  	//fetch article
    super(props);
    this.state = {
      loaded_article: false,
      // rating: 10,
      // article_id: 11111, //dummy var
      // user_id: 22222 //dummy var
      article_link: 'jej', //dummy var
      user_id: 100 //dummy var
    };

    // This binding is necessary to make `this` work in the callback
    this.setRating = this.setRating.bind(this);
  }
  componentDidMount() {
   this.setState({
          user_id: this.props.user_ID,
          loaded_article: true,
          article_link: this.props.link,
         
        });
  }

  // TODO test
  getNextArticle() {
  	axios.get('/api/users/next_article', { 
    	params: {
			user_ID: this.props.userID
		}
    })
    .then(function (response) {
      if (response.status === 200) {
        console.log('got next article in app.js'); 
        this.setState({
        	"title": response.data.article_title,
            "link": response.data.article_link,
            "content": response.data.article
        });
      }
      else{
        alert ('rip');
      }

    })
    .catch(function (error) {
      alert('error');
    });    
  }

  setRating(rating){
    this.setState({
      rating: rating
      });

    axios.post('/api/users/rate_article', { //TODO test
    	"user_id": this.state.user_id,
    	"article_link": this.state.link,
    	"user_rating": {rating}
    })
    .then(function (response) {
      if (response.status === 201) {
        console.log('rated'); //good
      }
      else{
        alert ('rip');
      }

    })
    .catch(function (error) {
      alert('error');
    });    
  }

  render() {
    const ratings = [1,2,3,4,5,6,7,8,9,10]
    return (
      <div className="col-md-8">
        <div className="article">
          <h2> {this.state.title} </h2>
          <p> {this.state.content} </p>
          <p> Read more about the article at this <a href={this.state.link}>LINK</a></p>
          <button className="button" onclick="this.getNextArticle"><span>next</span></button>
        </div>
        <div className='ratings-container'>
            <p> rate article </p> <span> <form> {
            ratings.map((rating, index)=> {
            return (

                <label key={index}>
                   <input  name="rating-scale" className="radio-btn" type="radio" key={index} onClick={(e) => this.setRating(rating)}/>
                   <p>{rating}</p>
                </label>
                
              )
          })
          }</form></span></div>
      </div>
    );
  }
}

function ArticleContainer(props){
  return (
    <div>{props.articles.map((article, index) => {
      return (
        <div key={index}>
          <Article title={article.title} link={article.link} content={article.content} user_id={props.user_ID}/>
        </div>
        )
    })}
    </div>
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
        <Logout loginStatus={props.loginStatus}/>
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
            window.FB.logout((response) => {
              //call loginStatus to update login status
              this.props.loginStatus();
            });
          }
        });
  }

  render() { 
    return (
      <div id="fbLogout">
        <button className="fbButton" onClick={(e) => this.fbLogout()}>
        Logout
        </button>
      </div>)
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
          "content": "article content goes here!"
        }]
    };
  }

  componentDidMount() {
    console.log(this.props.userID())
    axios.get('/api/login', { 
      params: {
        user_ID: this.props.userID(),
      }
      }).then((response)=>{
        console.log(response);
        this.setState({
          name: response.data.name,
          profilepic: response.data.propic,
          articles: [{
            "title": response.data.article_title,
            "link": response.data.article_link,
            "content": response.data.article
          }],
          loading: false
        })
      }).catch((error)=>{
        console.log(error)
        this.setState({
          loading: false
        })
      });
  }

  render() {
    if (this.state.loading){

      return(
        <img className="headerbox" src={require('../imgs/loading.gif')} alt={"loading"}/>
      );
    }

    return (
      <div className="row">
        <Sidebar name={this.state.name} imgurl={this.state.profilepic} loginStatus={this.props.loginStatus}/>
        <ArticleContainer articles={this.state.articles} user_ID={this.props.userID()}/>
      </div>
    );
  }
  
}
export default Feed;