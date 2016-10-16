import React from 'react';
import { render } from 'react-dom';
import CreateStep from './scenes/CreateStep';
import Cookies from 'cookies-js';

render(<CreateStep csrfToken={Cookies.get('csrftoken')}/>, document.getElementById("create"));
