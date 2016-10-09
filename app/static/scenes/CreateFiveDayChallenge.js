import React from 'react';
import StepDetails from '../components/StepDetails';
import { FiveDayChallengeGoal } from '../components/GoalDetails';
import Scene from '../components/Scene';

export default function CreateFiveDayChallenge({ csrfToken }) {
    return <Scene
        csrfToken={csrfToken}
        pages={[FiveDayChallengeGoal, StepDetails]}
        data={{ type: 'FIVE_DAY_CHALLENGE' }}
    />;
}
