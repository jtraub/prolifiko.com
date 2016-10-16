import React from 'react';
import { render } from 'react-dom';
import CreateMidnightStep from './scenes/CreateMidnightStep';
import Cookies from 'cookies-js';

render(<CreateMidnightStep csrfToken={Cookies.get('csrftoken')}/>, document.getElementById("create"));
