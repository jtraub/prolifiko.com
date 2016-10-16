import React from 'react';
import { CustomGoal } from '../components/GoalDetails';
import GoalTarget  from '../components/GoalTarget';
import StepDetails from '../components/StepDetails';
import StepDeadline from '../components/StepDeadline';
import Scene from '../components/Scene';

export default function CreateGoal({ csrfToken }) {
    console.log('Rendering CreateGoal');

    return <Scene
        csrfToken={csrfToken}
        pages={[
            CustomGoal,
            GoalTarget,
            StepDetails,
            StepDeadline,
        ]}
        data={{ type: 'CUSTOM' }}
    />;
}
