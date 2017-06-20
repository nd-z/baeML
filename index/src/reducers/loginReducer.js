import { combineReducers } from 'redux'
import {
  LOGIN
} from '../index.js'

const initialState = {
  visibilityFilter: VisibilityFilters.SHOW_ALL,
  todos: []
}

function todos(state = [], action) {
  switch (action.type) {
    case LOGIN:
      return [
        ...state,
        {
          text: action.text,
          completed: false
        }
      ]
    
    default:
      return state
  }
}



export default todoApp