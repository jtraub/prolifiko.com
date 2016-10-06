import React from 'react';
import StepDetails from './StepDetails';
import {FiveDayChallenge} from './GoalDetails';
import Scene from './Scene';

export default function CreateFiveDayChallenge({csrfToken}) {
    return <Scene
        csrfToken={csrfToken}
        pages={[FiveDayChallenge, StepDetails]}
        data={{ type: 'FIVE_DAY_CHALLENGE' }}
    />;
}
