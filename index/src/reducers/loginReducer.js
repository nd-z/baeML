const initialState = new Immutable.Map({
  email: '',
  password: '',
  isLoggingIn: false,
  isLoggedIn: false,
  error: null
});

export default function user(state = initialState, action) {
  switch (action.type) {
    case LOGIN_ATTEMPT:
      return state.merge({
        isLoggingIn: true,
        isLoggedIn: false,
        email: action.email,
        password: action.password // Note you shouldn't store user's password in real apps
      });
    case LOGGED_FAILED:
      return state.merge({
        error: action.error,
        isLoggingIn: false,
        isLoggedIn: false
      });
    case LOGGED_SUCCESSFULLY:
      return state.merge({
        error: null,
        isLoggingIn: false,
        isLoggedIn: true
      });
      break;
    default:
      return state;
  }