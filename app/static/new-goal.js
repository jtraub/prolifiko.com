import React from 'react';
import { render } from 'react-dom';
import NewGoal from './components/NewGoal';
import Cookies from 'cookies-js';

render(<NewGoal csrfToken={Cookies.get('csrftoken')} timezones={window.TIMEZONES}/>, document.getElementById("new-goal"));