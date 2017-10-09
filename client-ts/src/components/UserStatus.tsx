import * as React from 'react';
import { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import User from './User';

interface UserStatusProps {
  isAuthenticated: boolean;
}

class UserStatus extends Component<UserStatusProps, User> {
  constructor(props: UserStatusProps) {
    super(props);
    this.state = {
      created_at: '',
      email: '',
      id: '',
      username: '',
    };
  }

  componentDidMount() {
    if (this.props.isAuthenticated) {
      this.getUserStatus();
    }
  }

  getUserStatus() {
    const req = {
      url: `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/status`,
      method: 'get',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${window.localStorage.authToken}`,
      },
    };
    return axios(req)
        .then((res) => {
          const user = res.data.data;
          this.setState({
            created_at: user.created_at,
            email: user.email,
            id: user.id,
            username: user.username,
          });
        });
  }

  render() {
    if (!this.props.isAuthenticated) {
      return <p>You must be logged in to view this. Click <Link to="/login">here</Link> to log back in.</p>;
    }
    return (
        <div>
          <ul>
            <li><strong>User ID:</strong> {this.state.id}</li>
            <li><strong>Email:</strong> {this.state.email}</li>
            <li><strong>Username:</strong> {this.state.username}</li>
          </ul>
        </div>
    );
  }
}

export default UserStatus;
