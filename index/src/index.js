
import React from 'react'
import { render } from 'react-dom'
import { createStore } from 'redux'
import reducer from './reducers'
import Root from './components/Root'
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
