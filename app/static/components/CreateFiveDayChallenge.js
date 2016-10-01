import React from 'react';
import StepDetails from './StepDetails';

import GoalDetails from './GoalDetails';
import Scene from './Scene';



export default function CreateFiveDayChallenge({csrfToken}) {

    return <Scene csrfToken={csrfToken} pages={[GoalDetails, StepDetails]} />;
}


