var ReactRouter = require("react-router"),
    Login = require("./login_component"),
    Feed = require("./App"),
    Frame = require("./Frame/Frame");

var Router = ReactRouter.Router;
var Route = ReactRouter.Route;

module.exports = (
  <Router>
    <Route component = {Frame}/>
      <Route path="/" component={Feed} />
      <Route path="/login" component={Login} />
    </Route>
  </Router>
);