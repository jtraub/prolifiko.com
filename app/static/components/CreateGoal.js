import React from 'react';

import GoalDetails from './GoalDetails';
import GoalTarget from './GoalTarget';
import StepDetails from './StepDetails';
import StepDeadline from './StepDeadline';
import Scene from './Scene';



export default function CreateGoal({csrfToken}) {

    return <Scene csrfToken={csrfToken} pages={[
        GoalTarget,
        GoalDetails,
        StepDetails,
        StepDeadline,
    ]} />;
}
