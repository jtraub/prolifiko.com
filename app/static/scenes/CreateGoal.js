import React from 'react';
import { CustomGoalDetails, FirstGoalDetails } from '../components/GoalDetails';
import GoalTarget, { FirstGoalTarget }  from '../components/GoalTarget';
import { CustomStepDetails, FirstStepDetails } from '../components/StepDetails';
import StepDeadline from '../components/StepDeadline';
import Scene from '../components/Scene';

export default function CreateGoal({ csrfToken, isFirstGoal }) {
    console.log('Rendering CreateGoal');

    const goalDetails = isFirstGoal ? FirstGoalDetails : CustomGoalDetails;
    const goalTarget = isFirstGoal ? FirstGoalTarget: GoalTarget;
    const stepDetails = isFirstGoal ? FirstStepDetails : CustomStepDetails;

    return <Scene
        csrfToken={csrfToken}
        pages={[
            goalDetails,
            goalTarget,
            stepDetails,
            StepDeadline,
        ]}
        data={{ type: 'CUSTOM' }}
    />;
}
