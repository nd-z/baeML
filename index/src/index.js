import React from 'react';
import ReactDOM from 'react-dom';
import { Switch, Route, Link, BrowserRouter } from 'react-router-dom';
import Feed from './App';
import LoginComponent from './login_component.js';

const Main = () => (
  <main>
    <Switch>
      <Route exact path='/' component={LoginComponent}/>
      <Route path='/feed' component={Feed}/>
    </Switch>
  </main>
)

ReactDOM.render(
	<BrowserRouter>
  	<Main />
  	</BrowserRouter>,
  document.getElementById('root'),
);