import React from 'react';
import ReactDOM from 'react-dom';
import './css/App.css';
//set up framework for feed
//tested bootstrap
//img

class Article extends React.Component {
  render() {
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
}


class Sidebar extends React.Component {

  render() {
    return (
      <div className="col-md-4 sidebar">
        <img id="logo" src={require('./imgs/logo.png')}  />
        <h1> welcome to your personal news feed</h1>
        <p> [facebook api call for profile pic] </p>
        <img id="profilepic" src={require('./imgs/testimg.jpg')} />
        <p> logout [facebook api call] </p>
      </div>
    );
  }

}

class Feed extends React.Component {

  componentDidMount() {
    var component = ReactDOM.findDOMNode(this);
    component.style.opacity = 0;
    window.requestAnimationFrame(function() {
      component.style.transition = "opacity 2000ms";
      component.style.opacity = 1;
    });
  }

  render() {
    return (
      <div className="row">
        <Sidebar />
        <Article />
      </div>
    );
  }

  
}
export default Feed;