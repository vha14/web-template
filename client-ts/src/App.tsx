import * as React from 'react';
import { Route, Switch } from 'react-router-dom';
import axios from 'axios';

import UsersList from './components/UsersList';
import About from './components/About';
import NavBar from './components/NavBar';
import Form from './components/Form';
import { FormData } from './components/Form';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';
import { ChangeEvent, Component, FormEvent } from 'react';
import User from './components/User';

interface State {
  users: User[];
  username: string;
  email: string;
  title: string;
  formData: FormData;
  isAuthenticated: boolean;
}

class App extends Component<{}, State> {
  static SERVICE_URL = process.env.REACT_APP_USERS_SERVICE_URL;
  constructor() {
    super();
    this.state = {
      users: [],
      username: '',
      email: '',
      title: '*',
      formData: {
        username: '',
        email: '',
        password: '',
      },
      isAuthenticated: false,
    };
    this.handleFormChange = this.handleFormChange.bind(this);
    this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
  }

  componentDidMount() {
    this.getUsers();
  }

  getUsers() {
    axios.get(`${App.SERVICE_URL}/users`)
        .then(res => this.setState({users: res.data.data.users}));
  }

  handleUserFormSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formType = window.location.href.split('/').reverse()[0];
    const data = {
      username: '',
      email: this.state.formData.email,
      password: this.state.formData.password,
    };
    if (formType === 'register') {
      data.username = this.state.formData.username;
    }
    axios.post(`${App.SERVICE_URL}/auth/${formType}`, data)
        .then((res) => {
          this.setState({
            formData: {username: '', email: '', password: ''},
            username: '',
            email: '',
            isAuthenticated: true,
          });
          window.localStorage.setItem('authToken', res.data.auth_token);
          this.getUsers();
        });
  }

  handleFormChange(event: ChangeEvent<HTMLInputElement>) {
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState(() => (obj));
  }

  logoutUser() {
    window.localStorage.clear();
    this.setState({isAuthenticated: false});
  }

  mainRoute() {
    return (
        <Route
            exact
            path="/"
            render={() => (
                <UsersList
                    users={this.state.users}
                />
            )}
        />);
  }

  loginRoute() {
    return (
        <Route
            exact
            path="/login"
            render={() => (
                <Form
                    formType={'Login'}
                    formData={this.state.formData}
                    handleFormChange={this.handleFormChange}
                    handleUserFormSubmit={this.handleUserFormSubmit}
                    isAuthenticated={this.state.isAuthenticated}
                />
            )}
        />);
  }

  logoutRoute() {
    return (
        <Route
            exact
            path="/logout"
            render={() => (
                <Logout
                    logoutUser={this.logoutUser}
                    isAuthenticated={this.state.isAuthenticated}
                />
            )}
        />);
  }

  registerRoute() {
    return (
        <Route
            exact
            path="/register"
            render={() => (
                <Form
                    formType={'Register'}
                    formData={this.state.formData}
                    handleFormChange={this.handleFormChange}
                    handleUserFormSubmit={this.handleUserFormSubmit}
                    isAuthenticated={this.state.isAuthenticated}
                />
            )}
        />);
  }

  statusRoute() {
    return (
        <Route
            exact
            path="/status"
            render={() => (
                <UserStatus
                    isAuthenticated={this.state.isAuthenticated}
                />
            )}
        />);
  }

  render() {
    return (
        <div>
          <NavBar
              title={this.state.title}
              isAuthenticated={this.state.isAuthenticated}
          />
          <div className="container">
            <div className="row">
              <div className="col-md-6">
                <br />
                <Switch>
                  {this.mainRoute()}
                  <Route exact path="/about" component={About} />
                  {this.loginRoute()}
                  {this.logoutRoute()}
                  {this.registerRoute()}
                  {this.statusRoute()}
                </Switch>
              </div>
            </div>
          </div>
        </div>
    );
  }
}

export default App;
