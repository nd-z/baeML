
import React from 'react'
import { render } from 'react-dom'
import { createStore } from 'redux'
import { Provider } from 'react-redux'
import App from './components/App'
import reducer from './reducers'
import Root from './components/Root'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import { compose } from 'redux'
import { autoRehydrate, persistStore } from 'redux-persist'

const store = compose (
	autoRehydrate()
	)(createStore)(reducer);
persistStore(store);

render(
  <Root store={store} />,
  document.getElementById('root')
)
