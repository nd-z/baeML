import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
//set up framework for feed
//tested bootstrap
//img

class Article extends React.Component {
  render() {
    return (
      <div className="article">
        <h1> this represents an article </h1>
        <p> read more about the article at this LINK </p>

      </div>
    );
  }
}


class Sidebar extends React.Component {


  render() {
    return (
      <div className="sidebar">
        <img id="logo" src={require('./logo.svg')}  />
        
        <h1> Hello, [fb api call for name] </h1>
        <p> [facebook api call for profile pic] </p>
        <img id="profilepic" src={require('./testimg.jpg')} />
        <p> logout [facebook api call] </p>
      </div>
    );
  }

}

class Feed extends React.Component {

  render() {
   
    return (
      <div className="feed">
        <Sidebar />
        <Article />
      </div>
    );
  }

  
}
export default Feed;