import React from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'
import { Switch, Router, Route, BrowserRouter } from 'react-router-dom'
import App from './App'
import Feed from './App';
import LoginComponent from '../containers/login_component.js';
import { loadState, saveState } from './localStorage.js';
import { createStore } from 'redux';
import { feed } from './App';

// const persistedState = loadState();
// const store = createStore(
//   feed, persistedState
// );

// store.subscribe(() => {
//   saveState(store.getState());
// })
const Main = () => (
  <main>
    <Switch>
      <Route exact path='/' component={LoginComponent}/>
      <Route path='/feed' component={Feed}/>
      <Route render={
        function() {
          return (<p> Not Found </p>)
        }
      }/>
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