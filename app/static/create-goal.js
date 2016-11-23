import React from 'react';
import { render } from 'react-dom';
import CreateGoal from './scenes/CreateGoal';
import Cookies from 'cookies-js';

render(<CreateGoal csrfToken={Cookies.get('csrftoken')} isFirstGoal={window.DATA.isFirstGoal} />,
    document.getElementById('create'));
