import * as React from 'react';
import { Link } from 'react-router-dom';
import { Component } from 'react';

interface LogoutProps {
  logoutUser: () => void;
  isAuthenticated: boolean;
}

class Logout extends Component<LogoutProps, {}> {
  componentDidMount() {
    this.props.logoutUser();
  }

  render() {
    return (
        <div>
          <p>You are now logged out. Click <Link to="/login">here</Link> to log back in.</p>
        </div>
    );
  }
}

export default Logout;
