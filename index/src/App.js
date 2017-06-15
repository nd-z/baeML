import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import ButtonToolbar from 'react-bootstrap';


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
        <h1> Hello, [name] </h1>
        <p> [img] </p>
      
      </div>
    );
  }

}

class Feed extends React.Component {

  render() {
   
    return (
      <div>
        <Sidebar />
        <Article />
      </div>
    );
  }

  
}
export default Feed;