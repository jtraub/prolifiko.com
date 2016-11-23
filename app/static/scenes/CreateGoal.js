import React from 'react';
import { CustomGoalDetails, FirstGoalDetails } from '../components/GoalDetails';
import GoalTarget  from '../components/GoalTarget';
import { CustomStepDetails, FirstStepDetails } from '../components/StepDetails';
import StepDeadline from '../components/StepDeadline';
import Scene from '../components/Scene';

export default function CreateGoal({ csrfToken, isFirstGoal }) {
    console.log('Rendering CreateGoal');

    const goalDetails = isFirstGoal ? FirstGoalDetails : CustomGoalDetails;
    const stepDetails = isFirstGoal ? FirstStepDetails : CustomStepDetails;

    return <Scene
        csrfToken={csrfToken}
        pages={[
            goalDetails,
            GoalTarget,
            stepDetails,
            StepDeadline,
        ]}
        data={{ type: 'CUSTOM' }}
    />;
}
