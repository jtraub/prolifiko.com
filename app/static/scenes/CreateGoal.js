import React from 'react';
import { CustomGoalDetails } from '../components/GoalDetails';
import GoalTarget  from '../components/GoalTarget';
import { CustomStepDetails } from '../components/StepDetails';
import StepDeadline from '../components/StepDeadline';
import Scene from '../components/Scene';

export default function CreateGoal({ csrfToken }) {
    console.log('Rendering CreateGoal');

    return <Scene
        csrfToken={csrfToken}
        pages={[
            CustomGoalDetails,
            GoalTarget,
            props => <CustomStepDetails {...props} stepNumber={1} />,
            StepDeadline,
        ]}
        data={{ type: 'CUSTOM' }}
    />;
}
