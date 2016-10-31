import React from 'react';
import { MidnightStepDetails } from '../components/StepDetails';
import { FiveDayChallengeDetails } from '../components/GoalDetails';
import Scene from '../components/Scene';

export default function CreateFiveDayChallenge({ csrfToken }) {
    console.log('Rendering CreateFiveDayChallenge');

    return <Scene
        csrfToken={csrfToken}
        pages={[
            FiveDayChallengeDetails,
            props => <MidnightStepDetails {...props} stepNumber={1} />
        ]}
        data={{ type: 'FIVE_DAY_CHALLENGE' }}
    />;
}
