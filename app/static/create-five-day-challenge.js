import React from 'react';
import { render } from 'react-dom';
import CreateFiveDayChallenge from './scenes/CreateFiveDayChallenge';
import Cookies from 'cookies-js';

render(<CreateFiveDayChallenge csrfToken={Cookies.get('csrftoken')}/>, document.getElementById('create'));
