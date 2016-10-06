import React from 'react';
import {CustomGoal} from './GoalDetails';
import GoalTarget  from './GoalTarget';
import StepDetails from './StepDetails';
import StepDeadline from './StepDeadline';
import Scene from './Scene';

export default function CreateGoal({csrfToken}) {
    console.log('Rendering CreateGoal');

    return <Scene
        csrfToken={csrfToken}
        pages={[
            GoalTarget,
            CustomGoal,
            StepDetails,
            StepDeadline,
        ]}
        data={{ type: 'CUSTOM' }}
    />;
}
