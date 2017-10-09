import * as React from 'react';
import { Table } from 'react-bootstrap';
import User from './User';

interface UsersListProps {
  users: User[];
}

const UsersList = (props: UsersListProps) => (
    <div>
      <h1>All Users</h1>
      <hr />
      <br />
      <Table striped bordered condensed hover>
        <thead>
          <tr>
            <th>User ID</th>
            <th>Email</th>
            <th>Username</th>
          </tr>
        </thead>
        <tbody>
          {
            props.users.map(user => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.email}</td>
                  <td>{user.username}</td>
                  <td>{user.created_at}</td>
                </tr>
            ))
          }
        </tbody>
      </Table>
    </div>
);

export default UsersList;
