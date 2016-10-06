import React from 'react';
import { render } from 'react-dom';
import CreateGoal from './scenes/CreateGoal';
import Cookies from 'cookies-js';

render(<CreateGoal csrfToken={Cookies.get('csrftoken')}/>, document.getElementById("new-goal"));
