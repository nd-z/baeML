import React from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'
import { Switch, Router, Route, BrowserRouter } from 'react-router-dom'
import App from './App'
import Feed from './App';
import LoginComponent from '../login_component.js';

const Main = () => (
  <main>
    <Switch>
      <Route exact path='/' component={LoginComponent}/>
      <Route path='/feed' component={Feed}/>
    </Switch>
  </main>
)

const Root = ({ store }) => (
  <Provider store={store}>
    <BrowserRouter>
      <Main />
    </BrowserRouter>
  </Provider>
)




Root.propTypes = {
  store: PropTypes.object.isRequired
}

export default Root