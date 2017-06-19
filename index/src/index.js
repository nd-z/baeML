import React from 'react';
import ReactDOM from 'react-dom';
import { Switch, Route, BrowserRouter} from 'react-router-dom';
import Feed from './App';
import LoginComponent from './login_component.js';

const Main = () => (
  <BrowserRouter>
    <Switch>
      <Route exact path='/' component={LoginComponent}/>
      <Route exact path='/feed' component={Feed}/>
      <Route render={
        function() {
          return (<p> Not Found </p>)
        }
      }/>
    </Switch>
  </BrowserRouter>)

ReactDOM.render(
  	<Main />,
  document.getElementById('root'),
);